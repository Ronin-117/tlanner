# Contributing to Tlanner

## Branch naming
- `feat/short-description` — new feature
- `fix/short-description` — bug fix
- `chore/short-description` — tooling, deps, config
- `docs/short-description` — documentation only

## Commit messages (Conventional Commits)
- `feat(user-service)`— add refresh token rotation
- `fix(trip-service)`— handle null destination
- `chore(infra)` — add redis healthcheck
- `docs(rag)` — document embedding pipeline

## Pull Request rules
- No direct commits to `main`
- Every PR needs: what it does + how to test it
- The other person reviews before merge
- Squash merge only

## Local setup
1. Copy `.env.example` to `.env` and fill in values
2. Run `make dev-infra` to start infrastructure containers
3. Start individual services as needed