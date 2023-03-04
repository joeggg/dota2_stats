"""
    App main entry point
"""

import logging

from .app import create_app
from .utils import set_up_logger, StaticObjects


set_up_logger()
StaticObjects.setup()
app = create_app()


@app.get("/status")
async def status():
    """Test command"""
    logging.info("Received status command")
    return "Hello world!"
