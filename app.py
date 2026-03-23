import streamlit as st
import os
import sys
import re
from datetime import datetime # <-- Added to get real time

# 1. Path Setup
sys.path.append(os.path.dirname(__file__))

# 2. Stable Imports (Now importing reporter_agent)
try:
    from crewai import Crew, Process
    from agents import planner_agent, analyst_agent, reporter_agent
    from tasks import create_tasks
except Exception as e:
    st.error(f"Environment Error: {e}. Try restarting VS Code.")
    st.stop()

# Disable Telemetry
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# --- THE CLEAN CALLBACK ---
def streamlit_callback(step_output):
    """Refined callback to show clean, formatted agent progress."""
    raw_text = str(step_output)
    
    # 1. Hide internal CrewAI parsing errors from the user
    if "Failed to parse" in raw_text:
        return

    with st.chat_message("ai"):
        # Pull out human-readable parts
        thought = re.search(r"thought=['\"](.*?)['\"]", raw_text, re.DOTALL)
        output = re.search(r"output=['\"](.*?)['\"]", raw_text, re.DOTALL)
        
        # Display Agent's Thought/Strategy
        if thought:
            # Fix newlines but safely preserve emojis!
            clean_thought = thought.group(1).replace('\\n', '\n').strip()
            if clean_thought:  # Don't show empty boxes
                with st.container(border=True):
                    st.markdown("**🤔 Agent Strategy:**")
                    st.info(clean_thought)

        # Display Tool Usage or Result
        if output:
            clean_output = output.group(1).replace('\\n', '\n').strip()
            
            if clean_output in ["{}", "{", "None", ""]:
                with st.status("🔧 Tool active: Searching/Processing...", state="running"):
                    st.write("Fetching live data...")
            else:
                st.success("🏁 **Task Progress**")
                st.markdown(clean_output)

# --- UI CONFIG ---
st.set_page_config(page_title="DeepSeek Sports Analyst", page_icon="🏏", layout="wide")
st.title("🏏 Sports Planning Agent")

with st.sidebar:
    st.title("⚙️ Configuration")
    os.environ["SERPER_API_KEY"] = st.text_input("Serper API Key", value="HIDDEN", type="password")
    st.info("Using Local DeepSeek-R1 (8B) with 3 Agents")

user_goal = st.text_input("What sports data should I analyze?", placeholder="e.g. Latest India vs WI match stats")

# --- EXECUTION ---
if st.button("🚀 Execute Plan"):
    if not user_goal:
        st.warning("Please enter a goal first.")
    else:
        # Attach the callback to ALL THREE agents
        planner_agent.step_callback = streamlit_callback
        analyst_agent.step_callback = streamlit_callback
        reporter_agent.step_callback = streamlit_callback

        with st.status("📡 Agents are working...", expanded=True) as status:
            try:
                # Get the actual current time from your computer
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Pass all 3 agents to create_tasks
                my_tasks = create_tasks(planner_agent, analyst_agent, reporter_agent)
                
                sports_crew = Crew(
                    agents=[planner_agent, analyst_agent, reporter_agent],
                    tasks=my_tasks,
                    process=Process.sequential,
                    verbose=True
                )
                
                # Pass both the goal AND the current time to the LLM
                result = sports_crew.kickoff(inputs={'goal': user_goal, 'current_time': now})
                status.update(label="✅ Success!", state="complete")

                # --- FINAL SUMMARY ---
                st.divider()
                st.subheader("📋 Final Executive Report")
                
                final_report = result.raw if hasattr(result, 'raw') else str(result)
                st.success(final_report.strip("`"))
                
            except Exception as e:
                st.error(f"Run Error: {e}")

st.markdown("---")
st.caption("Powered by CrewAI, Streamlit & Ollama DeepSeek-R1")
