from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.init_db import init_db

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Books and reviews API built for XJCO3011 coursework",
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(api_router, prefix="/api")
