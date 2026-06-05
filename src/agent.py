"""
agent.py
--------
Agente conversacional de IA usando LangChain + Gemini + Azure AI Search.

Este módulo será la capa lógica del agente. Su objetivo es responder preguntas
sobre el proyecto de costos operativos usando documentos internos del análisis.

Modo actual:
- Prueba local usando Gemini y los documentos Markdown completos.

Modo futuro:
- Recuperación semántica usando Azure AI Search.
- Exposición mediante FastAPI.

Documentos fuente:
- reports/resumen_ejecutivo.md
- reports/resultados_eda.md
- reports/resultados_modelado.md
- reports/resultados_forecasting.md
- reports/preguntas_frecuentes.md
"""

import os
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv

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
    """
    Retorna las rutas de los documentos que alimentarán el agente.
    """
    return [REPORTS_PATH / file_name for file_name in KNOWLEDGE_FILES]


def validate_knowledge_files() -> Dict[str, object]:
    """
    Verifica que todos los documentos base existan.
    """
    paths = get_knowledge_paths()

    existing = [str(path) for path in paths if path.exists()]
    missing = [str(path) for path in paths if not path.exists()]

    return {
        "existing": existing,
        "missing": missing,
        "all_available": len(missing) == 0,
    }


def load_knowledge_documents() -> str:
    """
    Carga el contenido de los documentos base en texto plano.

    Esta función permite probar el agente localmente antes de conectar
    Azure AI Search.
    """
    validation = validate_knowledge_files()

    if not validation["all_available"]:
        missing = "\n".join(validation["missing"])
        raise FileNotFoundError(
            f"Faltan documentos para el agente:\n{missing}"
        )

    contents = []

    for path in get_knowledge_paths():
        text = path.read_text(encoding="utf-8")
        contents.append(f"\n\n# Fuente: {path.name}\n\n{text}")

    return "\n".join(contents)


def answer_with_local_context(question: str) -> str:
    """
    Versión temporal sin Azure AI Search.

    Usa los documentos cargados localmente como contexto completo.
    Sirve para validar que la base documental del agente está bien construida.

    En el siguiente paso esta lógica será reemplazada por recuperación
    semántica usando Azure AI Search.
    """
    if not GOOGLE_API_KEY:
        raise ValueError(
            "No se encontró GOOGLE_API_KEY. Configura tu archivo .env."
        )

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.prompts import ChatPromptTemplate
    except ImportError as exc:
        raise ImportError(
            f"Faltan dependencias de LangChain/Gemini: {exc}"
        )

    context = load_knowledge_documents()

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
Eres un agente de IA especializado en el proyecto de costos operativos de construcción.

Tu tarea es responder preguntas usando únicamente el contexto proporcionado.

Reglas:
1. No inventes cifras.
2. Si la respuesta no está en el contexto, dilo claramente.
3. Responde en español.
4. Usa lenguaje claro, profesional y orientado a negocio.
5. Cuando menciones métricas, explica brevemente qué significan.
6. Si la pregunta es de decisión gerencial, responde con recomendación y justificación.
7. Si hay incertidumbre o limitaciones, menciónalas explícitamente.
                """,
            ),
            (
                "human",
                """
Contexto del proyecto:
{context}

Pregunta del usuario:
{question}
                """,
            ),
        ]
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,
        google_api_key=GOOGLE_API_KEY,
    )

    chain = prompt | llm
    response = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return response.content


def check_agent_ready() -> Dict[str, object]:
    """
    Verifica si el agente tiene documentos y variables mínimas para funcionar.
    """
    validation = validate_knowledge_files()

    return {
        "knowledge_files_ready": validation["all_available"],
        "missing_files": validation["missing"],
        "google_key_available": bool(GOOGLE_API_KEY),
        "azure_search_configured": all(
            [
                AZURE_SEARCH_ENDPOINT,
                AZURE_SEARCH_KEY,
                AZURE_SEARCH_INDEX_NAME,
            ]
        ),
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