from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from langchain_core.documents import Document

CHROMA_PATH = "chroma"
SIMILARITY_THRESHOLD = 1.0 # Maximum embedding distance considered relevant

embeddings = OllamaEmbeddings(model="nomic-embed-text") 

db = Chroma(
persist_directory=CHROMA_PATH, 
embedding_function=embeddings
)


def add_document(fact):
    """Add a new fact of the user to the database"""
    document = Document(
        page_content = fact,
        metadata={"source": "user_input"}
    )

    db.add_documents([document])


def search_data(query):
    """Return the text of documents similar to the query."""
    results = db.similarity_search_with_score(query, k=3)

    if not results:
        return None
    
    valid_documents = [
        doc.page_content
        for doc, score in results
        if score < SIMILARITY_THRESHOLD
    ]

    if not valid_documents:
        return None
    
    return " ".join(valid_documents)