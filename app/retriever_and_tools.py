from langchain_community.vectorstores import FAISS, Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import llms_and_embeddings
from langchain.tools.retriever import create_retriever_tool
from db_interaction import db
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_community.document_loaders import DirectoryLoader
from pathlib import Path

import ast
import re

def query_as_list(db, query, label):
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [label + ": " + re.sub(r'\b\d+\b', '', string).strip() for string in res]
    return list(set(res))

script_dir = Path(__file__).resolve().parent
docs_dir = script_dir.parent / 'docs'

paths = [str(docs_dir)+"/trapreadme.md", str(docs_dir)+"/trapextendeddoc.md"]
docs = [TextLoader(path).load() for path in paths]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=520, chunk_overlap=100
)
doc_splits = text_splitter.split_documents(docs_list)

vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=llms_and_embeddings.embeddings,
)
retriever = vectorstore.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_trap_documentation",
    "Search and return information about the TRAP (Test result Analysis Platform) web application documentation and on the TRAP package, concerning scripting procedures, coding, tutorials, files, jobs, permissions, and other relevant information.",
)

step_activities = query_as_list(db, "SELECT sa.step_activity_name FROM cvg_step_activity sa", "Step Activity Name")
steps = query_as_list(db, "SELECT s.step_name FROM cvg_step s", "Ste Namep")
output_names = query_as_list(db, "SELECT ao.archetype_output_name FROM cvg_archetype_output ao JOIN cvg_archetype a ON ao.archetype_id = a.archetype_id", "Archetype Output Name")
archetype_names = query_as_list(db, "SELECT archetype_name FROM cvg_archetype", "Archetype Name")

# Merge all the labeled lists into one
combined_list = step_activities + steps + output_names + archetype_names

# Create a single FAISS vector database and retriever for the combined list
combined_vector_db = FAISS.from_texts(combined_list, llms_and_embeddings.embeddings)
combined_retriever = combined_vector_db.as_retriever(search_kwargs={"k": 6})

# Create a description for the merged retriever tool
combined_description = """Use this tool to look up proper name values across step activities, steps, archetype outputs, and archetype names. 
Input is an approximate spelling of the proper noun, and the output is valid proper nouns with their respective categories."""

# Create the merged retriever tool
search_proper_names = create_retriever_tool(
    combined_retriever,
    name="search_proper_names",
    description=combined_description,
)