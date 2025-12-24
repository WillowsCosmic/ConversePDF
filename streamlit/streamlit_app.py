import asyncio
from pathlib import Path
import time

import streamlit as st
import inngest
from dotenv import load_dotenv
import os
import requests

load_dotenv()

st.set_page_config(page_title="ConversePDF", page_icon="📄", layout="centered")


def send_rag_ingest_event(pdf_path: Path) -> None:
    event_key = os.getenv('INNGEST_EVENT_KEY')
    response = requests.post(
        f"https://inn.gs/e/{event_key}",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "name": "rag/converse_pdf",
            "data": {
                "pdf_path": str(pdf_path.resolve()),
                "source_id": pdf_path.name,
            }
        }
    )
    response.raise_for_status()


def save_uploaded_pdf(file) -> Path:
    uploads_dir = Path("/tmp/uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)
    file_path = uploads_dir / file.name
    file_bytes = file.getbuffer()
    file_path.write_bytes(file_bytes)
    return file_path


st.title("Upload a PDF to Ingest")
uploaded = st.file_uploader("Choose a PDF", type=["pdf"], accept_multiple_files=False)

if uploaded is not None:
    with st.spinner("Uploading and triggering ingestion..."):
        path = save_uploaded_pdf(uploaded)
        send_rag_ingest_event(path)
    st.success(f"Triggered ingestion for: {path.name}")

st.divider()
st.title("Ask a question about your PDFs")


def send_rag_query_event(question: str, top_k: int):
    event_key = os.getenv('INNGEST_EVENT_KEY')
    response = requests.post(
        f"https://inn.gs/e/{event_key}",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "name": "rag/query_pdf_ai",
            "data": {
                "question": question,
                "top_k": top_k,
            }
        }
    )
    response.raise_for_status()


with st.form("rag_query_form"):
    question = st.text_input("Your question")
    top_k = st.number_input("How many chunks to retrieve", min_value=1, max_value=20, value=5, step=1)
    submitted = st.form_submit_button("Ask")

    if submitted and question.strip():
        send_rag_query_event(question.strip(), int(top_k))
        st.success("Query sent! Check Inngest dashboard for results.")