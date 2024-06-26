import asyncio

import pytest
import pytest_asyncio
from db import init_mongo
from main import app


@pytest_asyncio.fixture(scope="session")
async def test_app():
    # NOTE: Gave up on mock the client for now due pkg_resources error
    mongo_client = await init_mongo(mock=False)
    database = mongo_client.db_name

    app.config["TESTING"] = True
    app.config["MOTOR_CLIENT"] = mongo_client
    app.config["DATABASE"] = database

    yield app


@pytest_asyncio.fixture(scope="function")
async def test_client(test_app):
    async with test_app.test_client() as test_client:
        yield test_client

    # Teardown - drop all collections after the test
    # for collection in await test_app.config["DATABASE"].list_collection_names():
    #     await test_app.config["DATABASE"].drop_collection(collection)


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
