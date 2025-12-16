"""
Ponto de entrada do aplicativo.
"""
from jogador import Jogador
from persistencia import PersistenciaJSON
from cli import CLI

if __name__ == "__main__":
    nome = input("Digite o nome do jogador: ")
    jogador = Jogador(nome)

    try:
        jogador = PersistenciaJSON.carregar()
        print("Arquivo JSON encontrado e carregado.")
    except FileNotFoundError:
        PersistenciaJSON.salvar(jogador)
        print("Arquivo JSON criado automaticamente.")

    cli = CLI(jogador)
    cli.menu()