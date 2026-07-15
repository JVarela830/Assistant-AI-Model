from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from langchain_core.documents import Document

CHROMA_PATH = "chroma"
DATA_PATH = "data"


def get_database():

    embeddings = OllamaEmbeddings(model="nomic-embed-text") #qwen model cannot do the embedding's work

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
    results = db.similarity_search_with_score(query, k=3)

    if len(results) == 0:
        return None
    
    valid_documents = []
    for doc, score in results:
        if score < 1.0: 
            valid_documents.append(doc.page_content)

    if not valid_documents:
        return None
    
    return " ".join(valid_documents)