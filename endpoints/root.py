from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from create import templates
import logs as log


router = APIRouter(
    tags=["root"],
    responses={
        404: {"description": "Not found"}
    }
)


@router.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:
    log.actions.info(f'GET on root')
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "button_text": "Test text"},
        status_code=200
    )