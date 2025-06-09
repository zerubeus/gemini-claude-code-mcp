# sdk doc can be found at: https://googleapis.github.io/python-genai/
#
# Type annotations for Google Generative AI SDK:
# 1. generate_content() returns: types.GenerateContentResponse
# 2. generate_content_stream() returns: AsyncIterator[types.GenerateContentResponse]
# 3. GenerateContentResponse.text is a property that returns Optional[str]
#    - It concatenates all text parts in the response
#    - Returns None if there's no text content
# 4. Each chunk in the stream is also a GenerateContentResponse object

import asyncio
import time
from collections.abc import AsyncGenerator

from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from gemini_claude_code_mcp.config.settings import settings
from gemini_claude_code_mcp.utils.logging import get_logger

logger = get_logger(__name__)

gemini_client = genai.Client(api_key=settings.gemini.api_key)

# Rate limiting state
rate_limit_state: dict[str, int | float | asyncio.Lock] = {
    'request_count': 0,
    'window_start': time.time(),
    'lock': asyncio.Lock(),
}


async def check_rate_limit() -> None:
    """Check and enforce rate limiting."""
    lock = rate_limit_state['lock']
    assert isinstance(lock, asyncio.Lock)

    async with lock:
        current_time = time.time()
        window_start = rate_limit_state['window_start']
        assert isinstance(window_start, (int, float))
        window_elapsed = current_time - window_start

        if window_elapsed >= settings.rate_limit_window:
            # Reset the window
            rate_limit_state['request_count'] = 0
            rate_limit_state['window_start'] = current_time

        request_count = rate_limit_state['request_count']
        assert isinstance(request_count, int)

        if request_count >= settings.rate_limit_requests:
            # Calculate wait time
            wait_time = settings.rate_limit_window - window_elapsed
            logger.warning(f'Rate limit reached, waiting {wait_time:.2f} seconds')
            await asyncio.sleep(wait_time)
            # Reset after waiting
            rate_limit_state['request_count'] = 0
            rate_limit_state['window_start'] = time.time()

        rate_limit_state['request_count'] = request_count + 1


async def gemini_text_to_text(
    prompt: str,
    system_instruction: list[str] | None = None,
    model: str = settings.gemini.model,
    temperature: float = settings.gemini.temperature,
    max_output_tokens: int = settings.gemini.max_output_tokens,
    max_retries: int = 3,
    initial_retry_delay: float = 1.0,
) -> str | None:
    """Generate text using Gemini's text-to-text model with retry logic."""
    contents = [types.Content(role='user', parts=[types.Part.from_text(text=prompt)])]

    generate_content_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        response_mime_type='text/plain',
    )

    retry_delay = initial_retry_delay
    last_error = None

    for attempt in range(max_retries):
        try:
            # Check rate limit before making request
            await check_rate_limit()

            logger.debug(f'Attempting Gemini API call (attempt {attempt + 1}/{max_retries})')

            response = await gemini_client.aio.models.generate_content(  # type: ignore[attr-defined]
                model=model,
                contents=contents,
                config=generate_content_config,
            )

            logger.debug('Gemini API call successful')
            # response.text is Optional[str] - returns None if no text content
            return response.text

        except ServerError as e:
            last_error = e
            # Check if this is a rate limit error (usually 429 status code)
            if 'rate' in str(e).lower() or '429' in str(e):
                logger.warning(f'Rate limit error from Gemini API: {e}')
                # Use exponential backoff with jitter
                wait_time = retry_delay * (2**attempt) + (0.1 * time.time() % 1)
                await asyncio.sleep(wait_time)
            else:
                logger.error(f'Server error from Gemini API: {e}')
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (2**attempt))

        except ClientError as e:
            logger.error(f'Client error from Gemini API: {e}')
            # Don't retry on client errors
            raise

        except Exception as e:
            last_error = e
            logger.error(f'Unexpected error from Gemini API: {e}')
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)

    logger.error(f'Failed after {max_retries} attempts. Last error: {last_error}')
    return None


async def gemini_text_to_text_stream(
    prompt: str,
    system_instruction: list[str] | None = None,
    model: str = settings.gemini.model,
    temperature: float = settings.gemini.temperature,
    max_output_tokens: int = settings.gemini.max_output_tokens,
    max_retries: int = 3,
    initial_retry_delay: float = 1.0,
) -> AsyncGenerator[str, None]:
    """Generate text using Gemini's text-to-text model with streaming support."""
    contents = [types.Content(role='user', parts=[types.Part.from_text(text=prompt)])]

    generate_content_config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        response_mime_type='text/plain',
    )

    retry_delay = initial_retry_delay
    last_error = None

    for attempt in range(max_retries):
        try:
            # Check rate limit before making request
            await check_rate_limit()

            logger.debug(f'Attempting Gemini streaming API call (attempt {attempt + 1}/{max_retries})')

            # Each chunk is a GenerateContentResponse object
            # generate_content_stream returns AsyncIterator[GenerateContentResponse]
            async for chunk in gemini_client.aio.models.generate_content_stream(  # type: ignore[attr-defined]
                model=model,
                contents=contents,
                config=generate_content_config,
            ):
                # chunk.text is Optional[str] - only yield if it has content
                if chunk.text:  # type: ignore[attr-defined]
                    yield chunk.text  # type: ignore[misc]

            logger.debug('Gemini streaming API call completed')
            return

        except ServerError as e:
            last_error = e
            # Check if this is a rate limit error (usually 429 status code)
            if 'rate' in str(e).lower() or '429' in str(e):
                logger.warning(f'Rate limit error from Gemini API: {e}')
                wait_time = retry_delay * (2**attempt) + (0.1 * time.time() % 1)
                await asyncio.sleep(wait_time)
            else:
                logger.error(f'Server error from Gemini API: {e}')
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (2**attempt))

        except ClientError as e:
            logger.error(f'Client error from Gemini API: {e}')
            raise

        except Exception as e:
            last_error = e
            logger.error(f'Unexpected error from Gemini API: {e}')
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)

    logger.error(f'Streaming failed after {max_retries} attempts. Last error: {last_error}')
