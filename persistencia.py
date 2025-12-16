"""
Persistência em JSON: salvar e carregar Jogador (reconstruindo objetos Jogo/subclasses).
"""
import json
from typing import Optional
from jogador import Jogador


class PersistenciaJSON:

    @staticmethod
    def salvar(jogador: Jogador, arquivo: str = "dados.json"):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(jogador.to_dict(), f, indent=4, ensure_ascii=False)

    @staticmethod
    def carregar(arquivo: str = "dados.json") -> Jogador:
        with open(arquivo, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Jogador.from_dict(data)