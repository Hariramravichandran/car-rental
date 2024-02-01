from fastapi import FastAPI
from db import Database,Database1
from models.config import app_configs



app=FastAPI()

db=Database()
db1=Database1

from aioredis import Redis, create_redis_pool


REDIS_URL = "redis://127.0.0.1"
redis_pool: Redis = None

async def get_redis_pool():
    global redis_pool
    if redis_pool is None:
        redis_pool = await create_redis_pool(REDIS_URL)
    return redis_pool

async def on_startup():
    await db.init_db()
   
    await db1.init_db()
    await get_redis_pool()
    # Hook that runs after the server starts
    cdata = await app_configs()
    print(cdata)
    app.state.config = cdata

  