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

    db.addDocument([new_document])
