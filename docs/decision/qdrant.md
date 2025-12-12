# Qdrant

## Problem

Production RAG applications need:

- High-performance vector similarity search
- Metadata filtering for multi-tenant scenarios
- Easy integration without building custom APIs
- Support for hybrid search (dense + sparse vectors)

## Solution

We use [Qdrant](https://qdrant.tech/) as our vector database.

**Reference:** [Quick Start | Qdrant](https://qdrant.tech/documentation/quick-start/)

## Why Qdrant

### 1. Performance

Qdrant achieves the highest RPS (requests per second) and lowest latencies in almost all benchmark scenarios, showing up to 4x RPS gains on some datasets. Built with Rust, it delivers fast and reliable performance even under heavy loads.

For 1M vectors at 128D: FAISS ~5ms, Qdrant ~10ms, Pinecone ~10ms.

**Reference:** [Vector Database Benchmarks | Qdrant](https://qdrant.tech/benchmarks/)

### 2. Easy to Use

Unlike FAISS which is a library requiring you to build your own API layer, Qdrant provides REST API and gRPC out of the box:

| Feature | FAISS | Qdrant |
|---------|-------|--------|
| API | Build your own | REST/gRPC built-in |
| Deployment | Library only | Docker ready |
| Persistence | Manual | Built-in |
| Filtering | External integration | Native support |

```bash
# One-line deployment
docker run -p 6333:6333 qdrant/qdrant
```

Qdrant also provides client SDKs for Python, TypeScript/JavaScript, Rust, and Go.

### 3. Various Search Types

Qdrant supports multiple search capabilities that integrate directly into the search process (not post-processing):

| Search Type | Description |
|-------------|-------------|
| Dense Vector | Semantic similarity search (HNSW index) |
| Sparse Vector | BM25-like keyword matching |
| Hybrid Search | Combine dense + sparse with RRF fusion |
| Filtered Search | Payload-based filtering with rich expressions |

**Reference:** [Concepts | Qdrant](https://qdrant.tech/documentation/concepts/)

### 4. Production Features

- **Distance Metrics**: Cosine, Dot Product, Euclidean
- **Quantization**: Reduces RAM usage by up to 97%
- **Horizontal Scaling**: Sharding and replication support
- **Snapshots**: Backup and restore capabilities

## Comparison with Alternatives

| Database | Type | Best For |
|----------|------|----------|
| FAISS | Library | Prototyping, max speed (no API) |
| Qdrant | Open Source | Fast, filterable RAG apps |
| Pinecone | Managed SaaS | Scale with no infra management |

**Recommendation**: Start with Qdrant for open-source flexibility. Consider migration to managed services at 50-100M vectors or $500+/month cloud costs.

## Configuration

See [`libs/database/vector/qdrant/`](../../libs/database/vector/qdrant/) for our implementation.

## Sources

- [Vector Database Benchmarks - Qdrant](https://qdrant.tech/benchmarks/)
- [Vector Database Comparison 2025 | TensorBlue](https://tensorblue.com/blog/vector-database-comparison-pinecone-weaviate-qdrant-milvus-2025)
- [Qdrant vs Pinecone | Qdrant Blog](https://qdrant.tech/blog/comparing-qdrant-vs-pinecone-vector-databases/)
- [Vector Database Comparison | LiquidMetal AI](https://liquidmetal.ai/casesAndBlogs/vector-comparison/)
