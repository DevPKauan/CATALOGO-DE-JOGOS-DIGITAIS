

# Classe Base:
class Jogo:
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas, avaliacao, data_inicio, data_termino):
        # Atributos:
        self.titulo = titulo
        self.genero = genero
        self.plataforma = plataforma
        self.status = status
        self.horas_jogadas = 0
        self.avaliacao = avaliacao
        self.data_inicio = data_inicio
        self.data_termino = data_termino

    def iniciar_jogo(self, data_inicio):
        # Muda o status do jogo como iniciado
        pass 

    def registrar_progresso(self, horas):
        # Contabiliza o tempo jogado
        pass

    def finalizar_jogo(self):
        # encerra o jogo e atualiza o status
        pass

    def reiniciar_jogo(self):
        # volta o jogo para o estado inicial
        pass

class JogoPC(Jogo):
    def __init__(self, requisitos_minimos):
        self.requisitos_minimos=requisitos_minimos
    
    def configurar_requisitos(self):
        pass
    def exibir_requisitos(self):
        pass

class JogoConsole(Jogo):
    def __init__ (self, modelo_console, armazenamento):
        self.modelo_console = modelo_console
        self.armazenamento = armazenamento

class JogoMobile(Jogo):
    def __init__(self, tamanho_app, loja, versao):
        self.tamanho_app=tamanho_app
        self.versao=versao
        self.loja=loja
    def atualizar_versao(nova_versao):
        pass