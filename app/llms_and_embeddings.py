from langchain_openai import ChatOpenAI
from langsmith.wrappers import wrap_openai
from langchain_huggingface import HuggingFaceEmbeddings
import openai
import config_setup

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.6)
client = wrap_openai(openai.Client())

embeddings_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embeddings = HuggingFaceEmbeddings(model_name=embeddings_model_name)
