import asyncio
import logging
import threading

from backend.src.brain import LLMModule

log = logging.getLogger("zadai.web")


class ZadAIUnavailable(Exception):
    """A IA local não respondeu."""


# Trava compartilhada com o loop de voz/texto no zadai.py
brain_lock = threading.Lock()
_brain = None


def set_brain(brain) -> None:
    global _brain
    _brain = brain


def _get_brain():
    global _brain
    if _brain is None:  # permite subir só a web (uvicorn) sem o zadai.py
        _brain = LLMModule()
    return _brain


def _run(prompt: str):
    with brain_lock:
        return _get_brain().prompt(prompt)


async def ask_zadai(messages: list[dict]) -> str:
    prompt = messages[-1]["content"]
    try:
        result = await asyncio.to_thread(_run, prompt)  # ollama.chat é bloqueante
    except Exception as exc:
        log.exception("Falha ao processar o pedido no ZadAI")
        raise ZadAIUnavailable(
            "Não consegui falar com o ZadAI. Confira se o Ollama está rodando e se os modelos estão baixados."
        ) from exc
    return str(result).strip() or "Tarefa concluída."