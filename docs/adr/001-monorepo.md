# ADR-001 — Single monorepo for all services

**Date:** 2025-01-01  
**Status:** Accepted  
**Deciders:** Neil, Kripa  

## Context

Tlanner has ~10 services, a frontend, shared libraries, infra config, and
workers. We needed to decide whether to split these into separate repositories
or keep them together.

## Decision

Single monorepo under `tlanner/` on GitHub.

## Reasons

- Two developers: a polyrepo means managing 10+ repos, 10+ CI pipelines,
  and 10+ sets of branch protection rules for a small team
- Shared types and utilities live in `libs/` and are imported directly —
  no versioning or publishing overhead
- A single PR can span a service change and its frontend counterpart
- Easier for Kripa to onboard: one clone, one `.env`, one `make dev-infra`

## Consequences

- The repo will grow large over time — manageable with good folder structure
- CI must be scoped to changed paths to avoid running all tests on every commit
  (handled in Phase 4 with GitHub Actions path filters)

## Alternatives considered

**Polyrepo:** Each service in its own GitHub repo. Rejected because the
coordination overhead outweighs the isolation benefits at our team size.

**Nx / Turborepo monorepo tooling:** Overkill for this stage. Plain folder
structure is sufficient and more transparent for learning purposes.
