# ADR-003 — Qdrant as the vector database for RAG

**Date:** 2025-01-01  
**Status:** Accepted  
**Deciders:** Neil, Kripa  

## Context

The RAG service needs a vector database to store and search embeddings of
travel guide documents. Options evaluated: Qdrant, Pinecone, Weaviate,
pgvector (PostgreSQL extension).

## Decision

Qdrant, self-hosted via Docker.

## Reasons

- Self-hosted: no external API dependency, no per-query cost, runs inside
  our Docker Compose stack
- Purpose-built for vector search — faster and more memory-efficient than
  pgvector for our use case
- Good Python client with async support
- 256MB RAM limit is workable for our collection sizes
- Free and open source — fits the zero-budget constraint

## Consequences

- We manage the Qdrant container ourselves (handled in `docker-compose.yml`)
- On the OCI free tier (1GB RAM total), Qdrant is capped at 256MB —
  sufficient for a travel guide knowledge base of reasonable size

## Alternatives considered

**Pinecone:** Managed, excellent DX, but has a free tier limit and adds
an external dependency. Rejected to keep the stack self-contained.

**pgvector:** Runs inside existing PostgreSQL. Rejected because mixing
vector workloads into the primary relational DB creates resource contention
on a 1GB VPS.

**Weaviate:** More complex to operate, higher memory footprint. Overkill
for this stage.
