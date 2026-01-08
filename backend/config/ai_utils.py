from google import genai
from google.genai import types
import os

# Konfiguration
api_key = os.environ.get("GEMINI_API_KEY")

# Liste der Modelle, die wir nacheinander probieren
# Wir starten mit dem aktuellsten stabilen Flash-Modell
MODEL_CANDIDATES = [
    'gemini-2.5-flash',
    'gemini-1.5-flash-001',
    'gemini-1.5-flash-002',
    'gemini-1.5-flash-8b',
    'gemini-pro'  # Fallback auf Version 1.0
]


def get_ai_response(prompt_text):
    if not api_key:
        return "Kein API Key konfiguriert."

    try:
        client = genai.Client(api_key=api_key)

        last_error = None

        # Wir probieren die Modelle der Reihe nach durch
        for model_name in MODEL_CANDIDATES:
            try:
                # Versuch, das Modell abzurufen
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt_text
                )

                # Wenn wir hier sind, hat es geklappt!
                print(f"Erfolg mit Modell: {model_name}")
                return response.text

            except Exception as e:
                # Fehler speichern und mit dem nächsten Modell weitermachen
                print(f"Modell {model_name} fehlgeschlagen: {e}")
                last_error = e
                continue

        # Wenn gar nichts geklappt hat:
        return f"Entschuldigung, keines der KI-Modelle war erreichbar. Letzter Fehler: {str(last_error)}"

    except Exception as e:
        return f"Genereller Fehler bei der KI-Anfrage: {str(e)}"