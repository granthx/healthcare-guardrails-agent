import sys
import uuid
from pathlib import Path

# Ensure root directory is on sys.path when executed via streamlit run app/ui.py
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from langgraph.types import Command
from app.agent import healthcare_bot

st.set_page_config(
    page_title="Healthcare Guardrails Agent",
    page_icon="🛡️",
    layout="wide",
)

st.title("Healthcare Guardrails Agent")
st.caption("LangChain + LangGraph • Safety • PII • HITL • Output Validation")

with st.sidebar:
    st.subheader("Guardrail Stack")
    st.markdown(
        """
        - Safety/domain filter
        - Email redaction
        - Credit-card masking
        - Human approval for booking
        - Medical disclaimer validator
        - LangGraph checkpointing
        """
    )
    st.warning(
        "Educational demo only. This is not a diagnosis or clinical "
        "decision-making system."
    )

if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"streamlit-{uuid.uuid4()}"

if "pending_hitl" not in st.session_state:
    st.session_state.pending_hitl = False

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask a healthcare or appointment question...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    result = healthcare_bot.invoke(
        {"messages": [{"role": "user", "content": prompt}]},
        config=config,
    )

    if "__interrupt__" in result:
        st.session_state.pending_hitl = True
        st.warning("Human approval is required before the appointment can be booked.")
        st.json(result["__interrupt__"])
        st.rerun()

    answer = result["messages"][-1].content
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

if st.session_state.pending_hitl:
    st.divider()
    st.subheader("Human approval required")

    col1, col2 = st.columns(2)
    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    with col1:
        if st.button("Approve appointment", type="primary"):
            result = healthcare_bot.invoke(
                Command(resume={"decisions": [{"type": "approve"}]}),
                config=config,
            )
            st.session_state.pending_hitl = False
            answer = result["messages"][-1].content
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
            st.rerun()

    with col2:
        if st.button("Reject appointment"):
            result = healthcare_bot.invoke(
                Command(resume={"decisions": [{"type": "reject"}]}),
                config=config,
            )
            st.session_state.pending_hitl = False
            answer = result["messages"][-1].content
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
            st.rerun()
