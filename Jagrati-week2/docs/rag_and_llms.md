# Retrieval-Augmented Generation (RAG)

## What is RAG?
Retrieval-Augmented Generation (RAG) is an AI framework that combines information retrieval with language generation. Instead of relying solely on the knowledge stored in a model's parameters, RAG retrieves relevant documents from an external knowledge base and uses them as context when generating responses.

## Why RAG?
Large Language Models (LLMs) have a knowledge cutoff date and cannot access private or domain-specific documents. RAG solves this by:
- Allowing models to access up-to-date information
- Reducing hallucinations by grounding responses in retrieved facts
- Enabling use of private or proprietary documents without retraining the model
- Making the model's knowledge traceable and verifiable

## RAG Pipeline Components

### 1. Document Ingestion
Documents are loaded from various sources (PDFs, markdown, web pages, databases). They are then preprocessed and cleaned to remove noise.

### 2. Chunking
Documents are split into smaller chunks because:
- LLMs have a limited context window
- Smaller chunks improve retrieval precision
- Common strategies: fixed-size chunking, sentence-based chunking, semantic chunking

### 3. Embedding
Each chunk is converted into a dense vector representation using an embedding model. These embeddings capture the semantic meaning of the text. Popular embedding models include OpenAI's text-embedding-ada-002 and sentence-transformers.

### 4. Vector Store
Embeddings are stored in a vector database such as:
- Chroma (lightweight, local)
- FAISS (Facebook AI Similarity Search)
- Pinecone (cloud-based)
- Weaviate (open-source)

### 5. Retrieval
When a user asks a question, the query is embedded and compared against stored embeddings using cosine similarity or dot product. The top-k most similar chunks are retrieved.

### 6. Generation
The retrieved chunks are passed to the LLM as context along with the original query. The model uses this context to generate a grounded, accurate answer.

## Advanced RAG Techniques

### Hybrid Search
Combines dense vector search with sparse keyword search (BM25) for better retrieval coverage.

### Reranking
A second-pass model reranks the initially retrieved documents for better relevance before passing them to the LLM.

### HyDE (Hypothetical Document Embeddings)
The LLM first generates a hypothetical answer, which is then embedded and used for retrieval instead of the raw query.

### Parent-Child Chunking
Documents are chunked at multiple granularities. Small chunks are retrieved for precision, but their parent (larger) chunks are returned for context.

## Evaluation Metrics
- Faithfulness: Are answers grounded in retrieved documents?
- Answer Relevance: Does the answer address the question?
- Context Precision: Are the retrieved chunks relevant?
- Context Recall: Were all relevant documents retrieved?