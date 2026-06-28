# ADR-002 — FastAPI as the backend framework for all services

**Date:** 2025-01-01  
**Status:** Accepted  
**Deciders:** Neil, Kripa  

## Context

We needed a Python web framework for all backend microservices. The main
contenders were FastAPI, Flask, and Django REST Framework.

## Decision

FastAPI for every backend service.

## Reasons

- Native async support via `asyncio` — essential for services that call
  external APIs (Gemini, OpenWeatherMap, Amadeus) concurrently
- Automatic OpenAPI documentation at `/docs` — zero extra work
- Pydantic v2 integration for request/response validation is the same library
  used by LangChain and LangGraph, so the team only learns one schema system
- Significantly faster than Flask/Django for I/O-bound workloads in benchmarks
- First-class support in the Python AI/ML ecosystem

## Consequences

- Team needs to be comfortable with Python async (`async def`, `await`,
  `asyncio`) — steeper than sync Flask but worth learning
- Not a full framework (no built-in admin, ORM, etc.) — we bring our own
  pieces (SQLAlchemy, Alembic). This is a feature, not a bug.

## Alternatives considered

**Flask:** Simpler but sync-first. Async support is bolted on. No automatic
docs. Would require more boilerplate for the same result.

**Django REST Framework:** Too opinionated and heavy for microservices.
Built for monoliths. The ORM and admin are irrelevant here.
