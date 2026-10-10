from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from . import auth, chat, pages, settings

app = FastAPI(title="ZadAI", docs_url="/api/docs", redoc_url=None)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="zadai_session",
    same_site="lax",
    max_age=60 * 60 * 24 * 7,
)
app.mount("/static", StaticFiles(directory=settings.FRONTEND_DIR / "static"), name="static")

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(chat.router)
