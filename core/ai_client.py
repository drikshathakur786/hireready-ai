import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_last_error = None
_active_model = None   # cached after first successful call


def get_last_error():
    global _last_error
    return _last_error


def set_last_error(msg):
    global _last_error
    _last_error = msg


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


def _model_priority(model_id):
    """Rank models so best English text generation models are tried first."""
    mid = model_id.lower()
    if "llama-4" in mid or "llama-3.3" in mid:
        return 0
    if "gpt-oss-120b" in mid:
        return 1
    if "gpt-oss-20b" in mid:
        return 2
    if "llama-3.1" in mid or "llama3" in mid:
        return 3
    if "qwen" in mid:
        return 4
    if "mixtral" in mid or "mistral" in mid:
        return 5
    if "gemma" in mid:
        return 6
    return 10


def _get_available_models(groq_client):
    """
    Ask Groq which text-generation models this API key can actually use.
    Filters out non-English / audio / safeguard models and sorts by preference.
    """
    hardcoded = [
        "meta-llama/llama-4-scout-17b-16e-instruct",
        "openai/gpt-oss-120b",
        "openai/gpt-oss-20b",
        "qwen/qwen3.8-27b",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]

    # Exclude non-English, audio, vision, or safety moderation models
    excluded = ["whisper", "tts", "speech", "guard", "safeguard", "allam", "orpheus", "vision"]

    try:
        models_page = groq_client.models.list()
        text_models = [
            m.id for m in models_page.data
            if not any(skip in m.id.lower() for skip in excluded)
        ]
        if text_models:
            # Sort models by preferred English reasoning capabilities
            text_models.sort(key=_model_priority)
            print(f"INFO: Groq reports available text models: {text_models}")
            combined = text_models + [m for m in hardcoded if m not in text_models]
            return combined
    except Exception as e:
        print(f"WARNING: Could not fetch model list from Groq: {e}. Using fallback list.")

    return hardcoded


def call_claude(prompt, max_tokens=1024):
    global _last_error, _active_model

    active_client = get_client()
    if active_client is None:
        print("ERROR: Groq client is not set up. Check your .env file or Streamlit secrets.")
        return None

    # Cap max_tokens to 1800 to avoid tripping Groq's 6,000 TPM limit on free tier
    capped_tokens = min(max_tokens, 1800)

    # Get models to try
    models_to_try = _get_available_models(active_client)
    if _active_model and _active_model in models_to_try:
        # Try previously working model first
        models_to_try = [_active_model] + [m for m in models_to_try if m != _active_model]

    for model_name in models_to_try:
        try:
            response = active_client.chat.completions.create(
                model=model_name,
                max_tokens=capped_tokens,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            _active_model = model_name
            print(f"INFO: Successfully used model: {model_name}")
            return response.choices[0].message.content

        except Exception as e:
            err_msg = str(e)
            _last_error = err_msg

            # Fall back on model unavailability OR rate limit (429 TPM / RPM)
            is_recoverable = any(kw in err_msg.lower() for kw in [
                "model_not_found", "does not exist", "404",
                "do not have access", "invalid_request_error",
                "decommissioned", "deprecated", "not supported",
                "403", "429", "rate limit", "rate_limit", "tokens per minute"
            ])

            if is_recoverable:
                print(f"WARNING: Model '{model_name}' hit issue ({err_msg}). Trying fallback model...")
                if _active_model == model_name:
                    _active_model = None
                continue

            print(f"ERROR: Groq call failed on {model_name}: {e}")
            return None

    _last_error = "Groq rate limit or capacity reached across available models. Please wait a few seconds and try again."
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
