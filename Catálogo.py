import json
import datetime

# Persistência JSON

class PersistenciaJSON:

    @staticmethod
    def salvar(jogador, arquivo="dados.json"):
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump({
                "jogador": jogador.nome,
                "jogos": [j.to_dict() for j in jogador.jogos]
            }, f, indent=4)

    @staticmethod
    def carregar(arquivo="dados.json"):
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)


# Relatório

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



# Classe Base Jogo

class Jogo:
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas,
                 avaliacao, data_inicio, data_termino):

        self.titulo = titulo
        self.genero = genero
        self.plataforma = plataforma

        self._status = status
        self._horas_jogadas = horas_jogadas

        self.__avaliacao = avaliacao
        self.__data_inicio = data_inicio
        self.__data_termino = data_termino

    # ======== Regra: avaliação só se finalizado ========
    def avaliar(self, nota):
        if self._status != "Finalizado":
            raise ValueError("Não é possível avaliar um jogo não finalizado.")
        if nota < 0 or nota > 10:
            raise ValueError("A avaliação deve estar entre 0 e 10.")
        self.__avaliacao = nota

    # ======== Regra: Horas só progridem (>=0) ========
    def registrar_progresso(self, horas):
        if horas < 0:
            raise ValueError("Horas jogadas devem ser ≥ 0.")
        self._horas_jogadas += horas

    def iniciar_jogo(self, data_inicio):
        self._status = "Jogando"
        self.__data_inicio = data_inicio

    def finalizar_jogo(self, data_termino):
        self._status = "Finalizado"
        self.__data_termino = data_termino

    def reiniciar_jogo(self):
        self._status = "Não iniciado"
        self._horas_jogadas = 0
        self.__data_inicio = None
        self.__data_termino = None

    # Serialização
    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "titulo": self.titulo,
            "genero": self.genero,
            "plataforma": self.plataforma,
            "status": self._status,
            "horas_jogadas": self._horas_jogadas
        }



# Subclasses

class JogoPC(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas,
                 avaliacao, data_inicio, data_termino, requisitos_minimos):

        super().__init__(titulo, genero, plataforma, status, horas_jogadas,
                         avaliacao, data_inicio, data_termino)

        self.__requisitos_minimos = requisitos_minimos


class JogoConsole(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas,
                 avaliacao, data_inicio, data_termino, modelo_console, armazenamento):

        super().__init__(titulo, genero, plataforma, status, horas_jogadas,
                         avaliacao, data_inicio, data_termino)

        self._modelo_console = modelo_console
        self._armazenamento = armazenamento


class JogoMobile(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas,
                 avaliacao, data_inicio, data_termino, tamanho_app, loja, versao):

        super().__init__(titulo, genero, plataforma, status, horas_jogadas,
                         avaliacao, data_inicio, data_termino)

        self._tamanho_app = tamanho_app
        self._loja = loja
        self.__versao = versao



class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.jogos = []
        self.limite_simultaneos = 3  
        self.meta_anual = 5

    # ======== Regra: não permitir duplicados ========
    def adicionar_jogo(self, jogo):
        if any(j.titulo == jogo.titulo and j.plataforma == jogo.plataforma
               for j in self.jogos):
            raise ValueError("Jogo duplicado (mesmo título e plataforma).")

        # ======== Regra: máximo de jogos ativos ========
        jogando = sum(1 for j in self.jogos if j._status == "Jogando")
        if jogo._status == "Jogando" and jogando >= self.limite_simultaneos:
            raise ValueError("Limite de jogos simultâneos já atingido.")

        self.jogos.append(jogo)

    # ======== Regra: alerta sobre meta anual ========
    def verificar_meta(self):
        finalizados = sum(1 for j in self.jogos if j._status == "Finalizado")
        if finalizados < self.meta_anual:
            faltam = self.meta_anual - finalizados
            print(f"⚠ Atenção! Você está {faltam} jogos abaixo da meta anual.")
        else:
            print("🎉 Meta anual atingida!")

    def listar_jogos(self):
        return [j.titulo for j in self.jogos]

class CLI:

    def __init__(self, jogador):
        self.jogador = jogador

    def menu(self):
        while True:
            print("\n=== MENU PRINCIPAL ===")
            print("1. Adicionar jogo")
            print("2. Listar jogos")
            print("3. Registrar progresso")
            print("4. Finalizar jogo")
            print("5. Avaliar jogo")
            print("6. Verificar meta anual")
            print("7. Salvar dados")
            print("8. Carregar dados")
            print("0. Sair")

            opc = input("\nEscolha uma opção: ")

            if opc == "1":
                self.op_adicionar()
            elif opc == "2":
                self.op_listar()
            elif opc == "3":
                self.op_progresso()
            elif opc == "4":
                self.op_finalizar()
            elif opc == "5":
                self.op_avaliar()
            elif opc == "6":
                self.jogador.verificar_meta()
            elif opc == "7":
                PersistenciaJSON.salvar(self.jogador)
                print("Dados salvos!")
            elif opc == "8":
                dados = PersistenciaJSON.carregar()
                print("Dados carregados:", dados)
            elif opc == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida!")

    # ----- OPÇÕES -----

    def op_adicionar(self):
        print("\n=== ADICIONAR JOGO ===")

        titulo = input("Título: ")
        genero = input("Gênero: ")
        plataforma = input("Plataforma: ")

        jogo = Jogo(
            titulo=titulo,
            genero=genero,
            plataforma=plataforma,
            status="Não iniciado",
            horas_jogadas=0,
            avaliacao=None,
            data_inicio=None,
            data_termino=None
        )

        try:
            self.jogador.adicionar_jogo(jogo)
            print("Jogo adicionado com sucesso!")
        except Exception as e:
            print("Erro:", e)

    def op_listar(self):
        print("\n=== LISTA DE JOGOS ===")
        if not self.jogador.jogos:
            print("Nenhum jogo cadastrado.")
            return

        for j in self.jogador.jogos:
            print(f"- {j.titulo} ({j.plataforma}) - {j._status}")

    def op_progresso(self):
        print("\n=== REGISTRAR PROGRESSO ===")
        titulo = input("Título do jogo: ")

        jogo = self.buscar_jogo(titulo)
        if not jogo:
            return

        horas = float(input("Horas jogadas: "))
        try:
            jogo.registrar_progresso(horas)
            print("Progresso registrado!")
        except Exception as e:
            print("Erro:", e)

    def op_finalizar(self):
        print("\n=== FINALIZAR JOGO ===")
        titulo = input("Título do jogo: ")

        jogo = self.buscar_jogo(titulo)
        if not jogo:
            return

        jogo.finalizar_jogo(datetime.date.today())
        print("Jogo finalizado!")

    def op_avaliar(self):
        print("\n=== AVALIAR JOGO ===")
        titulo = input("Título do jogo: ")

        jogo = self.buscar_jogo(titulo)
        if not jogo:
            return

        nota = float(input("Nota (0-10): "))

        try:
            jogo.avaliar(nota)
            print("Avaliação registrada!")
        except Exception as e:
            print("Erro:", e)

    # ----- UTILITÁRIO -----

    def buscar_jogo(self, titulo):
        for j in self.jogador.jogos:
            if j.titulo == titulo:
                return j
        print("Jogo não encontrado.")
        return None
    
if __name__ == "__main__":
    jogador = Jogador("Pedro")
    cli = CLI(jogador)
    cli.menu()
