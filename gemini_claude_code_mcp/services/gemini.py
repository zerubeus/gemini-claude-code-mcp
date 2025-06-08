from google import genai


def get_gemini_client():
    """Create and return a Google Gemini API client."""
    return genai.Client(api_key=settings.gemini.api_key)
