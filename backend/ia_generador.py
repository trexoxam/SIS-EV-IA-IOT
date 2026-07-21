from google import genai
import json

# Coloca tu API Key
client = genai.Client(
    api_key="AQ.Ab8RN6KDuEIyevQiNvYaMZX9vGfotwBmV3dEPoQrngN4-8MZEw"
)

def generar_pregunta(nombre_examen, tema):

    prompt = f"""
Eres un experto creando exámenes de admisión.

Genera UNA pregunta de opción múltiple para el examen:

Nombre del examen:
{nombre_examen}

Tema:
{tema}

Reglas:

- Debe tener exactamente cuatro opciones.
- Solo una respuesta correcta.
- Las opciones deben ser creíbles.
- No agregues explicaciones.
- Devuelve únicamente un JSON.

Formato:

{{
"pregunta":"",
"opcion_a":"",
"opcion_b":"",
"opcion_c":"",
"opcion_d":"",
"respuesta_correcta":"A"
}}
"""

    respuesta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    texto = respuesta.text.strip()

    # Si Gemini devuelve ```json ... ```
    if texto.startswith("```"):
        texto = texto.replace("```json", "").replace("```", "").strip()

    return json.loads(texto)