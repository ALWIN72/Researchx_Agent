AI Research Assistant
An intelligent research assistant powered by Groq's ultra-fast LLM inference and LangChain agents. This tool autonomously searches the web, queries Wikipedia, and generates comprehensive research summaries on any topic.

Python
LangChain
Groq
License

✨ Features
🤖 Autonomous Research: Uses LangChain agents with tool calling capabilities

⚡ Ultra-Fast Inference: Powered by Groq's lightning-fast LLM API (up to 750 tokens/sec)

🔍 Multi-Source Research: Combines web search (DuckDuckGo) and Wikipedia

💾 Auto-Save: Automatically saves research outputs with timestamps

📊 Structured Output: Returns research in well-formatted JSON with sources cited

🛠️ Extensible Tools: Easy to add new research tools and capabilities

🚀 Demo
bash
🔬 AI Research Assistant (Powered by Groq)
============================================================

What can I help you research? quantum computing applications

> Entering new AgentExecutor chain...
[Agent uses web_search and wikipedia_search tools...]
> Finished chain.

============================================================
✅ Research Complete!
============================================================

📌 Topic: quantum computing applications

📝 Summary:
Quantum computing has diverse applications across multiple fields including...
[comprehensive summary combining findings from multiple sources]

📚 Sources: Wikipedia, Web Search

🔧 Tools Used: wikipedia_search, web_search
============================================================
📋 Prerequisites
Python 3.9 or higher

Groq API key (Get one free here https://console.groq.com/keys)

