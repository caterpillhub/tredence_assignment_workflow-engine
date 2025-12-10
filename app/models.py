from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class NodeConfig(BaseModel):
    """
    Configuration for a single node in the workflow graph.
    """
    name: str
    tool: str
    route_key: Optional[str] = None
    next: Optional[Dict[str, str]] = None
    default_next: Optional[str] = None

class GraphConfig(BaseModel):
    """
    Represents a complete workflow graph.
    """
    id: str
    start_node: str
    nodes: Dict[str, NodeConfig]

class RunLogEntry(BaseModel):
    """
    One step in the execution log.
    """
    node: str
    state_snapshot: Dict[str, Any]

class RunState(BaseModel):
    """
    State for a single graph run.
    """
    id: str
    graph_id: str
    current_node: Optional[str]
    state: Dict[str, Any] = Field(default_factory=dict)
    done: bool = False
    log: List[RunLogEntry] = Field(default_factory=list)

class CreateGraphRequest(BaseModel):
    """
    Request body for /graph/create.
    """
    start_node: str
    nodes: Dict[str, NodeConfig]

class CreateGraphResponse(BaseModel):
    """
    Response body for /graph/create.
    """
    graph_id: str

class RunGraphRequest(BaseModel):
    """
    Request body for /graph/run.
    """
    graph_id: str
    initial_state: Dict[str, Any] = Field(default_factory=dict)
    max_steps: int = 50

class RunGraphResponse(BaseModel):
    """
    Response body for /graph/run.
    """
    run_id: str
    final_state: Dict[str, Any]
    log: List[RunLogEntry]

class RunStateResponse(RunState):
    pass
