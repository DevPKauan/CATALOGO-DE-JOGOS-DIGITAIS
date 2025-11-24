#!/usr/bin/env bash
set -euo pipefail

# Script de conveniência para criar/ativar venv, instalar dependências e executar a app.
# Uso: ./run.sh

PYTHON=python3
VENV_DIR=.venv

if ! command -v $PYTHON >/dev/null 2>&1; then
  echo "Erro: $PYTHON não encontrado. Instale o Python 3.x." >&2
  exit 1
fi

# cria venv se não existir
if [ ! -d "$VENV_DIR" ]; then
  if $PYTHON -m venv --help >/dev/null 2>&1; then
    echo "Criando virtualenv em $VENV_DIR..."
    $PYTHON -m venv "$VENV_DIR"
  else
    echo "O módulo venv não está disponível. Instale 'python3-venv' ou crie um venv manualmente." >&2
    exit 1
  fi
fi

# ativa venv e instala dependências
# shellcheck disable=SC1090
source "$VENV_DIR/bin/activate"
python -m pip install --upgrade pip
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
fi

# executa a aplicação
python main.py
