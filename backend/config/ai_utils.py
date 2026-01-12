import os

from google import genai
from google.genai import types

# Configuration
api_key = os.environ.get("GEMINI_API_KEY")

# List of models to try sequentially
# We start with the most recent stable Flash model
MODEL_CANDIDATES = [
    'gemini-2.5-flash',
    'gemini-1.5-flash-001',
    'gemini-1.5-flash-002',
    'gemini-1.5-flash-8b',
    'gemini-pro'  # Fallback to version 1.0
]


def get_ai_response(prompt_text):
    """
    Generates a response from the AI model based on the provided prompt text.

    Iterates through a list of candidate models and returns the response from the
    first successful one.

    Args:
        prompt_text (str): The input text prompt for the AI model.

    Returns:
        str: The text response from the AI model, or an error message if all
             attempts fail or if the API key is missing.
    """
    if not api_key:
        return "Kein API Key konfiguriert."

    try:
        client = genai.Client(api_key=api_key)

        last_error = None

        # Try the models one by one
        for model_name in MODEL_CANDIDATES:
            try:
                # Attempt to retrieve the model
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt_text
                )

                # If we are here, it worked!
                print(f"Erfolg mit Modell: {model_name}")
                return response.text

            except Exception as e:
                # Save error and continue with the next model
                print(f"Modell {model_name} fehlgeschlagen: {e}")
                last_error = e
                continue

        # If nothing worked:
        return f"Entschuldigung, keines der KI-Modelle war erreichbar. Letzter Fehler: {str(last_error)}"

    except Exception as e:
        return f"Genereller Fehler bei der KI-Anfrage: {str(e)}"
