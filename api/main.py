"""
    App main entry point
"""

import logging

from .utils import app, setup_logger, StaticObjects
from .routes import match, player


setup_logger()
StaticObjects.setup()

app.include_router(match.router)
app.include_router(player.router)


@app.get("/status")
async def status():
    """Test command"""
    logging.info("Received status command")
    return "Hello world!"
