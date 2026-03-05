from crewai import Agent, LLM
from crewai_tools import SerperDevTool
from my_sports_tools import check_resource

# 1. Initialize the Search Tool (Kept at 3 results to protect your 8GB VRAM)
search_tool = SerperDevTool(search_kwargs={"num": 3})

# 2. Define the DeepSeek-R1 Brain (Clean setup!)
local_llm = LLM(
    model="ollama/deepseek-r1:8b",
    base_url="http://localhost:11434",
    temperature=0.1,
    num_ctx=8192 # Large context window to prevent crashes
)

# --- THE AGENTS ---

planner_agent = Agent(
    role='Lead Sports Planner',
    goal='Research real-time data using web search and break down the next steps for analysis.',
    backstory="""You are a world-class sports strategist. You leverage data from sources like 
    Cricbuzz to ensure plans are based on current match conditions and live statistics.
    
    CRITICAL RULES: Do not use conversational filler. Do not use <think> tags in your final 
    output. Just execute your tools using the exact Thought/Action format provided to you.""",
    llm=local_llm,
    tools=[search_tool],
    allow_delegation=False,
    verbose=True,
    max_iter=5 # Gives it 5 tries to get the tool right
)

analyst_agent = Agent(
    role='Resource Validator',
    goal='Validate tool availability and generate a final execution schedule.',
    backstory="""You are a technical feasibility expert. You verify that required databases 
    (like MatchStats_DB) are online and ready. You finalize the timeline for execution.
    
    CRITICAL RULES: Adhere strictly to the format required to use tools. Do not loop.""",
    llm=local_llm,
    tools=[check_resource],
    allow_delegation=False,
    verbose=True,
    max_iter=3
)

reporter_agent = Agent(
    role="Chief Sports Editor",
    goal="Combine live sports research and technical execution plans into a single markdown report.",
    backstory="""You are a meticulous lead editor. You receive raw match statistics from the 
    Planner and a technical timeline from the Validator. You merge them perfectly without dropping numbers.
    
    CRITICAL RULE: DO NOT invent, hallucinate, or make up sports data. If the match stats 
    are missing, you must explicitly state 'Data Unavailable'. Never write about a different sport.""",
    llm=local_llm,
    allow_delegation=False,
    verbose=True
)
