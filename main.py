import time

import uvicorn
from fastapi import FastAPI
from loguru import logger
from sqlalchemy import event, Engine

app = FastAPI(
    version="0.0.1",
    title="fastApiProject",
    openapi_url=f"/api/v1/openapi.json",
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


if __name__ == "__main__":
    # run fastapi using uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8888,
        log_level="error",
        reload=True,
    )
