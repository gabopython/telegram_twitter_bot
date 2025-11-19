import asyncio
import uvicorn
from fastapi_server import app, set_bot_instance
from telegram_bot import start_bot, get_bot
from config import fastapi_host, fastapi_port, callback_url


async def run_fastapi():
    """Run FastAPI server"""
    config = uvicorn.Config(
        app,
        host=fastapi_host,
        port=fastapi_port,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    
    # Set bot instance for FastAPI
    bot = get_bot()
    set_bot_instance(bot)
    
    # Run both servers concurrently
    await asyncio.gather(
        run_fastapi(),
        start_bot()
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down...")