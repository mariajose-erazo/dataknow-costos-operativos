import os
import re
from pathlib import Path

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType,
)

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_PATH = PROJECT_ROOT / "reports"

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv(
    "AZURE_SEARCH_INDEX_NAME",
    "dataknow-knowledge-index",
)

KNOWLEDGE_FILES = [
    "resumen_ejecutivo.md",
    "resultados_eda.md",
    "resultados_modelado.md",
    "resultados_forecasting.md",
    "preguntas_frecuentes.md",
]


def validate_env():
    missing = []

    if not AZURE_SEARCH_ENDPOINT:
        missing.append("AZURE_SEARCH_ENDPOINT")

    if not AZURE_SEARCH_KEY:
        missing.append("AZURE_SEARCH_KEY")

    if not AZURE_SEARCH_INDEX_NAME:
        missing.append("AZURE_SEARCH_INDEX_NAME")

    if missing:
        raise ValueError(f"Faltan variables en .env: {', '.join(missing)}")


def chunk_text(text: str):
    """
    Divide documentos Markdown usando encabezados ###.
    Ideal para FAQs y documentación estructurada.
    """

    sections = re.split(r"\n(?=### )", text)

    chunks = []

    for section in sections:
        section = section.strip()

        if section:
            chunks.append(section)

    return chunks

def create_index():
    """
    Crea o actualiza el índice de Azure AI Search.
    """
    credential = AzureKeyCredential(AZURE_SEARCH_KEY)

    index_client = SearchIndexClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        credential=credential,
    )

    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
        ),
        SearchableField(
            name="content",
            type=SearchFieldDataType.String,
            analyzer_name="es.microsoft",
        ),
        SimpleField(
            name="source",
            type=SearchFieldDataType.String,
            filterable=True,
            facetable=True,
        ),
        SimpleField(
            name="category",
            type=SearchFieldDataType.String,
            filterable=True,
            facetable=True,
        ),
    ]

    index = SearchIndex(
        name=AZURE_SEARCH_INDEX_NAME,
        fields=fields,
    )

    index_client.create_or_update_index(index)

    print(f"Índice creado o actualizado: {AZURE_SEARCH_INDEX_NAME}")


def build_documents():
    """
    Construye documentos indexables desde los archivos Markdown.
    """
    documents = []

    for file_name in KNOWLEDGE_FILES:
        path = REPORTS_PATH / file_name

        if not path.exists():
            print(f"Archivo no encontrado: {path}")
            continue

        text = path.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        category = file_name.replace(".md", "")

        for i, chunk in enumerate(chunks):
            documents.append(
                {
                    "id": f"{category}-{i}",
                    "content": chunk,
                    "source": file_name,
                    "category": category,
                }
            )

    return documents


def upload_documents(documents):
    """
    Sube los fragmentos al índice de Azure AI Search.
    """
    credential = AzureKeyCredential(AZURE_SEARCH_KEY)

    search_client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=credential,
    )

    result = search_client.upload_documents(documents=documents)

    succeeded = sum(1 for item in result if item.succeeded)

    print(f"Documentos subidos correctamente: {succeeded}/{len(documents)}")


if __name__ == "__main__":
    validate_env()
    create_index()

    docs = build_documents()

    print(f"Fragmentos construidos: {len(docs)}")

    upload_documents(docs)