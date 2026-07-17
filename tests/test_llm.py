from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch

from app.config import Settings
from app.services.llm import MockLLM, get_llm_client, GeminiClient
from app.services.phrasing import PhrasingContext


@pytest.fixture
def phrasing_ctx() -> PhrasingContext:
    return PhrasingContext(
        language="en",
        facility_name="Gate A",
        facility_type="gate",
        facility_landmark=None,
        crowd_level="low",
        accessibility_mode="standard",
        landmark_based=False,
        hurry=False,
        alternative_type=None,
        total_distance=0,
        step_count=0,
    )


@pytest.mark.asyncio
async def test_mock_llm_sync_and_stream(phrasing_ctx):
    client = MockLLM()
    assert client.is_live is False

    ans = await client.phrase(phrasing_ctx, "Question?")
    assert "Your destination is Gate A" in ans

    # Stream output
    tokens = []
    async for token in client.phrase_stream(phrasing_ctx, "Question?"):
        tokens.append(token)
    assert "".join(tokens) == ans


def test_get_llm_client_fallback_when_disabled():
    settings = Settings(gemini_api_key=None)
    client = get_llm_client(settings)
    assert isinstance(client, MockLLM)


@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_get_llm_client_live_initialization(mock_model, mock_configure):
    settings = Settings(gemini_api_key="valid_test_key")
    client = get_llm_client(settings)
    assert isinstance(client, GeminiClient)
    assert client.is_live is True
    mock_configure.assert_called_once_with(api_key="valid_test_key")


@pytest.mark.asyncio
@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
async def test_gemini_client_phrase_success(mock_model_class, mock_configure, phrasing_ctx):
    mock_model = MagicMock()
    mock_model.generate_content.return_value.text = "Answer from Gemini"
    mock_model_class.return_value = mock_model

    settings = Settings(gemini_api_key="test_key")
    client = GeminiClient(settings)
    
    ans = await client.phrase(phrasing_ctx, "What's the route?")
    assert ans == "Answer from Gemini"


@pytest.mark.asyncio
@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
async def test_gemini_client_phrase_failure_fallback(mock_model_class, mock_configure, phrasing_ctx):
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("API error")
    mock_model_class.return_value = mock_model

    settings = Settings(gemini_api_key="test_key")
    client = GeminiClient(settings)

    # Should degrade gracefully to template rendering
    ans = await client.phrase(phrasing_ctx, "What's the route?")
    assert "Your destination is Gate A" in ans


@pytest.mark.asyncio
@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
async def test_gemini_client_stream_success(mock_model_class, mock_configure, phrasing_ctx):
    mock_model = MagicMock()
    
    async def mock_generate_content_async(*args, **kwargs):
        async def async_generator():
            chunk1 = MagicMock()
            chunk1.text = "Chunk"
            yield chunk1
            chunk2 = MagicMock()
            chunk2.text = " 1"
            yield chunk2
        return async_generator()
        
    mock_model.generate_content_async.side_effect = mock_generate_content_async
    mock_model_class.return_value = mock_model

    settings = Settings(gemini_api_key="test_key")
    client = GeminiClient(settings)

    tokens = []
    async for token in client.phrase_stream(phrasing_ctx, "Any help?"):
        tokens.append(token)
    assert "".join(tokens) == "Chunk 1"


@patch("google.generativeai.configure")
@patch("google.generativeai.GenerativeModel")
def test_gemini_client_staff_persona(mock_model_class, mock_configure):
    mock_model = MagicMock()
    mock_model_class.return_value = mock_model

    settings = Settings(gemini_api_key="test_key")
    client = GeminiClient(settings)

    staff_ctx = PhrasingContext(
        language="en",
        facility_name="Gate A",
        facility_type="gate",
        facility_landmark=None,
        crowd_level="low",
        accessibility_mode="standard",
        landmark_based=False,
        hurry=False,
        alternative_type=None,
        total_distance=0,
        step_count=0,
        persona="staff",
        incident_id="inc_123",
        incident_type="spill",
        incident_desc="drink spill"
    )

    facts = client._build_facts(staff_ctx)
    assert "persona: staff" in facts
    assert "incident_id: inc_123" in facts
    assert "incident_type: spill" in facts
    assert "incident_description: drink spill" in facts
