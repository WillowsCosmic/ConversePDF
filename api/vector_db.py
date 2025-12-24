# Connect the vector database
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

load_dotenv()


class QdrantStorage:
    def __init__(self, url=None, api_key=None, collection="docs_gemini", dim=768):
        # Read from environment variables if not provided
        url = url or os.getenv("QDRANT_URL", "http://localhost:6333")
        api_key = api_key or os.getenv("QDRANT_API_KEY")
        
        # Connect to Qdrant (cloud or local)
        self.client = QdrantClient(url=url, api_key=api_key, timeout=30)
        self.collection = collection
        
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
            )
    
    def upsert(self, ids, vectors, payloads):
        points = [
            PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) 
            for i in range(len(ids))
        ]
        self.client.upsert(collection_name=self.collection, points=points)
    
    def search(self, query_vector, top_k: int = 5):
        from qdrant_client.models import QueryRequest
        
        results = self.client.query_batch_points(
            collection_name=self.collection,
            requests=[
                QueryRequest(
                    query=query_vector,
                    limit=top_k,
                    with_payload=True
                )
            ]
        )[0].points
        
        context = []
        sources = set()

        for r in results:
            payload = getattr(r, "payload", None) or {}
            text = payload.get("text", "")
            source = payload.get("source", "")
            if text:
                context.append(text)
                sources.add(source)

        return {"contexts": context, "sources": list(sources)}