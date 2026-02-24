from crewai import Task

def create_tasks(planner, analyst):
    # Task 1: Research and Plan
    research_task = Task(
        description="""1. Use the search tool to find the latest live score and match 
        summary for {goal} on Cricbuzz or similar sites.
        2. Based on the real-time data found, break down the next steps for a full 
        statistical analysis (including player form and key partnerships).""",
        expected_output="""A report containing the current live score and a 
        5-step technical plan for deep match analysis based on that score.""",
        agent=planner
    )

    # Task 2: Validate and Schedule
    validation_task = Task(
        description="""1. Review the analysis plan from the Lead Planner.
        2. Use the check_resource tool to verify if 'MatchStats_DB' is ONLINE 
        to store this new data.
        3. Create a final execution schedule for the data team.""",
        expected_output="""A confirmation of database status and a finalized 
        30-minute execution timeline for the analysis.""",
        agent=analyst,
        context=[research_task] # This passes the search results to the analyst
    )

    return [research_task, validation_task]