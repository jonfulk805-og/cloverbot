"""
CloverBot - RAG (Retrieval-Augmented Generation) Pipeline
Ingests product docs into ChromaDB and retrieves relevant context for queries.
"""

import os
import logging
from pathlib import Path

import chromadb
from chromadb.config import Settings as ChromaSettings

from config import Config

logger = logging.getLogger("cloverbot.rag")

# Global client and collection
_client = None
_collection = None


def get_chroma_client():
    """Get or create the ChromaDB client."""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(
            path=Config.CHROMA_DIR,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return _client


def get_collection():
    """Get or create the knowledge base collection."""
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(
            name="cloverbot_knowledge",
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into overlapping chunks."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks


def ingest_knowledge_base():
    """
    Ingest all .txt and .md files from the knowledge directory into ChromaDB.
    Call this on startup or when knowledge base is updated.
    """
    knowledge_dir = Path(Config.KNOWLEDGE_DIR)
    if not knowledge_dir.exists():
        logger.warning("Knowledge directory not found: %s", knowledge_dir)
        return 0

    collection = get_collection()

    # Clear existing documents for a clean re-ingest
    existing = collection.count()
    if existing > 0:
        logger.info("Clearing %d existing documents from knowledge base", existing)
        all_ids = collection.get()["ids"]
        if all_ids:
            collection.delete(ids=all_ids)

    documents = []
    metadatas = []
    ids = []
    doc_count = 0

    for filepath in sorted(knowledge_dir.rglob("*")):
        if filepath.suffix.lower() not in (".txt", ".md"):
            continue

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            logger.error("Failed to read %s: %s", filepath, e)
            continue

        if not content.strip():
            continue

        source_name = str(filepath.relative_to(knowledge_dir))
        chunks = chunk_text(content)

        for i, chunk in enumerate(chunks):
            doc_id = f"{source_name}__chunk_{i}"
            documents.append(chunk)
            metadatas.append({"source": source_name, "chunk_index": i})
            ids.append(doc_id)

        doc_count += 1
        logger.info("Ingested %s (%d chunks)", source_name, len(chunks))

    if documents:
        # ChromaDB has a batch limit, process in batches of 500
        batch_size = 500
        for i in range(0, len(documents), batch_size):
            batch_end = min(i + batch_size, len(documents))
            collection.add(
                documents=documents[i:batch_end],
                metadatas=metadatas[i:batch_end],
                ids=ids[i:batch_end],
            )

    logger.info(
        "Knowledge base ingestion complete: %d files, %d chunks",
        doc_count,
        len(documents),
    )
    return doc_count


def query_knowledge(question, n_results=5):
    """
    Query the knowledge base for relevant context.
    Returns a list of relevant text chunks.
    """
    collection = get_collection()

    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[question],
        n_results=min(n_results, collection.count()),
    )

    chunks = []
    if results and results["documents"]:
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            chunks.append({"text": doc, "source": meta.get("source", "unknown")})

    return chunks


def format_context(chunks):
    """Format retrieved chunks into a context string for the LLM."""
    if not chunks:
        return ""

    context_parts = []
    for chunk in chunks:
        source = chunk["source"]
        text = chunk["text"]
        context_parts.append(f"[Source: {source}]\n{text}")

    return (
        "\n\n---\n\nRelevant product knowledge:\n\n"
        + "\n\n".join(context_parts)
        + "\n\n---"
    )
