# utpl_chatbot

A clean, hexagonal-architecture chatbot backend using FastAPI, Langchain (Gemini LLM), PostgreSQL, SQLAlchemy, and Alembic. Receives Telegram webhooks, replies using Gemini, and persists conversations.

## Features
- FastAPI backend
- Telegram webhook integration
- Langchain + Gemini LLM for responses
- PostgreSQL persistence (SQLAlchemy + Alembic)
- Dockerized setup
- Hexagonal Architecture
- Unit and integration tests

## Setup

1. Copy `.env.example` to `.env` and fill in your secrets.
2. Build and run with Docker Compose:
   ```sh
   docker-compose up --build
   ```
3. Run Alembic migrations:
   ```sh
   docker-compose exec app alembic upgrade head
   ```

## Project Structure

- `app/` - Main application code (hexagonal architecture)
- `alembic/` - Database migrations
- `tests/` - Unit and integration tests

## Environment Variables
See `.env.example` for required variables.