"""Configurações da camada web. Tudo vem de variáveis de ambiente (ou do .env na raiz)."""
import logging
import os
import secrets
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]
FRONTEND_DIR = ROOT_DIR / "frontend"

try:
    from dotenv import load_dotenv

    load_dotenv(ROOT_DIR / ".env")
except ImportError:  # python-dotenv é opcional
    pass

log = logging.getLogger("zadai.web")

# Autenticação (usuário único, ideal para uso local)
USERNAME = os.getenv("ZADAI_USERNAME", "")
PASSWORD_HASH = os.getenv("ZADAI_PASSWORD_HASH", "")

SECRET_KEY = os.getenv("ZADAI_SECRET_KEY", "")
if not SECRET_KEY:
    SECRET_KEY = secrets.token_urlsafe(32)
    log.warning("ZADAI_SECRET_KEY não definida: as sessões serão perdidas a cada reinício.")

# IA local
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
ZADAI_MODEL = os.getenv("ZADAI_MODEL", "")
SYSTEM_PROMPT = os.getenv(
    "ZADAI_SYSTEM_PROMPT",
    "Você é o ZadAI, um assistente pessoal que roda localmente. "
    "Responda no idioma do usuário, de forma direta e objetiva.",
)

HOST = os.getenv("ZADAI_HOST", "0.0.0.0")
PORT = int(os.getenv("ZADAI_PORT", "8000"))