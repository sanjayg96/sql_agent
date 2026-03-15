# Datalogue: Democratizing Enterprise Data Access

**Live Demo:** [Try Datalogue Here](https://sqlagent-uhtpvkmjt4r5zomm6ayk9o.streamlit.app/)

An autonomous, LLM-powered SQL agent designed to bridge the gap between non-technical business stakeholders and complex relational databases. Built with Python, Streamlit, and LangChain, this application acts as a virtual data analyst capable of reasoning through database schemas, writing multi-table SQL joins, executing queries, and maintaining conversational context for follow-up questions.

## The Pain Point
In most organizations, business intelligence (BI) dashboards are static. While standard BI copilots can answer simple questions based on pre-aggregated dashboard views, they fail when stakeholders need ad-hoc insights requiring complex, multi-table joins or iterative reasoning. 

Consequently, finance, accounting, and operational teams must submit ticketing requests to Data Science or Data Engineering teams just to pull specific numbers. This creates massive bottlenecks, delays critical business decisions, and wastes the data team's time on repetitive querying.

## The Solution
This project introduces an **Agentic AI Workflow** that interacts directly with the database. Instead of relying on pre-built views, the agent:
1. Receives a natural language question.
2. Autonomously inspects the database schema and data dictionary.
3. Formulates a syntactically correct SQL query.
4. Self-corrects if it encounters execution errors.
5. Returns the final analytical answer alongside a fully transparent execution trace.

## Key Features
* **Conversational Memory:** Supports continuous follow-up questions without losing context (e.g., "Who is our top client?" -> "What country are they from?").
* **Execution Transparency:** Built-in tracing allows users to open an expander and view the exact thought process and SQL queries executed by the agent, ensuring trust and auditability for critical business decisions.
* **Agentic Reasoning:** Utilizes OpenAI's function-calling to dynamically choose between tools (like syntax checkers vs. direct execution) based on query complexity.

## Business Impact & Value
While deployed as a proof-of-concept using the open-source Chinook database, the architecture is designed for enterprise scalability. 
* **Turnaround Time Reduction:** Reduces ad-hoc data request times from days (via ticketing systems) to seconds.
* **Resource Optimization:** Frees up Data Science and Engineering teams to focus on strategic, high-impact predictive modeling rather than routine SQL pulls.
* **Trust & Verifiability:** Unlike "black box" LLMs, the visible execution trace guarantees that human operators can verify the exact logic used to generate financial or operational metrics.

## Tech Stack
* **Frontend:** Streamlit
* **Agent Framework:** LangChain
* **LLM:** OpenAI
* **Database:** SQLite (Chinook Dataset)
* **Environment Management:** `uv`

---
*Note: To run this locally, ensure you have set up a `.env` file with your `OPENAI_API_KEY`.*