from typing import Dict, Any

ToolState = Dict[str, Any]

def extract_functions(state: ToolState) -> ToolState:
    """
    Very naive 'function extraction': just count Python 'def ' occurrences.
    """
    code = state.get("code", "")
    functions = code.count("def ")
    state["function_count"] = functions
    return state

def check_complexity(state: ToolState) -> ToolState:
    """
    Naive complexity metric: function_count * 10.
    """
    functions = state.get("function_count", 0)
    state["complexity_score"] = functions * 10
    return state

def detect_basic_issues(state: ToolState) -> ToolState:
    """
    Simple 'issue' checker:
    - counts lines longer than 80 characters as issues.
    """
    code = state.get("code", "")
    long_lines = sum(1 for line in code.splitlines() if len(line) > 80)
    state["issues"] = long_lines
    return state

def suggest_improvements(state: ToolState) -> ToolState:
    """
    Generates textual suggestions and a naive quality_score.
    """
    issues = state.get("issues", 0)
    complexity = state.get("complexity_score", 0)

    suggestions = []
    if issues > 0:
        suggestions.append("Break down long lines (>80 chars).")
    if complexity > 50:
        suggestions.append("Refactor into smaller, focused functions.")

    state["suggestions"] = suggestions
    # naive quality score out of 100
    state["quality_score"] = max(0, 100 - complexity - issues * 2)
    return state

def decide_quality_route(state: ToolState) -> ToolState:
    """
    Decide whether to continue improving or finish.
    - Uses 'quality_score' and 'threshold' from state.
    - Writes 'route' key with 'continue' or 'finish' for branching.
    """
    quality = state.get("quality_score", 0)
    threshold = state.get("threshold", 75)  

    if quality >= threshold:
        state["route"] = "finish"
    else:
        state["route"] = "continue"

    return state

def auto_improve_code(state: ToolState) -> ToolState:
    """
    Pretend to 'auto-improve' the code:
    - Reduce issues by 1 (if any).
    - Increase quality_score by 10.
    - Increment improvement_rounds counter.
    This simulates an iterative refinement loop.
    """
    issues = state.get("issues", 0)
    if issues > 0:
        issues -= 1
    state["issues"] = issues

    quality = state.get("quality_score", 0)
    state["quality_score"] = quality + 10

    state["improvement_rounds"] = state.get("improvement_rounds", 0) + 1

    suggestions = state.get("suggestions", [])
    suggestions.append("Applied automatic improvement round.")
    state["suggestions"] = suggestions

    return state

def finalize_review(state: ToolState) -> ToolState:
    state["review_status"] = "completed"
    return state

TOOL_REGISTRY = {
    "extract_functions": extract_functions,
    "check_complexity": check_complexity,
    "detect_basic_issues": detect_basic_issues,
    "suggest_improvements": suggest_improvements,
    "decide_quality_route": decide_quality_route,
    "auto_improve_code": auto_improve_code,
    "finalize_review": finalize_review,
}
