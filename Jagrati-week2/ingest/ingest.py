"""
ingest/ingest.py

Loads documents from /docs, chunks them, embeds them,
and stores them in a local ChromaDB vector store.
"""

import os
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ── Paths ────────────────────────────────────────────────────────────────────
DOCS_DIR = Path(__file__).parent.parent / "docs"
CHROMA_DIR = Path(__file__).parent.parent / "chroma_db"

# ── Embedding model (local, no API key needed) ────────────────────────────────
EMBED_MODEL = "all-MiniLM-L6-v2"


def load_documents():
    """Load all .md and .txt files from the docs/ directory."""
    docs = []
    for filepath in DOCS_DIR.glob("*.md"):
        loader = TextLoader(str(filepath), encoding="utf-8")
        loaded = loader.load()
        # Tag each document with its source filename
        for doc in loaded:
            doc.metadata["source"] = filepath.name
        docs.extend(loaded)
    print(f"[Ingest] Loaded {len(docs)} document(s) from {DOCS_DIR}")
    return docs


def chunk_documents(docs, chunk_size=500, chunk_overlap=50):
    """Split documents into smaller chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(docs)
    # Add chunk index within each source file
    source_counters = {}
    for chunk in chunks:
        src = chunk.metadata.get("source", "unknown")
        source_counters[src] = source_counters.get(src, 0)
        chunk.metadata["chunk_index"] = source_counters[src]
        source_counters[src] += 1

    print(f"[Ingest] Created {len(chunks)} chunk(s)")
    return chunks


def build_vector_store(chunks):
    """Embed chunks and persist to ChromaDB."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR),
        collection_name="rag_docs",
    )
    print(f"[Ingest] Vector store saved to {CHROMA_DIR}")
    return vector_store


def run_ingestion():
    """Full ingestion pipeline: load → chunk → embed → store."""
    docs = load_documents()
    chunks = chunk_documents(docs)
    vector_store = build_vector_store(chunks)
    return vector_store


if __name__ == "__main__":
    run_ingestion()
    print("[Ingest] Done.")