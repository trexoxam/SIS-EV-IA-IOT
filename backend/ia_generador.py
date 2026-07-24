from google import genai
import json
import os


# API Key
client = genai.Client(
    api_key=os.getenv("AQ.Ab8RN6KDuEIyevQiNvYaMZX9vGfotwBmV3dEPoQrngN4-8MZEw")
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

    if texto.startswith("```"):
        texto = texto.replace("```json", "").replace("```", "").strip()

    return json.loads(texto)


def generar_examen(nombre_puesto):

    prompt = f"""
Eres un experto creando exámenes técnicos.

Genera exactamente 10 preguntas de opción múltiple
para el siguiente puesto:

Puesto:
{nombre_puesto}

Reglas:

- Genera exactamente 10 preguntas.
- Cada pregunta debe tener exactamente cuatro opciones.
- Solo una respuesta debe ser correcta.
- Las preguntas deben estar relacionadas con el puesto.
- Las opciones deben ser creíbles.
- No agregues explicaciones.
- Devuelve únicamente un JSON válido.
- La respuesta_correcta debe ser únicamente A, B, C o D.

Formato:

[
    {{
        "pregunta": "",
        "opcion_a": "",
        "opcion_b": "",
        "opcion_c": "",
        "opcion_d": "",
        "respuesta_correcta": "A"
    }}
]
"""

    respuesta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    texto = respuesta.text.strip()

    # Limpiar bloques Markdown
    if texto.startswith("```json"):
        texto = texto.replace("```json", "", 1)

    if texto.startswith("```"):
        texto = texto.replace("```", "", 1)

    if texto.endswith("```"):
        texto = texto[:-3]

    texto = texto.strip()

    return json.loads(texto)