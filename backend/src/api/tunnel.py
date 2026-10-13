import json
import shutil
import subprocess


class Tunnel:
    """Endereço público fixo via Tailscale Funnel."""

    def __init__(self, port: int):
        self.port = port
        self.url: str | None = None
        self._active = False

    def start(self) -> "Tunnel":
        if not shutil.which("tailscale"):
            print("Funnel desativado: o comando 'tailscale' não foi encontrado.")
            return self

        try:
            result = subprocess.run(
                ["tailscale", "funnel", "--bg", str(self.port)],
                capture_output=True, text=True, timeout=20,
            )
        except subprocess.TimeoutExpired:
            print("O Funnel não respondeu em 20s. Rode 'tailscale funnel 8000' no terminal "
                  "para ver se ele pede para ser habilitado no painel.")
            return self

        if result.returncode != 0:
            print("Não consegui ligar o Funnel:")
            print((result.stderr or result.stdout).strip())
            return self

        self._active = True
        self.url = self._public_url()
        if self.url:
            print(f"ZadAI público em {self.url}")
        return self

    def _public_url(self) -> str | None:
        status = subprocess.run(["tailscale", "status", "--json"], capture_output=True, text=True)
        try:
            host = json.loads(status.stdout)["Self"]["DNSName"].rstrip(".")
            return f"https://{host}"
        except (ValueError, KeyError):
            return None

    def stop(self) -> None:
        if self._active:
            subprocess.run(["tailscale", "funnel", "reset"], check=False)
            self._active = False