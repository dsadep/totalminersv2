import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.db.database import create_tables
from api.routers import routers
from logger import config_logger

app = FastAPI(
    title='API',
    redoc_url=None,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8080'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
[app.include_router(router) for router in routers]


@app.get("/healthcheck")
async def healthcheck():
    await create_tables()
    return {
        "status": 'ok',
    }


def create_app():
    config_logger()
    logging.critical('App starting...')
    return app
