import sys
import os
import streamlit as st
import datetime
from dotenv import load_dotenv

# 1. Load secure keys from the .env file
load_dotenv()

# 2. Pre-Flight Check: Ensure keys are actually loaded before running
if not os.getenv("GEMINI_API_KEY") or not os.getenv("SERPER_API_KEY"):
    st.error("🚨 Missing API Keys! Please add GEMINI_API_KEY and SERPER_API_KEY to your .env file.")
    st.stop()

from crewai import Crew, Process
from agents import planner_agent, analyst_agent, reporter_agent
from tasks import create_tasks

# --- Streamlit Web UI Setup ---
st.set_page_config(page_title="Sports Planning Assistant", page_icon="🏆")
st.title("🏆 AI Sports Planning Assistant")
st.markdown("Powered by CrewAI and Gemini")

# Ask for the goal IN THE BROWSER instead of the terminal
user_goal = st.text_input("Enter your sports analysis goal (e.g., 'Plan a 5K training schedule'):")

# Create a button to start the AI
if st.button("Generate Plan"):
    
    # Only run if the user actually typed something
    if user_goal:
        # Show a loading spinner while the agents work in the background
        with st.spinner(f"Agents are researching and planning for: '{user_goal}'... This may take a minute or two!"):
            
            # 1. Setup the tasks
            my_tasks = create_tasks(planner_agent, analyst_agent, reporter_agent)

            # 2. Define the Crew (Fixed the missing reporter_agent here!)
            sports_crew = Crew(
                agents=[planner_agent, analyst_agent, reporter_agent],
                tasks=my_tasks,
                process=Process.sequential,
                verbose=True
            )

            # 3. Get the current time and Kickoff the Crew
            current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            result = sports_crew.kickoff(inputs={
                'goal': user_goal,
                'current_time': current_time_str  # <--- Passing the missing variable!
            })
        
        # 4. Print the final result directly to the web page!
        st.success("Analysis Complete!")
        st.markdown("### 📊 Final Agent Report")
        
        # Ensure the output renders nicely in the browser
        if hasattr(result, 'raw'):
            st.markdown(result.raw)
        else:
            st.markdown(result)
            
    else:
        st.warning("⚠️ Please enter a goal in the text box first!")