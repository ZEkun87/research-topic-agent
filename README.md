# Research Topic Agent
科研选题智能助手 · 多智能体协作系统

一个基于大模型与多Agent架构的自动化科研选题推荐系统，可根据用户研究兴趣自动完成文献检索、领域分析、创新选题生成与最优决策。

## 架构
- 需求解析 Agent
- 文献检索 Agent
- 领域分析 Agent
- 选题生成 Agent
- 收敛决策 Agent

基于 LangGraph 实现流水线式多智能体协作。

## 功能
- 输入研究方向 → 自动生成关键词
- 自动检索 arXiv / Semantic Scholar 学术文献
- 分析领域热点、研究空白
- 生成 3 条可直接用于论文的科研选题
- 输出最优选题 + 证据链

## 技术栈
- Python
- LangChain / LangGraph
- LLM API
- Academic API (arXiv / Semantic Scholar)

## 运行
```bash
pip install -r requirements.txt
python main.py