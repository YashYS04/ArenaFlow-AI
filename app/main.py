from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app.config import Settings, get_settings
from app.logging_conf import get_logger
from app.models.schemas import (
    AccessibilityNeed,
    AssistResponse,
    DestinationIntent,
    HealthResponse,
    Language,
    UserContext,
)
from app.services import phrasing as phr
from app.services.context_engine import RouteNotFound, build_decision, run_assist
from app.services.incidents import get_incident_manager
from app.services.llm import get_llm_client
from app.services.security import RateLimiter
from app.services.stadium_data import Stadium, get_stadium

logger = get_logger("arenaflow")

_STATIC_DIR = Path(__file__).resolve().parent / "static"

_SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Content-Security-Policy": (
        "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; "
        "connect-src 'self'; base-uri 'none'; frame-ancestors 'none'"
    ),
}


def _stadium_metadata(stadium: Stadium) -> dict[str, Any]:
    return {
        "stadium": {
            "name": stadium.name,
            "fifa_name": stadium.fifa_name,
            "city": stadium.city,
            "capacity": stadium.capacity,
        },
        "zones": [
            {"id": z.id, "name": z.names, "type": z.type, "level": z.level}
            for z in stadium.zones.values()
        ],
        "facilities": [
            {
                "id": f.id,
                "name": f.names,
                "type": f.type,
                "zone": f.zone,
                "accessible": f.accessible,
                "landmark": f.landmarks,
            }
            for f in stadium.facilities
        ],
        "intents": [i.value for i in DestinationIntent],
        "languages": [lang.value for lang in Language],
        "accessibility_needs": [n.value for n in AccessibilityNeed],
    }


def _rate_limit_dependency(request: Request) -> None:
    limiter: RateLimiter = request.app.state.rate_limiter
    client_ip = request.client.host if request.client else "unknown"
    allowed, retry_after = limiter.check(client_ip)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please slow down.",
            headers={"Retry-After": str(int(retry_after) + 1)},
        )


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()

    app = FastAPI(
        title="ArenaFlow",
        description="Multilingual, accessible stadium operations assistant for FIFA World Cup 2026.",
        version="1.0.0",
    )

    app.state.settings = settings
    app.state.stadium = get_stadium()
    app.state.llm = get_llm_client(settings)
    app.state.rate_limiter = RateLimiter(
        settings.rate_limit_capacity, settings.rate_limit_refill_per_sec
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

    @app.middleware("http")
    async def add_security_headers(request: Request, call_next: Any) -> Any:
        response = await call_next(request)
        for header, value in _SECURITY_HEADERS.items():
            response.headers.setdefault(header, value)
        return response

    @app.exception_handler(RouteNotFound)
    async def _route_not_found_handler(request: Request, exc: RouteNotFound) -> JSONResponse:
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.get("/health", response_model=HealthResponse, tags=["system"])
    async def health() -> HealthResponse:
        return HealthResponse(status="ok")

    @app.get("/api/stadium", tags=["data"])
    async def stadium_metadata(request: Request) -> dict[str, Any]:
        return _stadium_metadata(request.app.state.stadium)

    @app.post(
        "/api/assist",
        response_model=AssistResponse,
        dependencies=[Depends(_rate_limit_dependency)],
        tags=["assist"],
    )
    async def assist(ctx: UserContext, request: Request) -> AssistResponse:
        stadium: Stadium = request.app.state.stadium
        llm = request.app.state.llm
        response = await run_assist(ctx, stadium, llm)
        logger.info(
            "assist location=%s intent=%s needs=%s crowd=%s used_llm=%s",
            ctx.current_location,
            ctx.destination_intent.value,
            "+".join(n.value for n in ctx.accessibility_needs),
            response.crowd_level.value,
            response.used_llm,
        )
        return response

    @app.post(
        "/api/assist/stream",
        dependencies=[Depends(_rate_limit_dependency)],
        tags=["assist"],
    )
    async def assist_stream(ctx: UserContext, request: Request) -> StreamingResponse:
        stadium: Stadium = request.app.state.stadium
        llm = request.app.state.llm

        decision = build_decision(ctx, stadium)

        phrasing_ctx = phr.PhrasingContext(
            language=decision.language,
            facility_name=decision.facility.name,
            facility_type=decision.facility.type,
            facility_landmark=decision.facility.landmark,
            crowd_level=decision.crowd_level.value,
            accessibility_mode=decision.accessibility_mode.value,
            landmark_based=decision.landmark_based,
            hurry=decision.hurry,
            alternative_type=decision.facility.type if decision.alternatives_note else None,
            total_distance=sum(step.distance for step in decision.route_steps),
            step_count=len(decision.route_steps),
            persona=ctx.persona.value,
            incident_id=decision.incident_id,
            incident_type=decision.incident_type,
            incident_desc=decision.incident_desc,
        )

        async def event_generator() -> AsyncIterator[str]:
            if not ctx.question:
                answer = phr.render_answer(phrasing_ctx)
                res = AssistResponse(
                    answer=answer,
                    route_steps=decision.route_steps,
                    facility=decision.facility,
                    crowd_level=decision.crowd_level,
                    language=ctx.language,
                    accessibility_mode=decision.accessibility_mode,
                    alternatives_note=decision.alternatives_note,
                    urgency=decision.urgency,
                    used_llm=False,
                    incident_action_logged=decision.incident_id,
                )
                yield f"event: result\ndata: {res.model_dump_json()}\n\n"
                return

            initial_res = AssistResponse(
                answer="",
                route_steps=decision.route_steps,
                facility=decision.facility,
                crowd_level=decision.crowd_level,
                language=ctx.language,
                accessibility_mode=decision.accessibility_mode,
                alternatives_note=decision.alternatives_note,
                urgency=decision.urgency,
                used_llm=llm.is_live,
                incident_action_logged=decision.incident_id,
            )
            yield f"event: metadata\ndata: {initial_res.model_dump_json()}\n\n"

            full_text_chunks = []
            async for token in llm.phrase_stream(phrasing_ctx, ctx.question):
                full_text_chunks.append(token)
                escaped_token = token.replace("\n", "\\n")
                yield f"event: token\ndata: {escaped_token}\n\n"

            final_answer = "".join(full_text_chunks).strip()
            if not final_answer:  # pragma: no cover
                final_answer = phr.render_answer(phrasing_ctx)

            final_res = AssistResponse(
                answer=final_answer,
                route_steps=decision.route_steps,
                facility=decision.facility,
                crowd_level=decision.crowd_level,
                language=ctx.language,
                accessibility_mode=decision.accessibility_mode,
                alternatives_note=decision.alternatives_note,
                urgency=decision.urgency,
                used_llm=llm.is_live,
                incident_action_logged=decision.incident_id,
            )
            yield f"event: result\ndata: {final_res.model_dump_json()}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    @app.get("/api/incidents", tags=["incidents"])
    async def list_incidents() -> list[dict[str, Any]]:
        return [
            {
                "id": inc.id,
                "zone_id": inc.zone_id,
                "issue_type": inc.issue_type,
                "description": inc.description,
                "resolved": inc.resolved
            }
            for inc in get_incident_manager().get_all_incidents()
        ]

    @app.post("/api/incidents/{incident_id}/resolve", tags=["incidents"])
    async def resolve_incident(incident_id: str) -> dict[str, str]:
        success = get_incident_manager().resolve_incident(incident_id)
        if not success:
            raise HTTPException(status_code=404, detail="Incident not found")
        return {"status": "resolved"}

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        return FileResponse(_STATIC_DIR / "index.html")

    app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")

    return app


app = create_app()
