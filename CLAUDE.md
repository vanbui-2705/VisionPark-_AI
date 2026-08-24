# CLAUDE.md

This file provides repository guidance for coding agents working on VisionPark.

## Project overview

VisionPark is a smart parking management system. The MVP is a monorepo with a FastAPI backend and one React frontend. ALPR is a bounded module inside the backend for MVP and may be extracted later only through an ADR.

The approved BA/SRS is in `docs/Document.md`. The authoritative architecture and directory rules are in `docs/architecture.md`.

## Required codebase boundaries

- All backend code belongs under `backend/app`.
- Business domains belong under `backend/app/modules`.
- ALPR code belongs under `backend/app/alpr`.
- External adapters belong under `backend/app/integrations`.
- All frontend code belongs under `frontend/src`.
- Frontend features belong under `frontend/src/modules`.
- Station and Admin are layouts/modules of one React application, not separate apps.
- Backend/frontend-specific scripts and tests stay under their corresponding parent.
- Root `tests` is reserved for system-wide E2E, performance, and security tests.
- Project documentation belongs under `docs`; deployment configuration belongs under `deployment`.
- Do not recreate the deprecated `apps`, `services`, `packages`, or `infra` directory structure.

## Architecture rules

- Backend: FastAPI/Python modular monolith.
- Frontend: React/TypeScript with role-based Station and Admin layouts.
- Database: PostgreSQL is the source of truth.
- ALPR: module boundary for YOLO/PaddleOCR/OpenCV; it must not own parking business decisions.
- Storage: use an image storage adapter; the database stores object keys and metadata, not image blobs.
- Communication: REST/JSON for MVP; no message broker without an approved ADR.
- State changes: only backend business modules may change parking transaction/payment states.
- Critical writes: use database transactions, idempotency, authorization, and audit logs.
- Business logic must not be placed in HTTP endpoints or React components.

## Expected commands after initialization

### Backend

- Install: `cd backend && pip install -e .`
- Run: `cd backend && uvicorn app.main:app --reload`
- Test: `cd backend && pytest`
- Lint: `cd backend && ruff check .`
- Format: `cd backend && ruff format .`
- Migration: `cd backend && alembic upgrade head`

### Frontend

- Install: `cd frontend && npm install`
- Run: `cd frontend && npm run dev`
- Test: `cd frontend && npm run test`
- Lint: `cd frontend && npm run lint`
- Build: `cd frontend && npm run build`

### Full local environment

- Run: `docker compose up --build`
- Stop: `docker compose down`

These commands describe the approved target setup. Do not claim they work until the corresponding project files have been initialized.
