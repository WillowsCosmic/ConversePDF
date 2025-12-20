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
    return {"hello" : "world"}

app = FastAPI()

inngest.fast_api.serve(app,inngest_client,[rag_converse_pdf]) #[] is the inngest function and will connect with the inngest dev server

