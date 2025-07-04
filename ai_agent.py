import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent

# Get environment variables
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# LLMs
openai_llm = ChatOpenAI(model="gpt-4o-mini")
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")

# Tool
search_tool = TavilySearchResults(max_results=2)
from langchain_core.messages.ai import AIMessage
# System prompt
system_prompt = "Act as an AI chatbot who is smart and friendly"
def get_response_from_ai_agent(llm_id,query,allow_search,system_prompt,provider):
    if provider == "Groq":
        llm = ChatGroq(model = llm_id)
    elif provider == "OpenAI":
        llm = ChatOpenAI(model = llm_id)
    # ✅ CORRECT: Create the agent with proper keywords
    tools = [TavilySearchResults(max_results=2)] if allow_search else []
    agent = create_react_agent(
        llm,               # llm (1st argument)
        tools,          # tools (2nd argument)    
    )

    # Initial state
    state = {"messages": query}

    # Get response
    response = agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]

