"""
agent.py
--------
Agente conversacional de IA usando LangChain + Gemini + Azure AI Search.

Modo actual:
- RAG con Azure AI Search.
- Gemini como modelo generativo.
- Memoria conversacional enviada desde FastAPI.
- Herramienta de simulación de escenarios.
- Herramienta de consulta de forecast por fecha.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

try:
    from .tools import simulate_material_change, get_forecast_by_date
except ImportError:
    from tools import simulate_material_change, get_forecast_by_date
load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_PATH = PROJECT_ROOT / "reports"

KNOWLEDGE_FILES = [
    "resumen_ejecutivo.md",
    "resultados_eda.md",
    "resultados_modelado.md",
    "resultados_forecasting.md",
    "preguntas_frecuentes.md",
]

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")


def get_knowledge_paths() -> List[Path]:
    return [REPORTS_PATH / file_name for file_name in KNOWLEDGE_FILES]


def validate_knowledge_files() -> Dict[str, object]:
    paths = get_knowledge_paths()

    existing = [str(path) for path in paths if path.exists()]
    missing = [str(path) for path in paths if not path.exists()]

    return {
        "existing": existing,
        "missing": missing,
        "all_available": len(missing) == 0,
    }


def load_knowledge_documents() -> str:
    validation = validate_knowledge_files()

    if not validation["all_available"]:
        missing = "\n".join(validation["missing"])
        raise FileNotFoundError(f"Faltan documentos para el agente:\n{missing}")

    contents = []

    for path in get_knowledge_paths():
        text = path.read_text(encoding="utf-8")
        contents.append(f"\n\n# Fuente local: {path.name}\n\n{text}")

    return "\n".join(contents)


def is_azure_search_configured() -> bool:
    return all(
        [
            AZURE_SEARCH_ENDPOINT,
            AZURE_SEARCH_KEY,
            AZURE_SEARCH_INDEX_NAME,
        ]
    )


def format_conversation_history(
    history: Optional[List[Dict[str, str]]] = None,
    max_messages: int = 8,
) -> str:
    if not history:
        return "No hay historial previo."

    recent_history = history[-max_messages:]
    formatted_messages = []

    for message in recent_history:
        role = message.get("role", "user")
        content = message.get("content", "")

        if not content:
            continue

        label = "Agente" if role == "assistant" else "Usuario"
        formatted_messages.append(f"{label}: {content}")

    return "\n".join(formatted_messages) if formatted_messages else "No hay historial previo."


def search_relevant_context(
    question: str,
    history: Optional[List[Dict[str, str]]] = None,
    top_k: int = 1,
) -> str:
    if not is_azure_search_configured():
        return load_knowledge_documents()

    search_query = question

    client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY),
    )

    results = client.search(
        search_text=search_query,
        top=top_k,
    )

    context_parts = []

    for result in results:
        score = result.get("@search.score", 0)

        if score < 3:
            continue

        print("\n====================")
        print("SCORE:", result.get("@search.score"))
        print("SOURCE:", result.get("source"))
        print("====================")

        source = result.get("source", "fuente_desconocida")
        category = result.get("category", "categoria_desconocida")
        content = result.get("content", "")

        if content:
            context_parts.append(
                f"""
Fuente: {source}
Categoría: {category}

{content}
"""
            )
    print(f"Resultados recuperados: {len(context_parts)}")

    if not context_parts:
        print("AZURE NO ENCONTRO RESULTADOS")
        return load_knowledge_documents()
    return "\n\n".join(context_parts)


def detect_scenario_question(question: str) -> Optional[Dict[str, object]]:
    question_lower = question.lower()

    material_match = re.search(r"price[_\s-]?(x|y|z)", question_lower)
    percent_match = re.search(r"(\d+(?:[.,]\d+)?)\s*%", question_lower)

    if not material_match or not percent_match:
        return None

    material_letter = material_match.group(1).upper()
    material = f"Price_{material_letter}"

    percent_change = float(percent_match.group(1).replace(",", "."))

    negative_words = [
        "baja",
        "bajar",
        "disminuye",
        "disminuir",
        "cae",
        "caer",
        "reduce",
        "reducir",
        "decrece",
    ]

    if any(word in question_lower for word in negative_words):
        percent_change = -percent_change

    if "equipo 1" in question_lower or "equipo1" in question_lower:
        target = "Price_Equipo1"
    elif "equipo 2" in question_lower or "equipo2" in question_lower:
        target = "Price_Equipo2"
    else:
        if material == "Price_Y":
            target = "Price_Equipo1"
        elif material == "Price_Z":
            target = "Price_Equipo2"
        else:
            target = "Price_Equipo2"

    return {
        "material": material,
        "percent_change": percent_change,
        "target": target,
    }


def build_scenario_context(question: str) -> str:
    scenario = detect_scenario_question(question)

    if not scenario:
        return ""

    simulation = simulate_material_change(
        material=scenario["material"],
        percent_change=scenario["percent_change"],
        target=scenario["target"],
    )

    return f"""
Resultado de simulación cuantitativa:

- Fecha base: {simulation["date"]}
- Materia prima analizada: {simulation["material"]}
- Equipo objetivo: {simulation["target"]}
- Cambio simulado en materia prima: {simulation["percent_change_material"]}%
- Precio actual de la materia prima: {simulation["current_material_price"]}
- Cambio absoluto en materia prima: {simulation["absolute_material_change"]}
- Coeficiente lineal usado: {simulation["coefficient"]}
- Precio actual del equipo: {simulation["current_target_price"]}
- Cambio estimado en el precio del equipo: {simulation["estimated_target_change"]}
- Nuevo precio estimado del equipo: {simulation["estimated_new_target_price"]}
- Variación estimada del equipo: {simulation["estimated_target_percent_change"]}%

Advertencia:
Este cálculo es una aproximación lineal basada en el modelo de regresión lineal.
No contempla shocks externos, inflación, TRM, contratos, proveedores, logística,
cambios regulatorios ni reentrenamiento del modelo.
"""


SPANISH_MONTHS = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "setiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}


def _parse_forecast_fecha(question_lower: str) -> Optional[str]:
    """Extrae una fecha en formatos ISO, numérico o texto en español."""
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", question_lower)
    if date_match:
        return date_match.group(1)

    date_match = re.search(
        r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})",
        question_lower,
    )
    if date_match:
        day = int(date_match.group(1))
        month = int(date_match.group(2))
        year = int(date_match.group(3))
        if year < 100:
            year += 2000
        return f"{year:04d}-{month:02d}-{day:02d}"

    months_pattern = "|".join(SPANISH_MONTHS.keys())

    date_match = re.search(
        rf"(\d{{1,2}})\s+de\s+({months_pattern})\s+de\s+(\d{{4}})",
        question_lower,
    )
    if date_match:
        day = int(date_match.group(1))
        month = SPANISH_MONTHS[date_match.group(2)]
        year = int(date_match.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"

    date_match = re.search(
        rf"({months_pattern})\s+(\d{{1,2}})(?:\s+de)?\s+(\d{{4}})",
        question_lower,
    )
    if date_match:
        month = SPANISH_MONTHS[date_match.group(1)]
        day = int(date_match.group(2))
        year = int(date_match.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"

    date_match = re.search(
        rf"(\d{{1,2}})\s+({months_pattern})\s+(\d{{4}})",
        question_lower,
    )
    if date_match:
        day = int(date_match.group(1))
        month = SPANISH_MONTHS[date_match.group(2)]
        year = int(date_match.group(3))
        return f"{year:04d}-{month:02d}-{day:02d}"

    return None


def _parse_forecast_equipo(question_lower: str) -> Optional[int]:
    if "equipo 1" in question_lower or "equipo1" in question_lower:
        return 1
    if "equipo 2" in question_lower or "equipo2" in question_lower:
        return 2
    return None


def detect_forecast_date_question(question: str) -> Optional[Dict[str, object]]:
    question_lower = question.lower()

    forecast_words = [
        "predicción",
        "prediccion",
        "forecast",
        "pronóstico",
        "pronostico",
        "proyección",
        "proyeccion",
        "estimado",
    ]

    if not any(word in question_lower for word in forecast_words):
        return None

    fecha = _parse_forecast_fecha(question_lower)
    equipo = _parse_forecast_equipo(question_lower)

    return {
        "equipo": equipo,
        "fecha": fecha,
    }

def get_risk_indicator(confidence_score: float) -> str:
    if confidence_score >= 80:
        return "Baja"

    if confidence_score >= 50:
        return "Media"

    if confidence_score >= 20:
        return "Alta"

    return "Muy Alta"


def build_forecast_context(question: str) -> str:
    forecast_request = detect_forecast_date_question(question)

    if not forecast_request:
        return ""

    equipo = forecast_request["equipo"]
    fecha = forecast_request["fecha"]

    if fecha and not equipo:
        return (
            "Puedo consultar el forecast, pero necesito saber "
            "si te refieres al Equipo 1 o al Equipo 2."
        )

    if equipo and not fecha:
        return "Necesito una fecha para consultar el forecast."

    if not fecha or not equipo:
        return ""

    forecast_result = get_forecast_by_date(
        equipo=equipo,
        fecha=fecha,
    )

    if forecast_result["type"] == "historical":
        return f"""
VALOR HISTÓRICO - EQUIPO {forecast_result["equipo"]}

Fecha consultada: {forecast_result["fecha"]}

Valor observado: {forecast_result["value"]:.2f}

Última fecha histórica disponible: {forecast_result["last_historical_date"]}

Interpretación:
La fecha consultada pertenece al histórico disponible. Por lo tanto, se reporta el valor real observado y no una predicción.
"""

    if forecast_result["type"] == "out_of_forecast_horizon":
        return f"""
FORECAST NO DISPONIBLE

Equipo consultado: Equipo {forecast_result["equipo"]}

Fecha consultada: {forecast_result["fecha"]}

Resultado:
{forecast_result["message"]}

Última fecha histórica: {forecast_result["last_historical_date"]}

Horizonte operativo disponible: {forecast_result["forecast_start_date"]} a {forecast_result["forecast_end_date"]}

Advertencia:
No se debe generar una predicción para esta fecha porque está fuera del horizonte operativo aprobado para el MVP.
"""

    if not forecast_result["found"]:
        return f"""
FORECAST NO DISPONIBLE

Equipo consultado: Equipo {equipo}

Fecha consultada: {fecha}

Resultado:
{forecast_result["message"]}
"""

    uncertainty_pct = forecast_result["uncertainty_pct"]
    confidence_score = max(0, 100 - uncertainty_pct)
    risk_indicator = get_risk_indicator(confidence_score)

    return f"""
FORECAST OPERATIVO - EQUIPO {forecast_result["equipo"]}

Fecha consultada: {forecast_result["fecha"]}

Modelo usado: {forecast_result["model"]}

Fuente: {forecast_result["source_file"]}

Última fecha histórica: {forecast_result["last_historical_date"]}

Días proyectados: {forecast_result["days_ahead"]}

Horizonte: {forecast_result["forecast_horizon"]}

Valor esperado: {forecast_result["forecast"]:.2f}

Rango probable:
- Mínimo: {forecast_result["lower_bound"]:.2f}
- Máximo: {forecast_result["upper_bound"]:.2f}

Confiabilidad estimada: {confidence_score:.2f}%

Nivel de incertidumbre: {forecast_result["uncertainty_level"]}

Nivel de riesgo: {risk_indicator}

Interpretación:
El valor esperado para la fecha consultada es {forecast_result["forecast"]:.2f}.

El resultado debe interpretarse como una estimación operativa y no como un valor exacto.
"""


def answer_with_local_context(
    question: str,
    history: Optional[List[Dict[str, str]]] = None,
) -> str:
    # =====================================================
    # RESPUESTA DIRECTA PARA FORECASTS
    # =====================================================

    forecast_context = build_forecast_context(question)

    if forecast_context:
        return forecast_context

    if not GOOGLE_API_KEY:
        raise ValueError("No se encontró GOOGLE_API_KEY. Configura tu archivo .env.")

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.prompts import ChatPromptTemplate
    except ImportError as exc:
        raise ImportError(f"Faltan dependencias de LangChain/Gemini: {exc}")

    context = search_relevant_context(
        question=question,
        history=history,
    )
    print("\n========== CONTEXTO ==========\n")
    print(context)
    print("\n==============================\n")

    scenario_context = build_scenario_context(question)

    if scenario_context:
        context = context + "\n\n" + scenario_context

    formatted_history = format_conversation_history(history)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
Eres un analista de negocio especializado en costos operativos de construcción.

El objetivo del agente no es repetir documentos, sino convertir los resultados del proyecto en información útil para la toma de decisiones. No eres un profesor: no expliques conceptos estadísticos ni técnicos salvo que el usuario los pida explícitamente.

Fuentes permitidas (usa solo estas, no inventes nada fuera de ellas):
1. El contexto recuperado desde Azure AI Search.
2. El historial reciente de conversación.
3. Los resultados cuantitativos de simulación de escenarios, cuando estén disponibles.
4. Los resultados de forecast por fecha (precalculado o dinámico), cuando estén disponibles.

Estructura de cada respuesta:
1. Si la pregunta es factual y la respuesta está completamente contenida en el contexto, responde únicamente con la información solicitada.
2. Solo añade interpretación de negocio cuando aporte información adicional útil para la toma de decisiones.
3. No añadas contexto, explicaciones ni comentarios cuando la respuesta ya sea suficiente por sí sola.

Para preguntas factuales simples:
- No agregues interpretación.
- No agregues explicación.
- No agregues relevancia.
- Responde únicamente el dato solicitado.

Ejemplos de preguntas factuales simples:
- ¿Cuántos registros se analizaron?
- ¿Cuál fue el periodo analizado?
- ¿Qué modelo se usó?
- ¿Cuál fue el MAPE?
- ¿Cuál fue el R²?

Reglas de interpretación:
4. Si existe una correlación o métrica, menciona únicamente su impacto en costos o en la toma de decisiones. No expliques qué es ni cómo se calcula.
5. Si existe un forecast, indica el valor esperado, el rango y el nivel de riesgo. Solo es válido dentro del horizonte ARIMA.
6. Si existe una simulación, describe la consecuencia operativa principal. Aclara que es una aproximación lineal.
7. Si la incertidumbre es Alta o Muy Alta, advierte brevemente que la predicción debe interpretarse con cautela.

Estilo:
8. Responde en español, con lenguaje claro, profesional y ejecutivo.
9. Sé conciso. Cuando la pregunta sea factual, dato + 2-3 oraciones es suficiente.
10. No conviertas cada respuesta en una explicación de estadística o machine learning.
11. Usa vocabulario de negocio, no de ciencia de datos. Prefiere frases como "apoya la planeación financiera", "facilita la toma de decisiones", "permite estimar costos futuros" o "reduce la incertidumbre presupuestal". Evita expresiones como "mayor granularidad", "identificación de patrones" o "mayor precisión" cuando el usuario no las pidió.
12. Evita expresiones académicas o de investigación: "representatividad de la muestra", "granularidad de los datos", "identificación de patrones", "análisis estadístico", "variabilidad observada", "significancia", "robustez metodológica". Usa en su lugar: "planeación financiera", "estimación de costos", "toma de decisiones", "control presupuestal", "gestión de riesgos", "seguimiento de costos", "proyecciones futuras".
13. Si la respuesta ya es suficientemente clara por sí sola, no añadas explicaciones adicionales. Para preguntas factuales simples (cantidad de registros, periodo analizado, modelo usado), una sola oración directa es la mejor respuesta.
14. No inventes escenarios adicionales ni texto que no aporte valor para decidir.
15. Prioriza la utilidad para gerentes, líderes financieros y responsables de planeación.
16. Si el usuario hace una pregunta corta ("¿por qué?", "¿cuál?", "¿y eso?"), interprétala usando el historial reciente.

Restricciones:
17. No inventes cifras ni información fuera de las fuentes permitidas.
18. Si la respuesta no está disponible, dilo claramente en una sola oración.
19. Cuando sea útil, menciona de qué fuente proviene la información.
                """,
            ),
            (
                "human",
                """
Contexto recuperado:
{context}

Historial reciente de la conversación:
{history}

Pregunta actual del usuario:
{question}
                """,
            ),
        ]
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.3,
        google_api_key=GOOGLE_API_KEY,
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "context": context,
            "history": formatted_history,
            "question": question,
        }
    )

    return response.content


def check_agent_ready() -> Dict[str, object]:
    validation = validate_knowledge_files()

    return {
        "knowledge_files_ready": validation["all_available"],
        "missing_files": validation["missing"],
        "google_key_available": bool(GOOGLE_API_KEY),
        "azure_search_configured": is_azure_search_configured(),
        "azure_search_index_name": AZURE_SEARCH_INDEX_NAME,
    }


if __name__ == "__main__":
    status = check_agent_ready()
    print("Estado del agente:")
    print(status)

    if not status["knowledge_files_ready"]:
        print("\nFaltan documentos. Revisa la carpeta reports/.")
    elif not status["google_key_available"]:
        print("\nFalta GOOGLE_API_KEY. Configura tu archivo .env.")
    else:
        print("\nAgente listo para prueba local.")
        question = input("Pregunta de prueba: ").strip()

        if question:
            answer = answer_with_local_context(question)
            print("\nRespuesta:")
            print(answer)
        else:
            print("\nNo se ingresó ninguna pregunta.")