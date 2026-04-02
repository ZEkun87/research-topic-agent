from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from main import build_workflow


def _initial_state():
    return {
        "user_input": "我想做大模型RAG方向研究",
        "keywords": [],
        "papers": [],
        "field_overview": {},
        "topic_paths": [],
        "final_recommendation": {},
        "evidence_chain": [],
    }


def test_workflow_runs_end_to_end():
    app = build_workflow()
    result = app.invoke(_initial_state())
    assert result["final_recommendation"]
    assert result["evidence_chain"]


def test_generate_three_topics():
    app = build_workflow()
    result = app.invoke(_initial_state())
    assert len(result["topic_paths"]) == 3

