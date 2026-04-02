# Research Topic Agent
科研选题智能助手 · 多智能体协作系统

一个基于 LangGraph 多 Agent 架构的科研选题推荐系统。  
当前版本为可运行 MVP：已打通“需求解析 -> 文献检索 -> 领域分析 -> 选题生成 -> 收敛决策”完整流程，并输出推荐结果与证据链。

## 架构
- 需求解析 Agent
- 文献检索 Agent
- 领域分析 Agent
- 选题生成 Agent
- 收敛决策 Agent

基于 LangGraph 实现流水线式多智能体协作。

## 功能
- 输入研究方向 → 自动生成关键词
- 自动检索（当前为 mock 数据，可替换为 arXiv / Semantic Scholar）
- 分析领域热点与研究空白
- 生成 3 条结构化候选选题
- 输出最优选题 + 证据链

## 技术栈
- Python
- LangChain / LangGraph
- requests（后续可接 Academic API）

## 项目结构

```text
research-topic-agent/
├── main.py                                  # 多 Agent 工作流主入口
├── requirements.txt
├── README.md
├── multi_agent_architecture_homework.md     # 作业配套说明
└── tests/
    └── test_workflow.py                     # 基础端到端测试
```

## 运行方式

```bash
pip install -r requirements.txt
python main.py
```

## 测试

```bash
pytest -q
```

## 后续扩展建议

1. 把 `search_semantic_scholar` / `search_arxiv` 从 mock 替换为真实 API 调用。
2. 将 5 个 Agent 拆分到独立模块，降低 `main.py` 复杂度。
3. 增加异常处理（API 超时、空检索、LLM 输出格式错误）。
4. 增加评估指标（选题质量、证据覆盖率、收敛时间）。