from apis import register_blueprints
from db import init_mongo
from quart import Quart

app = Quart(__name__)


@app.before_serving
async def startup():
    await init_mongo()


register_blueprints(app)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
