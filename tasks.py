from crewai import Task

# Notice the third argument here: 'reporter'
def create_tasks(planner, analyst, reporter):
    
    # Task 1: Research and Plan
    research_task = Task(
        description="""1. Use the search tool to find the latest live score and match 
        summary for {goal} on Cricbuzz or similar sites.
        2. Based on the real-time data found, break down the next steps for a full 
        statistical analysis (including player form and key partnerships).
        Note: The current real-world time is {current_time}.""",
        expected_output="""A detailed report containing the current live score, 
        match summary, and a 5-step technical plan for deep match analysis.""",
        agent=planner
    )

    # Task 2: Validate and Schedule
    validation_task = Task(
        description="""1. Review the analysis plan and match data from the Lead Planner.
        2. Use the check_resource tool to verify if 'MatchStats_DB' is ONLINE 
        to store this new data.
        3. Create a realistic 30-minute execution schedule for the data team. 
        IMPORTANT: The schedule must start EXACTLY at the current time: {current_time}.""",
        expected_output="""A confirmation of database status and a finalized 30-minute 
        execution timeline starting from {current_time}.""",
        agent=analyst
    )

    # Task 3: The New Summarizer Task
    reporting_task = Task(
        description="""Review the match stats from the Planner and the timeline from the Analyst. 
        Combine them into a single, cohesive Executive Report.""",
        expected_output="""A beautifully formatted Markdown report containing:
        1. 🏏 MATCH SUMMARY (Must include the exact scores and player names found by the planner)
        2. ⚙️ TECHNICAL PLAN (The 5-step analysis plan)
        3. 🗄️ DATABASE & TIMELINE (The DB status and the real-time schedule)""",
        agent=reporter,
        context=[research_task, validation_task] # This feeds Task 1 and 2 into Task 3
    )

    # Make sure we return all THREE tasks
    return [research_task, validation_task, reporting_task]
