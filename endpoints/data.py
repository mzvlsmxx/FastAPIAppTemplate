import time
from pydantic import BaseModel, Field

from fastapi import APIRouter, Query, Request
from fastapi.responses import Response, JSONResponse

from database import MySQLClient, RedisClient
from broker import KafkaClient
import logs as log


router = APIRouter(
    prefix="/data",
    tags=["data"],
    responses={
        404: {"description": "Not found"}
    }
)


@router.get("/fetch")
async def fetch(request: Request) -> JSONResponse:
    start_time: float = time.perf_counter()
    content = {
        "MySQLAccess": MySQLClient.check_access(),
        "RedisAccess": RedisClient.check_access(),
        "KafkaAccess": KafkaClient.check_access(),
        "TimeELapsed": f'{round(time.perf_counter() - start_time, 3)}s'
    }
    log.actions.info(f'GET on /data/fetch ({request.query_params = })')
    return JSONResponse(
        content=content,
        status_code=200
    )


@router.post("/process")
async def process(request: Request) -> Response:
    log.actions.info(f'POST on /data/process ({request.query_params = }, {await request.json() = })')
    return JSONResponse(content={}, status_code=200)
