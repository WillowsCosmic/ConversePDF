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
        "https://api.inngest.com/v1/events",
        headers={
            "Authorization": f"Bearer {event_key}",
            "Content-Type": "application/json"
        },
        json=[{
            "name": "rag/converse_pdf",
            "data": {
                "pdf_path": str(pdf_path.resolve()),
                "source_id": pdf_path.name,
            }
        }]
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
        time.sleep(0.3)
    st.success(f"Triggered ingestion for: {path.name}")
    st.caption("You can upload another PDF if you like.")

st.divider()
st.title("Ask a question about your PDFs")


def send_rag_query_event(question: str, top_k: int) -> str:
    event_key = os.getenv('INNGEST_EVENT_KEY')
    response = requests.post(
        "https://api.inngest.com/v1/events",
        headers={
            "Authorization": f"Bearer {event_key}",
            "Content-Type": "application/json"
        },
        json=[{
            "name": "rag/query_pdf_ai",
            "data": {
                "question": question,
                "top_k": top_k,
            }
        }]
    )
    response.raise_for_status()
    result = response.json()
    return result["ids"][0]


def fetch_runs(event_id: str) -> list[dict]:
    url = f"https://api.inngest.com/v1/events/{event_id}/runs"
    headers = {"Authorization": f"Bearer {os.getenv('INNGEST_EVENT_KEY')}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", [])


def wait_for_run_output(event_id: str, timeout_s: float = 120.0, poll_interval_s: float = 0.5) -> dict:
    start = time.time()
    last_status = None
    while True:
        runs = fetch_runs(event_id)
        if runs:
            run = runs[0]
            status = run.get("status")
            last_status = status or last_status
            if status in ("Completed", "Succeeded", "Success", "Finished"):
                return run.get("output") or {}
            if status in ("Failed", "Cancelled"):
                raise RuntimeError(f"Function run {status}")
        if time.time() - start > timeout_s:
            raise TimeoutError(f"Timed out waiting for run output (last status: {last_status})")
        time.sleep(poll_interval_s)


with st.form("rag_query_form"):
    question = st.text_input("Your question")
    top_k = st.number_input("How many chunks to retrieve", min_value=1, max_value=20, value=5, step=1)
    submitted = st.form_submit_button("Ask")

    if submitted and question.strip():
        with st.spinner("Sending event and generating answer..."):
            event_id = send_rag_query_event(question.strip(), int(top_k))
            output = wait_for_run_output(event_id)
            answer = output.get("answer", "")
            sources = output.get("sources", [])

        st.subheader("Answer")
        st.write(answer or "(No answer)")
        if sources:
            st.caption("Sources")
            for s in sources:
                st.write(f"- {s}")