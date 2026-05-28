#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "[run_local] Verificando/criando banco de dados 'projeto_orm'..."
if sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='projeto_orm'" | grep -q 1; then
  echo "[run_local] Banco já existe"
else
  echo "[run_local] Criando banco projeto_orm (poderá pedir senha sudo)..."
  sudo -u postgres psql -c "CREATE DATABASE projeto_orm;"
  echo "[run_local] Banco criado"
fi

echo "[run_local] Garantindo senha do usuário 'postgres'..."
sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"

if [ ! -d ".venv" ]; then
  echo "[run_local] Criando virtualenv .venv"
  python3 -m venv .venv
fi

echo "[run_local] Ativando venv e instalando dependências"
# shellcheck source=/dev/null
source .venv/bin/activate
pip install -r requirements.txt

echo "[run_local] Populando banco de dados com dados de exemplo"
python3 popular_bd.py

echo "[run_local] Iniciando a aplicação em background (logs em app.log)"
nohup bash -lc "source .venv/bin/activate && python3 app.py" > app.log 2>&1 &
PID=$!
echo "[run_local] App iniciado com PID ${PID} — aguardando saída de logs..."
sleep 1
tail -n 30 app.log || true

echo "[run_local] Concluído. Para ver logs: tail -f app.log"
