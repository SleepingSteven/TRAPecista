from typing import Any, Dict
import uuid
from fastapi import FastAPI
from requests import Request
import uvicorn
from langserve import add_routes
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import chain
from llms_and_embeddings import llm, embeddings

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple API server using LangChain's Runnable interfaces"
)

# Define the workflow and agents here
from workflow import create_workflow, inp, InputChat, parse  # Import workflow creation logic

async def fetch_session(config: Dict[str, Any], req: Request) -> Dict[str, Any]:
    if "REDIS_SESSION_ID" not in req.session:
        print("Creating new session ID")
        req.session["REDIS_SESSION_ID"] = uuid.uuid4().hex
    session_id = req.session["REDIS_SESSION_ID"]
    config["configurable"]["thread_id"] = session_id
    print("Current session ID:", session_id)
    return config

compiled_workflow = create_workflow()

# Remove comment and add SECRET_KEY env. variable to deploy on server
# app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY, max_age=60 * 60 * 24)


add_routes(
    app,
    RunnableLambda(inp) | compiled_workflow.with_config({"configurable": {"thread_id": "<foo>"}}).with_types(input_type=InputChat, output_type=dict) | parse,
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    #remove comment to use dynamic session history
    #per_req_config_modifier=fetch_session,
    path="/agent",
    playground_type="chat",
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)