"""
agent.py
--------
Agente conversacional de IA usando LangChain + ChromaDB + OpenAI.

El agente puede responder preguntas sobre:
- Resultados del análisis de datos
- Proyecciones de costos
- Comparaciones entre equipos y materias primas
- Interpretación de los modelos
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def build_vector_store(documents_path: str = "reports/"):
    """
    Construye la base de datos vectorial (ChromaDB) a partir
    de documentos del proyecto (informe, resultados, etc.).

    Returns:
        vectorstore: instancia de ChromaDB lista para consultas
    """
    try:
        from langchain_community.document_loaders import DirectoryLoader, TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.vectorstores import Chroma
        from langchain_openai import OpenAIEmbeddings
    except ImportError as e:
        raise ImportError(f"Instala las dependencias necesarias: {e}")

    loader = DirectoryLoader(documents_path, glob="**/*.md", loader_cls=TextLoader)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="chroma_db/")
    return vectorstore


def build_agent(vectorstore):
    """
    Construye el agente conversacional con memoria y contexto.

    Args:
        vectorstore: base de datos vectorial con el conocimiento del proyecto

    Returns:
        chain: cadena de conversación lista para responder preguntas
    """
    try:
        from langchain_openai import ChatOpenAI
        from langchain.chains import ConversationalRetrievalChain
        from langchain.memory import ConversationBufferMemory
    except ImportError as e:
        raise ImportError(f"Instala las dependencias necesarias: {e}")

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
        openai_api_key=OPENAI_API_KEY
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
        memory=memory,
        verbose=False
    )
    return chain


def ask_agent(chain, question: str) -> str:
    """
    Envía una pregunta al agente y retorna la respuesta.

    Args:
        chain: agente conversacional construido con build_agent()
        question: pregunta en lenguaje natural

    Returns:
        respuesta del agente como string
    """
    result = chain({"question": question})
    return result["answer"]


if __name__ == "__main__":
    print("Construyendo base de conocimiento...")
    vectorstore = build_vector_store()
    agent = build_agent(vectorstore)

    print("Agente listo. Escribe 'salir' para terminar.\n")
    while True:
        question = input("Tu pregunta: ").strip()
        if question.lower() in ["salir", "exit", "quit"]:
            break
        if question:
            answer = ask_agent(agent, question)
            print(f"\nAgente: {answer}\n")
