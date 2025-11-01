from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool
import os
import json

load_dotenv()

# Verify Groq API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY not found in .env file")
    exit(1)

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Initialize Groq LLM with tool-calling compatible model
llm = ChatGroq(
    model="llama-3.1-8b-instant",  # Best for tool calling
    temperature=0.5,
    max_tokens=8192,
    groq_api_key=api_key
)

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that helps generate research papers.
            Use the available tools to gather comprehensive information.
            
            After using tools, output ONLY a valid JSON object (no markdown, no extra text):
            {{
                "topic": "the research topic",
                "summary": "comprehensive summary combining all findings",
                "sources": ["Wikipedia", "Web Search"],
                "tools_used": ["wikipedia_search", "web_search"]
            }}
            
            {format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

print("🔬 AI Research Assistant (Powered by Groq)")
print("=" * 60)

query = input("\nWhat can I help you research? ")

try:
    raw_response = agent_executor.invoke({"query": query})
    
    output_text = raw_response.get("output", "")
    
    # Try to parse as JSON
    try:
        data = json.loads(output_text)
        
        # Unwrap if there's a "properties" key
        if isinstance(data, dict) and "properties" in data:
            data = data["properties"]
        
        structured_response = ResearchResponse(**data)
        
    except (json.JSONDecodeError, ValueError):
        # Fallback: try the parser
        structured_response = parser.parse(output_text)
    
    # Display results
    print("\n" + "="*60)
    print("✅ Research Complete!")
    print("="*60)
    print(f"\n📌 Topic: {structured_response.topic}")
    print(f"\n📝 Summary:\n{structured_response.summary}")
    print(f"\n📚 Sources: {', '.join(structured_response.sources)}")
    print(f"\n🔧 Tools Used: {', '.join(structured_response.tools_used)}")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nTroubleshooting: Check if GROQ_API_KEY is valid and tools are working")
