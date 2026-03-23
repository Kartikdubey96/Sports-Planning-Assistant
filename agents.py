from crewai import Agent, LLM
from crewai_tools import SerperDevTool
from my_sports_tools import check_resource
import os

# 1. Initialize the Search Tool
search_tool = SerperDevTool(search_kwargs={"num": 3})

# 2. Define the Cloud Brain (Swapped to Gemini for Production!)
cloud_llm = LLM(
    model="gemini/gemini-2.5-flash",  # <--- Updated to the active 2.5 model
    temperature=0.1,
    api_key=os.environ.get("AIzaSyATLqdn-yQykP2RDj1-pwG2AcuVEPY2HDc")
)

# --- THE AGENTS ---

planner_agent = Agent(
    role='Lead Sports Planner',
    goal='Research real-time data using web search and break down the next steps for analysis.',
    backstory="""You are a world-class sports strategist. You leverage data from sources like 
    Cricbuzz to ensure plans are based on current match conditions and live statistics.
    
    CRITICAL RULES: 
    1. You ONLY have access to the Search tool. 
    2. DO NOT attempt to use the 'check_resource' tool. Leave resource checking to the Validator agent.
    3. Do not use conversational filler. Do not use <think> tags in your final output. 
    4. Just execute your search tool using the exact Thought/Action format provided to you.""",
    llm=cloud_llm, # <--- Updated
    tools=[search_tool],
    allow_delegation=False,
    verbose=True,
    max_iter=5
)

analyst_agent = Agent(
    role='Resource Validator',
    goal='Validate tool availability and generate a final execution schedule.',
    backstory="""You are a technical feasibility expert. You verify that required databases 
    (like MatchStats_DB) are online and ready. You finalize the timeline for execution.
    
    CRITICAL RULES: Adhere strictly to the format required to use tools. Do not loop.""",
    llm=cloud_llm, # <--- Updated
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
    llm=cloud_llm, # <--- Updated
    allow_delegation=False,
    verbose=True
)