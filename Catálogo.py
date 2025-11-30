import json

# classe para persistencia de dados em json
class PersistenciaJSON:

    def salvar(jogador, arquivo="dados.json"):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump({
                "jogador": jogador.nome,
                "jogos": [j.to_dict() for j in jogador.jogos]
            }, f, indent=4)

    def carregar(arquivo="dados.json"):
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)


class Relatorio:

    @staticmethod
    def gerar(jogador):
        print("\n=== RELATÓRIO DE JOGOS ===")
        print(f"Jogador: {jogador.nome}\n")

        for jogo in jogador.jogos:
            print(f"Título: {jogo.titulo}")
            print(f"Gênero: {jogo.genero}")
            print(f"Plataforma: {jogo.plataforma}")
            print(f"Status: {jogo._status}")
            print(f"Horas jogadas: {jogo._horas_jogadas}")
            print("-" * 30)

# Classe Base
class Jogo:
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, data_inicio, data_termino):
        # Públicos
        self.titulo = titulo
        self.genero = genero
        self.plataforma = plataforma

        # Protegidos
        self._status = status
        self._horas_jogadas = horas_jogadas

        # Privados
        self.__avaliacao = avaliacao
        self.__data_inicio = data_inicio
        self.__data_termino = data_termino

    # Getters
    def get_status(self):
        return self._status

    def get_horas_jogadas(self):
        return self._horas_jogadas

    # Métodos da classe base
    def iniciar_jogo(self, data_inicio):
        self._status = "Em andamento"
        self.__data_inicio = data_inicio

    def registrar_progresso(self, horas):
        if horas > 0:
            self._horas_jogadas += horas

    def finalizar_jogo(self, data_termino):
        self._status = "Finalizado"
        self.__data_termino = data_termino

    def reiniciar_jogo(self):
        self._status = "Não iniciado"
        self._horas_jogadas = 0
        self.__data_inicio = None
        self.__data_termino = None


# Classe herdada para jogos de PC
class JogoPC(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao,
                 data_inicio, data_termino, requisitos_minimos):

        super().__init__(titulo, genero, plataforma, status, horas_jogadas,
                         avaliacao, data_inicio, data_termino)

        self.__requisitos_minimos = requisitos_minimos  # privado

    def configurar_requisitos(self, novos_requisitos):
        self.__requisitos_minimos = novos_requisitos

    def exibir_requisitos(self):
        return self.__requisitos_minimos


# Classe herdada para consoles
class JogoConsole(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao,
                 data_inicio, data_termino, modelo_console, armazenamento):

        super().__init__(titulo, genero, plataforma, status, horas_jogadas,
                         avaliacao, data_inicio, data_termino)

        self._modelo_console = modelo_console  # protegido
        self._armazenamento = armazenamento    # protegido

    def verificar_espaco(self, tamanho_jogo):
        return tamanho_jogo <= self._armazenamento


# Classe herdada para mobile
class JogoMobile(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao,
                 data_inicio, data_termino, tamanho_app, loja, versao):

        super().__init__(titulo, genero, plataforma, status, horas_jogadas,
                         avaliacao, data_inicio, data_termino)

        self._tamanho_app = tamanho_app   # protegido
        self._loja = loja                 # protegido
        self.__versao = versao            # privado

    def atualizar_versao(self, nova_versao):
        self.__versao = nova_versao


# classe jogador 
class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.jogos = []  # relação: Jogador -> Jogos

    def adicionar_jogo(self, jogo):
        self.jogos.append(jogo)

    def listar_jogos(self):
        return [jogo.titulo for jogo in self.jogos]
    
  # Serialização para JSON
    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "titulo": self.titulo,
            "genero": self.genero,
            "plataforma": self.plataforma,
            "status": self._status,
            "horas_jogadas": self._horas_jogadas
        }
