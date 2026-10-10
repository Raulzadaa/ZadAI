from fastapi import Request
from fastapi.templating import Jinja2Templates

from .settings import FRONTEND_DIR

templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))


def render(request: Request, name: str, status_code: int = 200, **context):
    context.setdefault("user", request.session.get("user"))
    return templates.TemplateResponse(request, name, context, status_code=status_code)
