# 科研选题智能Agent系统
# 架构：LangGraph 多Agent协作流程
# 包含：解析Agent、检索Agent、分析Agent、选题Agent、决策Agent

from typing import TypedDict, List, Dict

# 全局状态（多Agent共享数据）
class ResearchState(TypedDict):
    user_input: str          # 用户研究兴趣
    keywords: List[str]      # 检索关键词
    papers: List[Dict]       # 文献列表
    field_overview: Dict     # 领域全景
    topic_paths: List[Dict]  # 3条候选选题
    final_recommendation: Dict
    evidence_chain: List[Dict]

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