from fastapi import APIRouter, Request

from .templating import render

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def project(request: Request):
    return render(request, "project.html", active="project")
