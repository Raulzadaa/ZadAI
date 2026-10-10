#!/bin/bash

# ==============================================================================
# Script para rodar o FastAPI e abrir o Tunelamento Público Simultaneamente
# ==============================================================================

# Nome do seu arquivo Python (sem o .py) e a instância do FastAPI
APP_MODULE="main:app"
PORT=8000

echo "🚀 Iniciando o servidor FastAPI na porta $PORT..."
# Inicia o Uvicorn em background (--host 0.0.0.0 permite o bind correto)
uvicorn "$APP_MODULE" --host 0.0.0.0 --port "$PORT" &
UVICORN_PID=$!

# Aguarda 2 segundos para garantir que o FastAPI subiu completamente
sleep 2

echo "🌐 Criando túnel público temporário via localhost.run..."
echo "----------------------------------------------------------------"
echo "👉 AGUARDE UM MOMENTO PARA VER O LINK HTTPS ABAIXO"
echo "👉 Mantenha este terminal aberto. Pressione Ctrl+C para encerrar tudo."
echo "----------------------------------------------------------------"

# Executa o ssh para criar o túnel. 
# Quando o usuário apertar Ctrl+C, o script vai capturar e encerrar o FastAPI também.
ssh -R 80:localhost:"$PORT" nokey@localhost.run

# Garante que o FastAPI seja encerrado ao fechar o script
kill $UVICORN_PID 2>/dev/null
