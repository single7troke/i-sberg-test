from aioredis import create_redis_pool
import os


async def init_redis_pool():
    redis = await create_redis_pool(
        f"{os.environ['REDIS_URL']}:{os.environ['REDIS_PORT']}",
        password=os.environ['REDIS_PASSWORD'],
        encoding="utf-8",
        db=int(os.environ['REDIS_DB'])
    )
    return redis
