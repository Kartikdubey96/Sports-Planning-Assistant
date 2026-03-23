# Sports-Planning-Assistant


This repository contains a simple agent-driven sports analysis framework built using the `crewai` library. The system demonstrates how to build a multi-agent crew that can research live sports data, plan analysis steps, validate resource availability, and produce a final execution schedule.

## 📁 Project Structure

```
agents.py             # Agent definitions and LLM configuration
main.py               # Entry point - orchestrates the Crew and user interaction
my_sports_tools.py    # Custom tools used by agents (e.g. resource checker)
tasks.py              # Task definitions linking planner and analyst agents
requirements.txt      # Python dependencies
```

## ⚙️ Prerequisites

1. **Python 3.11+** installed and available in your PATH (tested on Windows).
2. A local LLM endpoint (e.g. Ollama running `deepseek-r1:8b`).
3. Environment variables:
   - `OPENAI_API_KEY` (set to `NA` if bypassing OpenAI checks for Ollama)
   - `SERPER_API_KEY` (required for web search via `SerperDevTool`)

Example (PowerShell):

```powershell
$env:OPENAI_API_KEY = 'NA'
$env:SERPER_API_KEY = 'your_serper_key'
```

Alternatively, you can hardcode these in `main.py` as shown in the example.

## 📦 Installation

Install required packages:

```powershell
python -m pip install -r requirements.txt
```

## 🚀 Usage

1. Start your local LLM server (e.g. Ollama) so that `http://localhost:11434` is reachable.
2. Run the main script:

```powershell
py -3.11 main.py
```

3. When prompted, enter a sports analysis goal (e.g., "India vs Australia live score").
4. The crew of agents will execute the tasks sequentially and print a final report.

The `planner_agent` will search for live match data and generate a plan. The `analyst_agent` will verify resource availability with `check_resource` and output a schedule.

## 🛠 Customization

- **Agents**: Modify `agents.py` to change roles, backstories, or add tools.
- **Tasks**: Update `tasks.py` to adjust the work flow or add new tasks.
- **Tools**: Add more functions decorated with `@tool` in `my_sports_tools.py` for additional capabilities.


---

