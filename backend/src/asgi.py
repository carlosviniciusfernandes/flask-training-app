from asgiref.wsgi import WsgiToAsgi, WsgiToAsgiInstance
from db import init_mongo
from flask import Flask


async def create_asgi_application() -> WsgiToAsgiInstance:
    app = Flask(__name__)

    await init_mongo()

    with app.app_context():
        from apis import add_review, add_user

    return WsgiToAsgi(app)
