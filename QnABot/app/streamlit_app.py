import streamlit as st
from workflows.qa_graph import build_qa_graph
from agents.extractor_agent import extractor_agent
from agents.summarizer_agent import summarizer_agent
from agents.qa_agent import qa_agent
import os
import tempfile

st.set_page_config(page_title="Smart PDF QA", layout="centered")

st.title("📄💬 Smart PDF Q&A Chat")
st.markdown("Upload a PDF and start chatting with it!")

# === 1. Upload File ===
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None

if "summary" not in st.session_state:
    st.session_state.summary = None

if "messages" not in st.session_state:
    st.session_state.messages = []

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file and st.button("📄 Process PDF"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Extracting and summarizing..."):
        extracted = extractor_agent(tmp_path)
        summary = summarizer_agent(extracted)
        st.session_state.pdf_text = extracted
        st.session_state.summary = summary
        st.session_state.messages = []  # reset conversation

    st.success("PDF processed and summarized!")

# === 2. Chat Interface ===
if st.session_state.summary:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask a question about the document...")
    if user_input:
        # Save user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = qa_agent(st.session_state.summary, user_input)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
