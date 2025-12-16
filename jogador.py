"""
Classe Jogador: gerencia lista de jogos e regras (duplicados, limite simultâneos).
"""
from typing import List
from jogo import Jogo


class Jogador:
    def __init__(self, nome: str):
        self.nome = nome
        self.jogos: List[Jogo] = []
        self.limite_simultaneos = 3

    # ======== Regra: não permitir duplicados ========
    def adicionar_jogo(self, jogo: Jogo):
        if any(j.titulo == jogo.titulo and j.plataforma == jogo.plataforma
               for j in self.jogos):
            raise ValueError("Jogo duplicado (mesmo título e plataforma).")

        # ======== Regra: máximo de jogos ativos ========
        jogando = sum(1 for j in self.jogos if j._status == "Jogando")
        if jogo._status == "Jogando" and jogando >= self.limite_simultaneos:
            raise ValueError("Limite de jogos simultâneos já atingido.")

        self.jogos.append(jogo)

    def listar_jogos(self):
        return [j.titulo for j in self.jogos]

    def to_dict(self):
        return {
            "jogador": self.nome,
            "jogos": [j.to_dict() for j in self.jogos]
        }

    @classmethod
    def from_dict(cls, d: dict):
        from jogo import Jogo
        nome = d.get("jogador", "Jogador")
        j = cls(nome)
        jogos_data = d.get("jogos", [])
        for jd in jogos_data:
            jogo_obj = Jogo.from_dict(jd)
            j.jogos.append(jogo_obj)
        return j
