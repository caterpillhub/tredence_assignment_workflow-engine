from uuid import uuid4
from typing import Dict, Any

from fastapi import FastAPI, HTTPException

from .models import (
    GraphConfig,
    RunState,
    CreateGraphRequest,
    CreateGraphResponse,
    RunGraphRequest,
    RunGraphResponse,
    RunStateResponse,
)
from .storage import GRAPHS, RUNS
from .engine import run_to_completion
from .workflows import default_code_review_graph

app = FastAPI(title="Workflow Engine - Option A (Code Review)")

@app.on_event("startup")
def load_default_graph() -> None:
    """
    On startup, register a default Option A Code Review graph.
    """
    graph = default_code_review_graph()
    GRAPHS[graph.id] = graph

@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "ok"}

@app.post("/graph/create", response_model=CreateGraphResponse)
def create_graph(req: CreateGraphRequest) -> CreateGraphResponse:
    """
    Create a new graph dynamically.
    """
    graph_id = str(uuid4())
    graph_config = GraphConfig(
        id=graph_id,
        start_node=req.start_node,
        nodes=req.nodes,
    )

    if graph_config.start_node not in graph_config.nodes:
        raise HTTPException(
            status_code=400,
            detail=f"start_node '{graph_config.start_node}' not found in nodes",
        )

    GRAPHS[graph_id] = graph_config
    return CreateGraphResponse(graph_id=graph_id)

@app.post("/graph/run", response_model=RunGraphResponse)
def run_graph(req: RunGraphRequest) -> RunGraphResponse:
    """
    Run an existing graph identified by graph_id with an initial state.
    """
    graph_id = req.graph_id

    if graph_id not in GRAPHS:
        raise HTTPException(status_code=404, detail=f"Graph '{graph_id}' not found")

    graph = GRAPHS[graph_id]

    run_id = str(uuid4())
    run_state = RunState(
        id=run_id,
        graph_id=graph_id,
        current_node=graph.start_node,
        state=req.initial_state,
    )

    run_state = run_to_completion(graph, run_state, max_steps=req.max_steps)
    RUNS[run_id] = run_state

    return RunGraphResponse(
        run_id=run_state.id,
        final_state=run_state.state,
        log=run_state.log,
    )

@app.get("/graph/state/{run_id}", response_model=RunStateResponse)
def get_run_state(run_id: str) -> RunStateResponse:
    """
    Fetch the current/terminal state of a particular run.
    """
    if run_id not in RUNS:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")

    return RUNS[run_id]
