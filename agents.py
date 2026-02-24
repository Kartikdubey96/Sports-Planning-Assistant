from crewai import Agent, LLM
from crewai_tools import SerperDevTool
from my_sports_tools import check_resource

# 1. Initialize the Search Tool
# Ensure os.environ["SERPER_API_KEY"] is set in your main.py
search_tool = SerperDevTool()

# 2. Define the local LLM with the DeepSeek-R1 System Template 
local_llm = LLM(
    model="ollama/deepseek-r1:8b",
    base_url="http://localhost:11434",
    system_template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a professional sports analyst and strategist. 
    When asked to perform a task, first reason internally, then provide your 
    final answer clearly using the 'Final Answer:' prefix.
    Follow the requested output format strictly.<|eot_id|>""",
    temperature=0.3
)

# 3. Define the Planner Agent
planner_agent = Agent(
    role='Lead Sports Planner',
    goal='Decompose {goal} into actionable steps and research real-time data using web search.',
    backstory="""You are a world-class sports strategist known for high-precision 
    planning. You leverage real-time data from sources like Cricbuzz to ensure 
    that execution plans are based on current match conditions, player form, and 
    live statistics.""",
    llm=local_llm,
    tools=[search_tool],
    allow_delegation=False,
    verbose=True
)

# 4. Define the Validator Agent
analyst_agent = Agent(
    role='Resource Validator',
    goal='Validate tool availability and generate a final execution schedule.',
    backstory="""You are a technical feasibility expert. Your job is to take 
    the research and steps provided by the Lead Planner and verify that the 
    required databases (like MatchStats_DB) are online and ready for 
    data processing. You finalize the timeline for execution.""",
    llm=local_llm,
    tools=[check_resource],
    allow_delegation=False,
    verbose=True
)