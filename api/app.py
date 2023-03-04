import logging
import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from .routes import match, player


def create_app() -> FastAPI:
    app = FastAPI(
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            ),
            Middleware(
                BaseHTTPMiddleware,
                dispatch=time_request,
            ),
        ]
    )
    app.include_router(match.router)
    app.include_router(player.router)

    return app


async def time_request(request: Request, call_next: RequestResponseEndpoint) -> Response:
    start = time.perf_counter()
    response = await call_next(request)
    time_taken = str(time.perf_counter() - start)
    logging.info("%ss taken for request: %s", time_taken, request.url.path)
    response.headers["X-Process-Time"] = time_taken
    return response
