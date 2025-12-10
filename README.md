# Workflow Engine - Option A (Code Review Mini-Agent)

This project implements a minimal workflow/graph engine using FastAPI.

- **Nodes** are configured with tools and routing info.
- **Tools** are Python functions that mutate a shared state dict.
- **Edges / Branching / Looping** are defined through node configs (`route_key`, `next`, `default_next`).
- A default **Code Review Mini-Agent** is provided as `code_review_v1`.

## Project Structure

- `app/main.py` – FastAPI app and HTTP endpoints.
- `app/models.py` – Pydantic models for nodes, graphs, runs, and API schemas.
- `app/engine.py` – Core engine logic (run_step, run_to_completion).
- `app/tools.py` – Code-review-related tools and tool registry.
- `app/storage.py` – In-memory storage of graphs and runs.
- `app/workflows.py` – Default Option A graph definition.

## How to Run

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: .\venv\Scripts\activate

2. Run the main app:

  ```bash
  uvicorn app.main:app --reload