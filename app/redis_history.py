from redis_server import initialize_async_pool, initialize_sync_pool, RedisSaver
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver
from urllib.parse import quote
import config

pwd = quote(config.REDIS_PWD)


#Replace loclahost with actual redis server address + pwd

sync_redis_direct = initialize_sync_pool(host="localhost", port=6379, db=0)
async_pool = initialize_async_pool(url='redis://localhost:6379/0')

checkpointerredis = RedisSaver(sync_connection=sync_redis_direct, async_connection=async_pool)
checkpointer = MemorySaver()