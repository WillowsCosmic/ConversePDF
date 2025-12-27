
# ConversePDF 🤖📄

> AI-powered document Q&A application that lets users upload PDFs and ask questions about them using Retrieval-Augmented Generation (RAG)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-RAG-orange)

## 🌟 Features

- **PDF Upload & Processing**: Upload any PDF document for analysis
- **Intelligent Q&A**: Ask natural language questions about your documents
- **Semantic Search**: Retrieves relevant chunks using vector embeddings
- **RAG Architecture**: Combines retrieval with Google Gemini LLM for accurate answers
- **Asynchronous Processing**: Background jobs for efficient document processing
- **Vector Database**: Persistent storage using Qdrant for embeddings
- **Modern UI**: Clean, intuitive interface built with Streamlit

## 🏗️ Architecture

```
┌─────────────┐
│  Streamlit  │  ← User Interface
└──────┬──────┘
       │
┌──────▼──────┐
│   FastAPI   │  ← Backend API
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
┌──▼───┐ ┌─▼────────┐
│Qdrant│ │ LlamaIndex│  ← Vector DB & RAG
└──────┘ └─┬────────┘
           │
      ┌────▼────┐
      │ Gemini  │  ← LLM (gemini-2.5-flash)
      └─────────┘
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: RESTful API framework
- **LlamaIndex**: RAG orchestration and document processing
- **Qdrant**: Vector database for embeddings storage
- **Google Gemini 2.5 Flash**: Large Language Model
- **PyMuPDF**: PDF parsing and text extraction
- **uvloop**: High-performance async event loop

### Frontend
- **Streamlit**: Interactive web interface
- **Requests**: HTTP client for API communication

### Infrastructure
- **Docker**: Qdrant containerization
- **Python 3.12**: Core language
- **Virtual Environment**: Dependency isolation

## 📋 Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/WillowsCosmic/ConversePDF.git
cd ConversePDF
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Start Qdrant Vector Database

```bash
docker-compose up -d
```

This starts Qdrant on `http://localhost:6333`

## 💻 Usage

### Start the Backend Server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Start the Frontend

In a new terminal (with virtual environment activated):

```bash
streamlit run streamlit_app.py
```

The UI will open automatically at `http://localhost:8501`

### Using the Application

1. **Upload a PDF**: Click "Choose a PDF file" and select your document
2. **Wait for Processing**: The system will chunk and embed your document
3. **Ask Questions**: Type your question in the text input
4. **Adjust Retrieval**: Use the slider to control how many chunks to retrieve (default: 5)
5. **Get Answers**: Click "Ask" to receive AI-generated responses with source citations

## 📁 Project Structure

```
ConversePDF/
├── main.py                 # FastAPI backend application
├── streamlit_app.py        # Streamlit frontend
├── data_loader.py          # PDF processing & embedding logic
├── vector_db.py            # Qdrant vector database operations
├── custom_types.py         # Type definitions
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Qdrant container configuration
├── .gitignore             # Git ignore rules
├── .python-version        # Python version specification
├── pyproject.toml         # Project metadata
├── uv.lock                # Dependency lock file
├── qdrant_storage/        # Qdrant data persistence
└── notes.md               # Development notes
```

## 🔧 Configuration

### Chunking Parameters

In `data_loader.py`, you can adjust:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Characters per chunk
    chunk_overlap=200,      # Overlap between chunks
    length_function=len,
)
```

### Retrieval Settings

In `streamlit_app.py`, modify the slider range:

```python
top_k = st.slider("How many chunks to retrieve", 1, 10, 5)
```

### LLM Model

In `data_loader.py`, change the Gemini model:

```python
client = Gemini(api_key=os.getenv("GEMINI_API_KEY"), model="gemini-2.5-flash")
```

## 🧪 API Endpoints

### `POST /upload`
Upload a PDF file for processing

**Request**: Multipart form-data with PDF file
**Response**: 
```json
{
  "message": "PDF uploaded successfully",
  "filename": "document.pdf",
  "job_id": "abc123"
}
```

### `POST /ask`
Ask a question about the uploaded PDF

**Request**:
```json
{
  "question": "What is an involute?",
  "top_k": 5
}
```

**Response**:
```json
{
  "answer": "An involute is a curve traced by...",
  "sources": ["/path/to/document.pdf"]
}
```

## 🐛 Troubleshooting

### Qdrant Connection Issues

```bash
# Check if Qdrant is running
docker ps

# Restart Qdrant
docker-compose down
docker-compose up -d
```

### Import Errors

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### API Key Errors

Ensure your `.env` file exists and contains:
```env
GEMINI_API_KEY=your_actual_key
```

## Screenshots
<img width="1920" height="1079" alt="Screenshot from 2025-12-27 10-39-24" src="https://github.com/user-attachments/assets/357a8e1c-7dd2-4931-b994-98420920ee4a" />

<img width="1920" height="1079" alt="Screenshot from 2025-12-27 10-39-44" src="https://github.com/user-attachments/assets/f7dab7ef-251e-4e05-b5e9-e4cbe9611d7d" />


## 📚 Key Technologies Explained

### RAG (Retrieval-Augmented Generation)
Combines document retrieval with LLM generation:
1. **Chunk**: Split documents into manageable pieces
2. **Embed**: Convert chunks to vector representations
3. **Store**: Save embeddings in vector database
4. **Retrieve**: Find most relevant chunks for user query
5. **Generate**: LLM creates answer using retrieved context

### Vector Database (Qdrant)
Stores document embeddings and enables semantic search based on similarity rather than keyword matching.

### LlamaIndex
Orchestrates the RAG pipeline, handling document loading, chunking, embedding, and querying.


## 🙏 Acknowledgments

- Built as a learning project to understand RAG architecture
- Powered by Google's Gemini LLM
- Uses open-source tools: FastAPI, Streamlit, LlamaIndex, Qdrant

---
