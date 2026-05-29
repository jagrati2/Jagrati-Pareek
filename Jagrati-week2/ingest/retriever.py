"""
ingest/retriever.py

Loads the persisted ChromaDB vector store and provides
a retrieval function that returns the top-k relevant chunks.
"""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v2"

# Module-level cache so the store is only loaded once
_vector_store = None


def get_vector_store():
    """Load (or return cached) ChromaDB vector store."""
    global _vector_store
    if _vector_store is None:
        if not CHROMA_DIR.exists():
            raise RuntimeError(
                "ChromaDB not found. Run `python -m ingest.ingest` first."
            )
        embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
        _vector_store = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embeddings,
            collection_name="rag_docs",
        )
    return _vector_store


def retrieve(query: str, top_k: int = 3) -> list[dict]:
    """
    Retrieve the top-k relevant chunks for a query.

    Returns a list of dicts:
        [{"content": str, "source": str, "chunk_index": int}, ...]
    """
    store = get_vector_store()
    results = store.similarity_search(query, k=top_k)
    chunks = []
    for doc in results:
        chunks.append(
            {
                "content": doc.page_content,
                "source": doc.metadata.get("source", "unknown"),
                "chunk_index": doc.metadata.get("chunk_index", -1),
            }
        )
    return chunks