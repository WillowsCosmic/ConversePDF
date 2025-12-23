#In this file it will have the logic for creating an api
#We will use decorator to wrap the api endpoint

import logging
from fastapi import FastAPI
import inngest
import inngest.fast_api
from inngest.experimental import ai
from dotenv import load_dotenv
import uuid
import os
import datetime
from data_loader import load_and_chunk_pdf,embed_texts
from vector_db import QdrantStorage
from custom_types import RAGChunkAndSrc, RAGUpsertResult, RAGSearchResult, RAGQueryResult

#load the environmental variables in the dotenv file
load_dotenv()

inngest_client = inngest.Inngest(
    app_id="rag_app",
    logger=logging.getLogger("uvicorn"),
    is_production=False, #disable the production
    serializer=inngest.PydanticSerializer() #PydanticSerializer is a typing system that defines the type of different variables 
)

#inngest function - decorator
@inngest_client.create_function(
    fn_id="ConversePDF: RAG Ingest PDF",
    trigger=inngest.TriggerEvent(event="rag/converse_pdf")
)
async def rag_converse_pdf(ctx: inngest.Context):
    def _load(ctx: inngest.Context) -> RAGChunkAndSrc:  
        pdf_path = ctx.event.data["pdf_path"]
        source_id = ctx.event.data.get("source_id", pdf_path)
        chunks = load_and_chunk_pdf(pdf_path)
        return RAGChunkAndSrc(chunks=chunks, source_id=source_id)

    def _upsert(chunks_and_src: RAGChunkAndSrc) -> RAGUpsertResult:  
        chunks = chunks_and_src.chunks
        source_id = chunks_and_src.source_id
        
        vecs = embed_texts(chunks)
        
        ids = [
            str(uuid.uuid5(uuid.NAMESPACE_URL, name=f"{source_id}:{i}")) 
            for i in range(len(chunks))
        ]
        
        payloads = [
            {"source": source_id, "text": chunks[i]} 
            for i in range(len(chunks))
        ]
        
        QdrantStorage().upsert(ids, vecs, payloads)
        
        return RAGUpsertResult(ingested=len(chunks))

    # Step 1
    chunks_and_src = await ctx.step.run(
        "load-and-chunk",
        lambda: _load(ctx),
        output_type=RAGChunkAndSrc
    )
    
    # Step 2
    ingested = await ctx.step.run(
        "embed-and-upsert",
        lambda: _upsert(chunks_and_src),
        output_type=RAGUpsertResult
    )

    return ingested.model_dump()
app = FastAPI()

inngest.fast_api.serve(app,inngest_client,[rag_converse_pdf]) #[] is the inngest function and will connect with the inngest dev server

