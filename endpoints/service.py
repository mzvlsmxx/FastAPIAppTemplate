import time
from pydantic import BaseModel, Field

from fastapi import APIRouter, Query, Request
from fastapi.responses import Response, JSONResponse

from service import check_service_access


router = APIRouter(
    prefix="/service",
    tags=["service"],
    responses={
        404: {"description": "Not found"}
    }
)


@router.get("/check_access")
async def check_access() -> JSONResponse:
    content: dict[str, str] = check_service_access()
    return JSONResponse(
        content=content,
        status_code=200
    )

