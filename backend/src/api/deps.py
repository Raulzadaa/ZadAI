from urllib.parse import quote

from fastapi import HTTPException, Request


def current_user(request: Request) -> str | None:
    return request.session.get("user")


def require_user_page(request: Request) -> str:
    """Para páginas HTML: redireciona para /."""
    user = current_user(request)
    if not user:
        raise HTTPException(
            status_code=303,
            headers={"Location": f"/?next={quote(request.url.path)}"},
        )
    return user


def require_user_api(request: Request) -> str:
    """Para endpoints JSON: responde 401."""
    user = current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Sessão expirada. Entre novamente.")
    return user


def safe_next(target: str | None) -> str:
    """Só aceita caminhos internos, evitando open redirect."""
    if target and target.startswith("/") and not target.startswith("//"):
        return target
    return "/chat"
