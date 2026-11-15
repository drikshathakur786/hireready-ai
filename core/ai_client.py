import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_last_error = None
_active_model = None   # cached after first successful call


def get_last_error():
    global _last_error
    return _last_error


def get_api_key():
    # 1. Check local environment / .env
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key.strip()

    # 2. Check Streamlit Cloud secrets (or .streamlit/secrets.toml)
    try:
        import streamlit as st  # type: ignore
        if hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
            return str(st.secrets["GROQ_API_KEY"]).strip()
    except Exception:
        pass

    return None


def get_client():
    global _last_error
    api_key = get_api_key()
    if not api_key:
        _last_error = "GROQ_API_KEY is not set. Please add it to your .env file or Streamlit Cloud Secrets."
        print(f"WARNING: {_last_error}")
        return None

    try:
        return Groq(api_key=api_key)
    except Exception as e:
        _last_error = f"Failed to initialize Groq client: {e}"
        print(f"ERROR: {_last_error}")
        return None


# Module-level client instance (for backwards compatibility)
client = get_client()


def _get_available_models(groq_client):
    """
    Ask Groq which text-generation models this API key can actually use.
    Returns a list of model IDs sorted by context window size (larger = better).
    Falls back to a hardcoded list if the models endpoint fails.
    """
    # Hardcoded fallback — covers both old and new Groq model IDs
    hardcoded = [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "qwen/qwen3.8-27b",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "llama3-70b-8192",
        "llama3-8b-8192",
    ]

    try:
        models_page = groq_client.models.list()
        # Filter to text models (exclude whisper / tts)
        text_models = [
            m.id for m in models_page.data
            if not any(skip in m.id.lower() for skip in ["whisper", "tts", "speech", "guard", "safeguard"])
        ]
        if text_models:
            print(f"INFO: Groq reports {len(text_models)} available text models: {text_models}")
            # Put discovered models first, then any hardcoded extras as fallback
            combined = text_models + [m for m in hardcoded if m not in text_models]
            return combined
    except Exception as e:
        print(f"WARNING: Could not fetch model list from Groq: {e}. Using hardcoded list.")

    return hardcoded


def call_claude(prompt, max_tokens=1024):
    global _last_error, _active_model

    active_client = get_client()
    if active_client is None:
        print("ERROR: Groq client is not set up. Check your .env file or Streamlit secrets.")
        return None

    # If we already know a working model, try it first
    models_to_try = []
    if _active_model:
        models_to_try = [_active_model]
    else:
        models_to_try = _get_available_models(active_client)

    for model_name in models_to_try:
        try:
            response = active_client.chat.completions.create(
                model=model_name,
                max_tokens=max_tokens,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            # Cache the working model so future calls skip discovery
            _active_model = model_name
            print(f"INFO: Using model: {model_name}")
            return response.choices[0].message.content

        except Exception as e:
            err_msg = str(e)
            _last_error = err_msg
            # Any availability / access error → try next model
            if any(kw in err_msg for kw in [
                "model_not_found", "does not exist", "404",
                "do not have access", "invalid_request_error",
                "decommissioned", "deprecated", "not supported",
                "403",
            ]):
                print(f"WARNING: Model '{model_name}' unavailable — trying next...")
                # Reset cached model so we re-discover on next call
                if _active_model == model_name:
                    _active_model = None
                continue

            # Non-availability error (rate limit, auth, etc.) — stop immediately
            print(f"ERROR: Groq call failed ({model_name}): {e}")
            return None

    _last_error = "No working Groq model found. All candidates were unavailable for this API key."
    print(f"ERROR: {_last_error}")
    return None


if __name__ == "__main__":
    print("Testing Groq connection...")
    response = call_claude("Say hello and tell me today's date. Reply in one sentence.")

    if response:
        print("SUCCESS! Groq says:")
        print(response)
    else:
        print("FAILED — check the error message above.")
        if _last_error:
            print(f"Reason: {_last_error}")
