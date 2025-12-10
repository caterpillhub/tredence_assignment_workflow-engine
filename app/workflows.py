from .models import GraphConfig, NodeConfig

def default_code_review_graph() -> GraphConfig:
    """
    Flow:
        extract -> complexity -> issues -> suggest -> decide -> (improve -> suggest) loop -> end
    """

    nodes = {
        "extract": NodeConfig(
            name="extract",
            tool="extract_functions",
            default_next="complexity",
        ),
        "complexity": NodeConfig(
            name="complexity",
            tool="check_complexity",
            default_next="issues",
        ),
        "issues": NodeConfig(
            name="issues",
            tool="detect_basic_issues",
            default_next="suggest",
        ),
        "suggest": NodeConfig(
            name="suggest",
            tool="suggest_improvements",
            default_next="decide",
        ),
        "decide": NodeConfig(
            name="decide",
            tool="decide_quality_route",
            route_key="route",
            next={
                "continue": "improve",
                "finish": "end",
            },
            default_next="end",  
        ),
        "improve": NodeConfig(
            name="improve",
            tool="auto_improve_code",
            default_next="suggest",  
        ),
        "end": NodeConfig(
            name="end",
            tool="finalize_review",
            default_next=None,  
        ),
    }

    graph = GraphConfig(
        id="code_review_v1",
        start_node="extract",
        nodes=nodes,
    )
    return graph
