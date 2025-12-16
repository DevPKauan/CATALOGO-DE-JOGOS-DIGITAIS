"""
Gera relatório simples de jogos.
"""
from jogador import Jogador


class Relatorio:

    @staticmethod
    def gerar(jogador: Jogador):
        print("\n=== RELATÓRIO DE JOGOS ===")
        print(f"Jogador: {jogador.nome}\n")

        for jogo in jogador.jogos:
            print(f"Título: {jogo.titulo}")
            print(f"Gênero: {jogo.genero}")
            print(f"Plataforma: {jogo.plataforma}")
            print(f"Status: {jogo._status}")
            print(f"Horas jogadas: {jogo._horas_jogadas}")
            print("-" * 30)