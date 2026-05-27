# AI Code Review Agent

AI Code Review Agent is a FastAPI-based GitHub webhook service that receives pull request events, enqueues review work in Redis (RQ), runs a code-review pipeline (parser + AI agents) in an RQ worker, and posts a combined Markdown review summary back to the pull request.

## Project Overview

The project automates lightweight code review for pull requests. GitHub sends a webhook to FastAPI, FastAPI queues the review job in Redis, the RQ worker runs the review pipeline over changed files, aggregates findings, formats Markdown, and posts a single PR comment.

Model execution is handled via the local `ollama` CLI (configurable with `OLLAMA_MODEL`, default `qwen2.5-coder:1.5b`).

## Architecture Diagram

```mermaid
flowchart TD
	A[GitHub PR Event] --> B[FastAPI /webhook]
	B --> C[RQ enqueue]
	C --> D[Redis Queue]
	D --> E[RQ Worker]
	E --> F[review_payload()]
	F --> G[Parser (tree_parser)]
	F --> H[Security Agent]
	F --> I[Logic Agent]
	F --> J[Style Agent]
	H --> K[Aggregator]
	I --> K
	J --> K
	K --> L[Markdown Formatter]
	L --> M[GitHub PR Comment]
```

## Architecture Explanation

The request path stays short while the review path stays asynchronous. FastAPI only receives and enqueues webhook payloads, then hands work off to Redis-backed RQ so the API remains responsive. The worker performs the expensive part of the pipeline: validating payloads, parsing code into structured facts, running the AI review agents, aggregating findings across all files, and publishing a single review comment.

For interview use, the important design point is separation of concerns. The webhook receiver, queue, worker, and analyzer are intentionally simple and isolated, which makes the pipeline easier to operate, debug, and scale independently.

## Features

- GitHub webhook ingestion for pull request events
- Asynchronous review execution through Redis and RQ
- Pull request file retrieval from the PR head branch
- AI-powered Security, Quality, and Best Practices checks
- Aggregated PR review summary with severity levels
- Single PR comment per review run

## Tech Stack

- Python 3.11+ (Docker image uses 3.11; local dev tested on macOS with 3.14)
- FastAPI
- Uvicorn
- Redis
- RQ
- PyGithub
- Ollama (local model runtime)
- Docker
- Docker Compose

## Project Structure

```text
app/
	main.py                  FastAPI application entrypoint
	api/webhook.py           GitHub webhook receiver
	github/github_client.py   GitHub API helpers
	parser/tree_parser.py     Python AST parser into CodeFact objects
	agents/                  Security/Logic/Style agents (Ollama-backed)
	reviewer/review_pipeline.py Orchestrates parse → agents → aggregate → markdown
	reviewer/aggregator.py    Dedup + normalize findings
	reviewer/formatter.py     Markdown output generation
	rag/                      Retrieval helpers (embeddings + search)
	workers/review_worker.py  Queue worker and PR comment poster
	workers/analyzer.py       Legacy analyzer (kept for reference; not used by pipeline)
	utils/logger.py           Shared logging helper
docker-compose.yml         Local container orchestration
Dockerfile                 Python application image
README.md                  Project documentation
requirements.txt           Python dependencies
```

## Production Package Report

Core files (ship these):
- `app/api/webhook.py`, `app/main.py`
- `app/workers/review_worker.py`
- `app/reviewer/review_pipeline.py`, `app/reviewer/aggregator.py`, `app/reviewer/formatter.py`, `app/reviewer/schemas.py`
- `app/parser/tree_parser.py`
- `app/agents/security.py`, `app/agents/logic.py`, `app/agents/style.py`, `app/agents/model_adapter.py`
- `app/github/github_client.py`
- `requirements.txt`, `Dockerfile`, `docker-compose.yml`

Ignored runtime artifacts (do not commit):
- `.DS_Store`, `venv/`, `__pycache__/`, `*.pyc`
- `app/storage/review_history.json`
- `cache/`, `.cache/`, `logs/`, `tmp/`, `temp/`, `model_cache/`

Dependencies used:
- Python deps: FastAPI/Uvicorn, Redis/RQ, PyGithub, python-dotenv, sentence-transformers
- External services/tools: Redis, Ollama (`ollama` CLI + local model)

## Installation

Prereqs:
- Redis available (Docker or local)
- Ollama installed and running

1. Clone the repository.
2. Create a `.env` file and set `GITHUB_TOKEN`.
3. (Optional) Set `REDIS_URL` (default: `redis://localhost:6379/0`).
4. (Optional) Set `OLLAMA_MODEL` (default: `qwen2.5-coder:1.5b`).

macOS Ollama setup:
```bash
brew install ollama
brew services start ollama
ollama pull qwen2.5-coder:1.5b
```

## Running Locally

### Recommended (Hybrid)

Run Redis in Docker, run API + worker on your host (so the worker can call the local `ollama` CLI).

Terminal 1 (Redis):
```bash
docker compose up -d redis
```

Terminal 2 (FastAPI):
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 3 (RQ worker):
```bash
source venv/bin/activate
rq worker --url redis://localhost:6379/0
```

Notes:
- The agents call `ollama run ...` via subprocess; ensure `ollama` is on PATH.
- `docker compose up --build` runs API+worker in containers, but the current image does not include the `ollama` binary.

### Without Docker

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Run the worker in a second terminal when testing the queue-based flow.

## Tests

```bash
source venv/bin/activate
python scripts/test_integration.py
python -m unittest tests.test_integration_stages
```

## Screenshots

Add screenshots here after deploying the app locally or to your target environment.

## Demo GIF

Insert a short demo GIF here for the final portfolio version.

## Resume Bullet Points

- Built an end-to-end GitHub PR review pipeline using FastAPI, Redis (RQ), and an RQ worker.
- Implemented a parser + multi-agent AI reviewer (security/logic/style) with aggregation into a single PR summary.
- Posted one Markdown review comment per PR with deduplication and lightweight history tracking.

## Interview Preparation

### A) 60-second project explanation
This is a GitHub PR code-review bot. GitHub hits a FastAPI webhook, the webhook enqueues a job into Redis via RQ, and a worker pulls the job to run an AI review pipeline: parse changed files, run three focused agents (security/logic/style) using Ollama, aggregate findings, generate a concise Markdown summary, and post it back as a PR comment.

### B) Architecture explanation (what runs where)
- FastAPI: accepts webhooks and enqueues jobs
- Redis: durable queue backend
- RQ worker: executes the long-running review pipeline
- Ollama: local model runtime used by the agents

### C) Challenges faced
- Recovering and re-verifying the historical AI pipeline modules
- Getting runtime dependencies aligned (Redis + Ollama + model availability)
- Keeping the webhook path fast while moving work to background execution

### D) Problems solved
- Asynchronous PR review execution (webhook stays responsive)
- Structured aggregation of multi-agent findings into one comment
- Repeatable local validation via integration scripts + staged tests

### E) Why Redis + RQ was used
RQ is simple, production-proven, and fits the “enqueue a Python function with a payload” model. Redis provides a durable queue backend so review jobs can survive transient API restarts and be retried.

### F) Why AI agents were separated
Separation keeps prompts and responsibilities narrow (security vs logic vs style), improves explainability of findings, and makes it easy to add/remove a dimension without rewriting the whole pipeline.

### G) Expected interview questions + short answers
- Q: Why not do the whole review inside the webhook?
	A: Model calls and repo IO are slow; queueing keeps the API responsive and reliable.
- Q: How do you ensure one clean PR comment?
	A: Findings are aggregated and formatted once; the GitHub client avoids duplicates.
- Q: What would you do for scale?
	A: Run more RQ workers, isolate queues, and add rate limiting / retries.

- Why did you separate the webhook receiver from the worker?
- How does Redis improve the reliability of the review pipeline?
- How do you avoid posting duplicate PR comments?
- How do you keep the review output concise and useful for developers?
- What would you change if the analyzer had to support more rules or higher traffic?

## Future Improvements

- Add richer rule configuration for analyzer checks
- Add automated tests for webhook and worker flows
- Persist review history for analytics and traceability
- Add a retry policy and dead-letter handling for failed jobs
- Improve severity scoring and file-level summaries