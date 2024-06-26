from apis import register_blueprints
from db import init_mongo
from exceptions import register_exception_handlers
from quart import Quart

app = Quart(__name__)

register_blueprints(app)
register_exception_handlers(app)


@app.before_serving
async def startup():
    await init_mongo()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
