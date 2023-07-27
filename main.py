import time

import uvicorn
from fastapi import FastAPI
from loguru import logger
from sqlalchemy import event
from sqlalchemy.future import Engine
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    version=settings.VERSION,
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault("query_start_time", []).append(time.time())
    logger.info(f"QUERY START: ========================================> \n{statement}")


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info["query_start_time"].pop(-1)
    logger.info(f"QUERY PARAMS : ========================================> \n{parameters}")
    logger.info(f"TOTAL TIME: {total}")


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_header=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    # run fastapi using uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8888,
        log_level="error",
        reload=True,
    )
