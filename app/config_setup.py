import os
import dotenv
import config

dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"]=config.OPEN_AI_API_KEY
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"]=config.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"]="gpt-4o-mini"
os.environ["HUGGINGFACEHUB_API_TOKEN"]=config.HUGGINGFACEHUB_API_TOKEN

db_config = {
    "user": os.getenv("DB_USER"),
    "secret": os.getenv("DB_SECRET"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
}