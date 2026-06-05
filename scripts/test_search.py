import os
from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

load_dotenv()

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
AZURE_SEARCH_INDEX_NAME = os.getenv("AZURE_SEARCH_INDEX_NAME")


def test_search(query: str):
    client = SearchClient(
        endpoint=AZURE_SEARCH_ENDPOINT,
        index_name=AZURE_SEARCH_INDEX_NAME,
        credential=AzureKeyCredential(AZURE_SEARCH_KEY),
    )

    results = client.search(
        search_text=query,
        top=3,
    )

    for result in results:
        print("=" * 80)
        print("SOURCE:", result["source"])
        print("CATEGORY:", result["category"])
        print("CONTENT:")
        print(result["content"][:1000])


if __name__ == "__main__":
    test_search("materia prima más importante Equipo 2 Price_Z")