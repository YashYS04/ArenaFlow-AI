# ArenaFlow AI ⚽

**A smart, multilingual, accessible stadium wayfinding & operations assistant for the FIFA World Cup 2026.**

ArenaFlow helps fans navigate MetLife Stadium (New York New Jersey Stadium), find step-free facilities, and receive real-time crowd warnings. It also provides venue staff and volunteers with incident logging and operational dispatch support. All answers are strictly grounded in verified stadium data, eliminating LLM hallucinations.

🌐 **Vercel Serverless Live Deployment:** Deployed at your Vercel URL (see [Deployment](#deployment)).

---

## Table of Contents
1. [Chosen Vertical & Persona](#1-chosen-vertical--persona)
2. [Approach & Logic](#2-approach--logic)
3. [Features & Innovations](#3-features--innovations)
4. [Tech Stack & Architecture](#4-tech-stack--architecture)
5. [Environment Configuration](#5-environment-configuration)
6. [Local Development](#6-local-development)
7. [Deployment](#7-deployment)
8. [Quality Attributes](#8-quality-attributes)
   - [Security](#security)
   - [Efficiency](#efficiency)
   - [Accessibility](#accessibility)
   - [Testing](#testing)

---

## 1. Chosen Vertical & Persona

*   **Persona:** Dual Persona (Fans + Venue Staff/Volunteers)
*   **Vertical:** Wayfinding + Accessibility + Multilingual Assistance + Operations Support
*   **Product:** *ArenaFlow AI* — A conversational wayfinding dashboard that computes step-free paths, dynamically routes around crowd surges, and provides volunteers with a stateful incident logger to route dispatch recommendations and bypass blocked hazard zones.

---

## 2. Approach & Logic — *Rules Before GenAI*

ArenaFlow operates on the core design principle of **deterministic rules first, language model last**:

```
UserContext ─▶ Rules Engine (Deterministic) ─▶ Resolved Facts ─▶ Streaming LLM ─▶ SSE Output
               • Find target facility         • Route step nodes  • Rephrase facts    • Types tokens
               • Step-free Dijkstra graph     • Simulated crowd   • Treat text as data• Screen reader
               • Dynamic crowd scaling        • Active blocks     • Localize prose    • Voice guidance
               • Incident block resolver      • Dispatch target                       • SVG highlight
```

1.  **Rules Engine (`context_engine.py`):** Resolves target facilities, computes pathfinding over the zone graph using Dijkstra, adjusts node costs based on simulated crowd levels, filters edges based on step-free needs, and applies blocks on zones with active hazards (like spills). No LLM is involved in routing decisions.
2.  **Generative AI Phrasing (`llm.py`):** The LLM receives only the resolved facts and system constraints. It is strictly prohibited from inventing facilities or executing instructions found in the user question (prompt-injection mitigation).
3.  **Short-Circuiting:** If no text question is asked, ArenaFlow skips the LLM entirely, serving a localized template answer instantly at zero cost and zero network call delay.

### Dynamic Operations & Route Weighting Rules
*   **Accessibility Mode:** Visual/wheelchair needs restrict paths to step-free edges (ramps/elevators) and completely exclude stairs. Low-vision mode enables landmark-based directions.
*   **Dynamic Crowd Routing:** Concourses and gates surge near kickoff. If a zone crowd level is `medium`, its traversal weight is multiplied by `1.5x`; if `high`, it is multiplied by `3.0x`. Dijkstra bypasses crowded areas automatically in favor of quieter paths.
*   **Incident Blocks:** Spills, medical emergencies, or maintenance hazards logged by staff immediately block their respective zones in the routing graph. Fans are automatically rerouted around the hazard.
*   **Facility Swaps:** If a fan heads to a restroom, concession, or water fountain that is highly concurrido, the rules engine automatically swaps their destination to the nearest quiet equivalent.

---

## 3. Features & Innovations

*   **Interactive SVG Stadium Map:** A lightweight vector map of MetLife Stadium. Clicking zones selects them in the form. It dynamically highlights the start/end points and draws the computed route paths and edges in real-time.
*   **SSE streaming (Server-Sent Events):** Typing effect is generated token-by-token for LLM phrasing, enhancing UX responsiveness.
*   **Text-to-Speech (TTS) Voice Guidance:** Utilizes the Web Speech API to read route directions aloud. Works offline and is fully localized.
*   **Stateful Staff Panel:** Toggle to Staff Mode to report issues. Active spills or hazards block zones, showing up as striped red areas on the SVG map, and automatically steer fan route calculations away from them.

---

## 4. Tech Stack & Architecture

*   **Backend:** Python 3.11+ / FastAPI. Fast, asynchronous event-loops, CORS middleware, and custom security middlewares.
*   **Frontend:** Vanilla HTML5, Vanilla CSS3 (glassmorphic theme), and Vanilla JS. Lightweight, responsive, zero build step, ensuring the repo size remains **under 10 MB**.
*   **API Documentation:** FastAPI automatically generates interactive Swagger API docs, available at `/docs` or `/redoc` when running locally.

---

## 5. Environment Configuration

ArenaFlow runs out-of-the-box without any environment variables by falling back to the offline `MockLLM` template. To enable live Gemini responses, configure the following keys:

| Variable | Purpose | Default |
|----------|---------|---------|
| `GEMINI_API_KEY` | Live Google Gemini API Key | *(unset, falls back to MockLLM)* |
| `GEMINI_MODEL` | Gemini model ID | `gemini-1.5-flash` |
| `GEMINI_MAX_OUTPUT_TOKENS` | Maximum response length | `256` |
| `ALLOWED_ORIGINS` | JSON array of CORS origins | `["http://localhost:8000", "http://127.0.0.1:8000"]` |
| `RATE_LIMIT_CAPACITY` | Token-bucket max request burst capacity | `30` |
| `RATE_LIMIT_REFILL_PER_SEC` | Token-bucket refill rate per second | `0.5` |

---

## 6. Local Development

### Prerequisites
*   Python 3.11 or higher
*   Git

### Installation
1.  **Clone the repository:**
    ```bash
    git clone <your-repo-link>
    cd promtwars
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    # Windows:
    .venv\Scripts\activate
    # macOS/Linux:
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Create a `.env` file:**
    Copy `.env.example` to `.env` and fill in your `GEMINI_API_KEY`.
5.  **Run the local server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser. Interactive API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 7. Deployment

### Deployment to Vercel (No Cost)
Vercel supports serverless python functions using `@vercel/python`. The repository includes a pre-configured `vercel.json` and a bridge file `api/main.py` routing traffic to our app.

1.  **Install Vercel CLI:**
    ```bash
    npm install -g vercel
    ```
2.  **Deploy from workspace:**
    Run the command from the root of the repository:
    ```bash
    vercel
    ```
    Follow the prompt instructions (default choices are recommended).
3.  **Add environment variables:**
    Go to your Vercel Dashboard -> project settings -> Environment Variables. Add `GEMINI_API_KEY` with your API key.
4.  **Deploy to production:**
    ```bash
    vercel --prod
    ```

### Deployment to Google Cloud Run (Docker)
A `Dockerfile` and `.dockerignore` are provided to compile a container image.
```bash
docker build -t arenaflow .
docker run -p 8080:8080 -e GEMINI_API_KEY=YOUR_KEY arenaflow
```

---

## 8. Quality Attributes

### 🔐 Security
*   **Zero Hardcoded Secrets:** Configuration variables are read from the environment only. If no key is set, the app degrades gracefully to MockLLM fallback without throwing errors or crashing.
*   **Prompt-Injection Defense:** Free-text is sanitised (HTML entities escaped, control characters stripped), wrapped inside XML tags, and routing Dijkstra is executed *prior* to LLM calls.
*   **Headers Middlewares:** Appends security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, and a strict `Content-Security-Policy`.
*   **IP-Based Rate Limiting:** A thread-safe, in-memory token-bucket limiter limits excessive requests per IP, returning `429` status codes with a `Retry-After` header.

### ⚡ Efficiency
*   **Startup-Time Parsing:** Stadium JSON data is read once at startup andcached.
*   **LRU Caching:** Phrase rendering and Dijkstra routes calculations are memoized using `lru_cache`.
*   **SSE Streaming:** Reduces Time-to-First-Token (TTFT) by streaming responses.
*   **Short-Circuiting:** Skips LLM calls entirely for standard wayfinding queries without free-text questions.

### ♿ Accessibility
*   **WCAG 2.2 AA compliant:** Standard semantic HTML5 structural layout, focus visible outlines, and screen-reader `aria-live` polite announcers.
*   **Skip Link:** A focusable skip-to-content link is present.
*   **High-Contrast Mode:** Toggles a pure black-and-yellow layout style.
*   **Voice Guidance:** Client-side speech synthesis reads routes.
*   **Localization:** Localized UI controls and speech voices for EN, ES, and FR.
*   **Axe-Core Audit:** AXE-Core 4.10 audits pass with **0 violations**.

### 🧪 Testing
*   The test suite achieves **100.00% statement coverage** across all Python code modules.
*   Run the offline test suite using:
    ```bash
    pytest
    ```
