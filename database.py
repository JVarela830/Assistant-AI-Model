from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from langchain_core.documents import Document

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def get_database():

    embeddings = OllamaEmbeddings(model="qwen2.5:1.5b")

    db = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embeddings
    )

    return db


def update_database(data):
    db = get_database()
    new_document = Document(
        page_content= data,
        metadata={"new_info": "data"}
    )

    db.add_documents([new_document])


def search_data(query):
    db = get_database()
    results = db.similarity_search_with_relevance_scores(query, k=3)

    if len(results) == 0 or results[0][1] < 0.7:
        print(f"Unable to find matching results.")
        return None
    
    similarity_data = [doc.page_content for doc, score in results]
    
    return " ".join(similarity_data)