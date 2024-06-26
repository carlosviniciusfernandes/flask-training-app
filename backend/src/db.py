import os

from beanie import init_beanie
from models import User
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT", 27017)
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")


async def init_mongo(mock=False) -> AsyncIOMotorDatabase:
    if mock:
        from mongomock_motor import AsyncMongoMockClient

        mongo_client = AsyncMongoMockClient()
    else:
        connection_string = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
        mongo_client = AsyncIOMotorClient(connection_string)

    await init_beanie(database=mongo_client.db_name, document_models=[User])
    return mongo_client
