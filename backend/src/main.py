import asyncio

import uvicorn
from asgi import create_asgi_application


async def main():
    app = await create_asgi_application()
    config = uvicorn.Config(app, host="0.0.0.0", port=5000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
