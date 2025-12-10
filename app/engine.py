from typing import Dict, Any
from fastapi import HTTPException

from .models import GraphConfig, RunState, RunLogEntry
from .tools import TOOL_REGISTRY

def _get_tool(tool_name: str):
    """
    Helper to fetch a tool function from the registry, or raise clear error.
    """
    if tool_name not in TOOL_REGISTRY:
        raise HTTPException(status_code=500, detail=f"Unknown tool: {tool_name}")
    return TOOL_REGISTRY[tool_name]

def run_step(graph: GraphConfig, run_state: RunState) -> RunState:
    """
    Execute a single node in the graph.

    - Reads current_node from run_state.
    - Executes the associated tool, mutating the state.
    - Appends to execution log.
    - Decides the next node based on route_key/next/default_next.
    """
    if run_state.done or run_state.current_node is None:
        return run_state

    if run_state.current_node not in graph.nodes:
        raise HTTPException(
            status_code=500,
            detail=f"Node '{run_state.current_node}' not found in graph '{graph.id}'",
        )

    node_conf = graph.nodes[run_state.current_node]
    tool_fn = _get_tool(node_conf.tool)

    new_state: Dict[str, Any] = dict(run_state.state)

    new_state = tool_fn(new_state)

    run_state.log.append(
        RunLogEntry(node=node_conf.name, state_snapshot=new_state.copy())
    )

    next_node = None

    if node_conf.route_key and node_conf.next:
        outcome = new_state.get(node_conf.route_key)
        if outcome is not None:
            outcome_str = str(outcome)
            next_node = node_conf.next.get(outcome_str)

    if next_node is None:
        next_node = node_conf.default_next

    if not next_node:
        run_state.done = True
        run_state.current_node = None
    else:
        if next_node not in graph.nodes:
            raise HTTPException(
                status_code=500,
                detail=f"Next node '{next_node}' not found in graph '{graph.id}'",
            )
        run_state.current_node = next_node

    run_state.state = new_state
    return run_state

def run_to_completion(
    graph: GraphConfig,
    run_state: RunState,
    max_steps: int = 50,
) -> RunState:

    steps = 0
    while not run_state.done and steps < max_steps:
        run_state = run_step(graph, run_state)
        steps += 1

    if not run_state.done and steps >= max_steps:
        run_state.done = True
        run_state.state["termination_reason"] = "max_steps_reached"

    return run_state
