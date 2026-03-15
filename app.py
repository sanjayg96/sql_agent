import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

# Load environment variables from .env file
load_dotenv()

# UI Configuration
st.set_page_config(page_title="AI Data Analyst", page_icon="📊")
# st.title("📊 Datalogue")
# st.caption("Conversational SQL Agent")

# Instead of st.title
st.markdown("<h1 style='font-size: 30px;'>📊 Datalogue</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='font-size: 18px;'>Conversational SQL Agent</p>", unsafe_allow_html=True
)


# Sidebar Configuration
with st.sidebar:
    st.header("Settings")
    # st.success("API Key loaded from environment.")

    st.markdown("---")
    st.markdown("### Conversation Mode")
    chat_mode = st.radio(
        "Select Mode:",
        ["Single Ad-Hoc Query", "Continuous Conversation"],
        help="Single query resets context. Continuous keeps chat history for follow-ups.",
    )

    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize session state for memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Verify Database exists
db_path = "chinook.db"
absolute_db_path = os.path.abspath(db_path)
if not os.path.exists(absolute_db_path):
    st.error("Database not found. Please run `uv run setup_db.py` first.")
    st.stop()

# Render chat history if in continuous mode
if chat_mode == "Continuous Conversation":
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

# System Prompt / Data Dictionary Injection
# This acts as a custom prefix for the agent. Notice the {dialect} and {top_k}
# which LangChain requires for its internal formatting.
CUSTOM_PREFIX = """You are an expert Data Analyst agent designed to interact with a {dialect} database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.

You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

=== DATA DICTIONARY & SCHEMA NOTES ===
- Customers: Client details. 'CustomerId' is the primary key.
- Employees: Staff details. Sales Support Reps are employees.
- Invoices: Transaction records representing purchases.
- InvoiceLines: Itemized details for each invoice.
- Tracks: Audio tracks available for purchase.
- Albums: Album details, linked to Artists.
- Artists: Band/Artist names.
======================================
"""

# Chat Input
if prompt := st.chat_input("Ask a question about the data..."):
    # Display user prompt in UI
    st.chat_message("user").write(prompt)

    # Manage conversational memory context
    if chat_mode == "Continuous Conversation":
        st.session_state.messages.append({"role": "user", "content": prompt})
        history_context = "\n".join(
            [
                f"{m['role'].capitalize()}: {m['content']}"
                for m in st.session_state.messages[:-1]
            ]
        )
        agent_input = (
            f"Previous Conversation Context:\n{history_context}\n\nNew Question: {prompt}"
            if history_context
            else prompt
        )
    else:
        agent_input = prompt

    # Initialize DB, LLM, and Agent
    db = SQLDatabase.from_uri(f"sqlite:///{absolute_db_path}")

    # ChatOpenAI automatically detects OPENAI_API_KEY from the environment
    llm = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # create_sql_agent imported correctly from langchain_community
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type="openai-tools",
        prefix=CUSTOM_PREFIX,  # Injecting the system prompt/data dictionary here
    )

    # Execute Agent and display trace/response
    with st.chat_message("assistant"):
        # The expand_new_thoughts=False keeps the UI clean until the user actively clicks to expand it
        st_callback = StreamlitCallbackHandler(
            st.container(), expand_new_thoughts=False
        )

        try:
            response = agent_executor.invoke(
                {"input": agent_input}, {"callbacks": [st_callback]}
            )
            output = response["output"]
            st.write(output)

            # Save assistant response to state if in continuous mode
            if chat_mode == "Continuous Conversation":
                st.session_state.messages.append(
                    {"role": "assistant", "content": output}
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
