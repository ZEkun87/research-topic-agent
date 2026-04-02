"""
科研选题智能 Agent 系统（可运行 MVP）。

架构：LangGraph 多 Agent 协作流程
包含：解析 Agent、检索 Agent、分析 Agent、选题 Agent、决策 Agent
"""

from __future__ import annotations

from typing import Dict, List, TypedDict

from langgraph.graph import END, StateGraph

# 全局状态（多Agent共享数据）
class ResearchState(TypedDict):
    user_input: str          # 用户研究兴趣
    keywords: List[str]      # 检索关键词
    papers: List[Dict]       # 文献列表
    field_overview: Dict     # 领域全景
    topic_paths: List[Dict]  # 3条候选选题
    final_recommendation: Dict
    evidence_chain: List[Dict]


def llm_parse(user_input: str) -> List[str]:
    """模拟需求解析：从用户输入抽取检索关键词。"""
    base = ["RAG", "大模型", "检索增强生成", "可解释性", "评测"]
    if "医学" in user_input:
        return base + ["医学", "临床"]
    return base


def search_semantic_scholar(keywords: List[str]) -> List[Dict]:
    """模拟 Semantic Scholar 检索。"""
    return [
        {
            "id": "S1",
            "title": "RAG Evaluation in Domain-specific QA",
            "source": "SemanticScholar",
            "year": 2024,
            "score": 0.92,
            "keywords": keywords[:3],
        },
        {
            "id": "S2",
            "title": "Improving Faithfulness of Retrieval-Augmented LLMs",
            "source": "SemanticScholar",
            "year": 2023,
            "score": 0.88,
            "keywords": keywords[:3],
        },
    ]


def search_arxiv(keywords: List[str]) -> List[Dict]:
    """模拟 arXiv 检索。"""
    return [
        {
            "id": "A1",
            "title": "A Survey of Retrieval-Augmented Generation",
            "source": "arXiv",
            "year": 2024,
            "score": 0.9,
            "keywords": keywords[:3],
        },
        {
            "id": "A2",
            "title": "RAG for Scientific Assistants: Methods and Challenges",
            "source": "arXiv",
            "year": 2025,
            "score": 0.86,
            "keywords": keywords[:3],
        },
    ]


def deduplicate_and_filter(papers: List[Dict]) -> List[Dict]:
    """去重并按年份与相关性过滤排序。"""
    by_title: Dict[str, Dict] = {}
    for paper in papers:
        title = paper["title"]
        if title not in by_title or paper["score"] > by_title[title]["score"]:
            by_title[title] = paper
    filtered = [p for p in by_title.values() if p["year"] >= 2023]
    return sorted(filtered, key=lambda x: (x["score"], x["year"]), reverse=True)


def llm_analyze_field(titles: List[str]) -> Dict:
    """模拟领域分析结果。"""
    return {
        "hot_topics": [
            "retrieval quality and reranking",
            "faithfulness and hallucination control",
            "domain adaptation for enterprise/science data",
        ],
        "gaps": [
            "缺少统一评测协议",
            "跨领域迁移性能波动明显",
            "证据可追溯性与解释性不足",
        ],
        "title_count": len(titles),
    }


def llm_generate_topics(user_input: str, field_overview: Dict) -> List[Dict]:
    """模拟生成 3 条候选选题路径。"""
    return [
        {
            "id": "T1",
            "name": "面向科研问答的可追溯 RAG 评测框架",
            "innovation": "引入证据链一致性指标，统一比较不同 RAG 管线。",
            "feasibility": "中高",
            "value": "高",
            "based_on": field_overview.get("hot_topics", [])[:2],
        },
        {
            "id": "T2",
            "name": "RAG 中重排序策略对事实一致性的影响研究",
            "innovation": "系统分析不同 reranker 对 hallucination 的抑制效果。",
            "feasibility": "高",
            "value": "中高",
            "based_on": field_overview.get("hot_topics", [])[:2],
        },
        {
            "id": "T3",
            "name": "面向垂直领域的轻量化 RAG 迁移方法",
            "innovation": "在低算力条件下保持召回与生成质量平衡。",
            "feasibility": "中",
            "value": "中高",
            "based_on": [user_input] + field_overview.get("gaps", [])[:1],
        },
    ]


def llm_judge_best_topic(topic_paths: List[Dict], field_overview: Dict):
    """模拟决策收敛：选择最优选题并返回证据链。"""
    _ = field_overview
    best = topic_paths[0]
    evidence = [
        {
            "paper_id": "S1",
            "reason": "支持统一评测框架的必要性。",
        },
        {
            "paper_id": "A1",
            "reason": "综述显示证据可追溯与可信评测是关键痛点。",
        },
    ]
    recommendation = {
        "topic_id": best["id"],
        "topic_name": best["name"],
        "why": "创新性与学术价值较高，同时可在学期内完成 MVP。",
    }
    return recommendation, evidence

# ===================== Agent 1：需求解析Agent =====================
def parse_requirement_agent(state: ResearchState):
    # 功能：理解用户意图 → 生成检索关键词
    user_input = state["user_input"]
    # 调用大模型提取核心关键词
    keywords = llm_parse(user_input)
    return {"keywords": keywords}

# ===================== Agent 2：文献检索Agent =====================
def paper_retrieve_agent(state: ResearchState):
    # 功能：自动检索 arXiv / Semantic Scholar
    # 近3年顶会论文，去重、过滤、排序
    papers = search_semantic_scholar(state["keywords"])
    papers += search_arxiv(state["keywords"])
    papers = deduplicate_and_filter(papers)
    return {"papers": papers}

# ===================== Agent 3：领域分析Agent =====================
def field_analysis_agent(state: ResearchState):
    # 功能：分析研究热点、空白点、现有不足
    titles = [p["title"] for p in state["papers"]]
    overview = llm_analyze_field(titles)
    return {"field_overview": overview}

# ===================== Agent 4：选题生成Agent =====================
def topic_generation_agent(state: ResearchState):
    # 功能：生成3条科研选题
    # 每条包含：名称、创新点、可行性、参考文献
    topics = llm_generate_topics(
        state["user_input"],
        state["field_overview"]
    )
    return {"topic_paths": topics}

# ===================== Agent 5：收敛决策Agent =====================
def decision_converge_agent(state: ResearchState):
    # 功能：评估选题 → 推荐最优 → 生成证据链
    recommendation, evidence = llm_judge_best_topic(
        state["topic_paths"],
        state["field_overview"]
    )
    return {
        "final_recommendation": recommendation,
        "evidence_chain": evidence
    }

# ===================== 多Agent工作流编排 =====================
def build_workflow():
    workflow = StateGraph(ResearchState)
    
    # 注册5个Agent节点
    workflow.add_node("parse", parse_requirement_agent)
    workflow.add_node("retrieve", paper_retrieve_agent)
    workflow.add_node("analyze", field_analysis_agent)
    workflow.add_node("generate", topic_generation_agent)
    workflow.add_node("judge", decision_converge_agent)

    # 定义执行顺序（流水线协作）
    workflow.add_edge("parse", "retrieve")
    workflow.add_edge("retrieve", "analyze")
    workflow.add_edge("analyze", "generate")
    workflow.add_edge("generate", "judge")
    workflow.add_edge("judge", END)

    workflow.set_entry_point("parse")
    return workflow.compile()

# ===================== 执行入口 =====================
if __name__ == "__main__":
    app = build_workflow()
    result = app.invoke({
        "user_input": "我想做大模型RAG方向研究",
        "keywords": [],
        "papers": [],
        "field_overview": {},
        "topic_paths": [],
        "final_recommendation": {},
        "evidence_chain": []
    })
    print("=== Final Recommendation ===")
    print(result["final_recommendation"])
    print("=== Evidence Chain ===")
    print(result["evidence_chain"])