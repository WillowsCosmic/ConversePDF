from llama_index.llms.gemini import Gemini  
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.gemini import GeminiEmbedding
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

client = Gemini(api_key=os.getenv("GEMINI_API_KEY"), model="gemini-2.5-flash")
embed_model = GeminiEmbedding(model_name="models/text-embedding-004")
EMBED_DIM = 768

splitter = SentenceSplitter(chunk_size=1000,chunk_overlap=200)

def load_and_chunk_pdf(path:str):
    docs = PDFReader().load_data(file=Path(path))
    texts = [d.text for d in docs if getattr(d,"text",None)]
    chunks = []
    for t in texts:
        chunks.extend(splitter.split_text(t))
    return chunks

def embed_texts(texts: list[str]) -> list[list[float]]:
    #use the model directly
    embeddings = embed_model.get_text_embedding_batch(texts)
    return embeddings