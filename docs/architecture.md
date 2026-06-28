# Tlanner — System Architecture

## Overview

Tlanner is an AI-powered travel planning platform built with a microservices
architecture. Users describe their travel goals; the platform generates
personalised itineraries using a multi-agent AI pipeline, integrates real-time
flight, hotel, and weather data, and delivers results as an interactive UI or
downloadable PDF.

## High-Level Design

```
Internet
    │
    ▼
Traefik (API Gateway)
    │   Rate limiting, JWT validation middleware, request routing
    │
    ├── User Service        Auth, profiles, preferences
    ├── Trip Service        Itinerary CRUD, destination management
    ├── Flight Service      Flight search (mock → Amadeus)
    ├── Hotel Service       Hotel search (mock → external API)
    ├── Weather Service     Forecasts via OpenWeatherMap + Redis cache
    └── Notification Svc   Email alerts, trip-ready notifications
              │
              ▼
         RabbitMQ
              │
    ┌─────────┼──────────┐
    ▼         ▼          ▼
LLM Svc   PDF Worker  Email Worker
LangGraph  ReportLab   SendGrid
Gemini API  → MinIO
    │
    ├── RAG Service         Qdrant vector search over travel guides
    ├── Recommender         LightFM collaborative filtering
    └── Cost Engine         XGBoost trip cost prediction
              │
    ┌─────────┼──────────┬──────────┐
    ▼         ▼          ▼          ▼
PostgreSQL  Redis     Qdrant     MinIO
```

## Services

| Service | Owner | Responsibility |
|---|---|---|
| user-service | Neil | Registration, login, JWT auth, user profiles |
| trip-service | Neil | Trip CRUD, destination management, itinerary storage |
| flight-service | Kripa | Flight search and fare comparison |
| hotel-service | Kripa | Hotel search and availability |
| weather-service | Kripa | Weather forecasts with Redis caching |
| llm-service | Neil | LangGraph multi-agent itinerary generation via Gemini |
| rag-service | Neil | Vector search over travel guides using Qdrant |
| recommendation-service | Neil | Personalised recommendations via LightFM |
| cost-service | Neil | Trip cost prediction via XGBoost |
| notification-service | Kripa | Email and in-app notifications via Celery |

## Data Stores

| Store | Purpose | Notes |
|---|---|---|
| PostgreSQL 16 | Primary relational store | One logical DB, schema-per-service pattern |
| Redis 7 | Cache, sessions, rate limiting | 100MB limit, LRU eviction |
| Qdrant | Vector embeddings for RAG | Travel guide knowledge base |
| MinIO | Object storage | Generated PDFs, user uploads |
| RabbitMQ | Message broker | Task queues, event bus between services |

## AI Pipeline

A user trip request flows through the AI layer in this order:

1. **Trip Service** receives the request and publishes an event to RabbitMQ
2. **LLM Service** picks it up and starts a LangGraph agent run
3. The agent calls **RAG Service** to retrieve relevant travel guide context
4. The agent calls **Recommender** for personalised attraction suggestions
5. The agent calls **Cost Engine** for a budget estimate
6. The agent synthesises all context and calls Gemini to generate the itinerary
7. Result is written back to **Trip Service** via API
8. A `trip.ready` event is published — triggers PDF generation and email

## Conventions

- All service APIs are versioned: `/api/v1/...`
- Every service exposes `GET /health` returning `{"status": "ok"}`
- All logs are structured JSON via `structlog`
- Correlation ID (`X-Request-ID`) is propagated across all service calls
- No secrets in code — `.env` only, documented in `.env.example`
- Migrations via Alembic — never raw `CREATE TABLE`
