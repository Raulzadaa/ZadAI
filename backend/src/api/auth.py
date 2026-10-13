import asyncio
import secrets
import time

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from . import settings
from .deps import current_user, safe_next
from .security import verify_password
from .templating import render

router = APIRouter()

_failures: list[float] = []
_WINDOW, _MAX = 600, 5

def _blocked() -> bool:
    now = time.monotonic()
    _failures[:] = [t for t in _failures if now - t < _WINDOW]
    return len(_failures) >= _MAX


@router.get("/", include_in_schema=False)
async def login_page(request: Request, next: str = "/chat"):
    if current_user(request):
        return RedirectResponse(safe_next(next), status_code=303)
    return render(request, "login.html", active="login", next=safe_next(next), error=None, username="")


@router.post("/", include_in_schema=False)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    next: str = Form("/chat"),
):
    if _blocked():
        return render(
            request, "login.html", status_code=429, active="login",
            next=safe_next(next), error="Muitas tentativas. Aguarde alguns minutos.", username="",
        )

    configured = bool(settings.USERNAME and settings.PASSWORD_HASH)
    user_ok = secrets.compare_digest(username.encode(), settings.USERNAME.encode())
    pass_ok = verify_password(password, settings.PASSWORD_HASH) if configured else False

    if configured and user_ok and pass_ok:
        request.session.clear()
        request.session["user"] = username
        return RedirectResponse(safe_next(next), status_code=303)

    await asyncio.sleep(0.6)  # atrito simples contra tentativa em massa
    error = (
        "Usuário ou senha incorretos."
        if configured
        else "Login não configurado. Defina ZADAI_USERNAME e ZADAI_PASSWORD_HASH no .env."
    )
    return render(
        request, "login.html", status_code=401, active="login",
        next=safe_next(next), error=error, username=username,
    )


@router.post("/logout", include_in_schema=False)
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)
