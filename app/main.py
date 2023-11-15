import os
import sys
import uvicorn

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from redis import asyncio as aioredis
from starlette.middleware.cors import CORSMiddleware

from app.config.config import DefaultServerSettings, RedisSettings, MONGO_URL
from app.endpoints import all_routes

root_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_folder)


def bind_routes(application: FastAPI, settings: DefaultServerSettings, list_of_routes) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route, prefix=settings.PATH_PREFIX)


def get_app(settings: DefaultServerSettings) -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    description = "RESTfull API for LeadHit"

    application = FastAPI(
        title="LeadHit (test task)",
        description=description,
        docs_url="/",
        openapi_url="/openapi",
        version="1.0.0",
    )
    bind_routes(application, settings, all_routes)
    return application


app = get_app(DefaultServerSettings())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT"],
    allow_credentials=True,
    allow_headers=["*"]
)

client = AsyncIOMotorClient(MONGO_URL)
app.state.mongo_client = client

# @app.on_event("startup")
# async def startup_event():
#     redis = aioredis.from_url(f"redis://{RedisSettings.REDIS_HOST}:{RedisSettings.REDIS_PORT}", encoding="utf8",
#                               decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="TimeOFF-fastapi-cache")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=DefaultServerSettings().APP_HOST,
        port=DefaultServerSettings().APP_PORT,
        log_level="debug",

    )
