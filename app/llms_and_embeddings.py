from langchain_openai import ChatOpenAI
from langsmith.wrappers import wrap_openai
from langchain_huggingface import HuggingFaceEmbeddings
import openai
import config_setup
import os

model=os.getenv("MODEL_NAME")

llm = ChatOpenAI(model_name=model, temperature=0.6)
client = wrap_openai(openai.Client())

embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
