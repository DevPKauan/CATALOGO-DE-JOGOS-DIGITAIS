"""
Interface de linha de comando (CLI) — opção "Relatório" carrega do arquivo antes de gerar.
Removida a opção separada de "Carregar dados".
"""
from typing import Optional
from jogador import Jogador
from jogo import JogoPC, JogoConsole, JogoMobile
from persistencia import PersistenciaJSON


class CLI:

    def __init__(self, jogador: Jogador):
        self.jogador = jogador

    def menu(self):
        while True:
            print("\n" + "=" * 36)
            print("=== MENU PRINCIPAL ===")
            print("=" * 36)
            print("1. Adicionar jogo")
            print("2. Listar jogos")
            print("3. Registrar progresso")
            print("4. Avaliar jogo")
            print("5. Salvar dados")
            print("6. Relatório")
            print("0. Sair")
            print("=" * 36 + "\n")

            opc = input("Escolha uma opção (0-6): ").strip()

            if opc == "1":
                self.op_adicionar()
            elif opc == "2":
                self.op_listar()
            elif opc == "3":
                self.op_progresso()
            elif opc == "4":
                self.op_avaliar()
            elif opc == "5":
                PersistenciaJSON.salvar(self.jogador)
                print("Dados salvos.")
            elif opc == "6":
                # Carrega do arquivo antes de gerar o relatório; se falhar, usa o estado atual
                from relatorio import Relatorio
                try:
                    novo = PersistenciaJSON.carregar()
                    self.jogador = novo
                    print("Dados carregados do arquivo para o relatório.")
                except FileNotFoundError:
                    print("Arquivo de dados não encontrado. Usando os dados em memória.")
                except Exception as e:
                    print("Erro ao carregar dados do arquivo. Usando os dados em memória.", e)
                Relatorio.gerar(self.jogador)
            elif opc == "0":
                print("Saindo... Até mais!")
                break
            else:
                print("Opção inválida! Tente novamente.")

    # ----- OPÇÕES -----
    def op_adicionar(self):
        print("\n" + "-" * 30)
        print("=== ADICIONAR JOGO ===")
        print("-" * 30 + "\n")

        # Tipos disponíveis: PC, Console, Mobile
        print("Tipos disponíveis:\n")
        print("  1) PC")
        print("  2) Console")
        print("  3) Mobile\n")

        tipo_map = {"1": "pc", "2": "console", "3": "mobile",
                    "pc": "pc", "console": "console", "mobile": "mobile"}

        while True:
            tipo_in = input("Escolha o tipo do jogo (1-3): ").strip().lower()
            tipo = tipo_map.get(tipo_in)
            if tipo:
                break
            print("Escolha inválida. Digite 1, 2 ou 3 (ou o nome do tipo).")

        print()  # linha em branco para espaçamento entre seções

        titulo = input("Título: ").strip()
        genero = input("Gênero: ").strip()

        # Campos específicos por tipo (com espaçamento)
        extra = {}
        if tipo == "pc":
            print()
            requisitos = input("Requisitos mínimos (opcional): ").strip()
            extra["requisitos_minimos"] = requisitos
            plataforma_inferida = "PC"
        elif tipo == "console":
            print()
            modelo = input("Modelo do console (opcional): ").strip()
            armazenamento = input("Armazenamento (opcional): ").strip()
            extra["modelo_console"] = modelo
            extra["armazenamento"] = armazenamento
            plataforma_inferida = modelo if modelo else "Console"
        else:  # mobile
            print()
            tamanho = input("Tamanho do app (opcional): ").strip()
            loja = input("Loja (opcional): ").strip()
            versao = input("Versão (opcional): ").strip()
            extra["tamanho_app"] = tamanho
            extra["loja"] = loja
            extra["versao"] = versao
            plataforma_inferida = loja if loja else "Mobile"

        # Sumário e confirmação
        tipo_display = {"pc": "PC", "console": "Console", "mobile": "Mobile"}[tipo]
        print("\nResumo do jogo a ser adicionado:")
        print(f"  Título: {titulo}")
        print(f"  Gênero: {genero}")
        print(f"  Plataforma (inferida): {plataforma_inferida}")
        print(f"  Tipo: {tipo_display}\n")

        confirmar = input("Confirmar adição? (S/n): ").strip().lower()
        if confirmar not in ("", "s", "sim", "y", "yes"):
            print("Operação cancelada pelo usuário.")
            return

        # Criar instância correta usando a plataforma inferida
        if tipo == "pc":
            jogo = JogoPC(
                titulo, genero, plataforma_inferida,
                status="Não iniciado", horas_jogadas=0,
                avaliacao=None, data_inicio=None,
                requisitos_minimos=extra.get("requisitos_minimos", "")
            )
        elif tipo == "console":
            jogo = JogoConsole(
                titulo, genero, plataforma_inferida,
                status="Não iniciado", horas_jogadas=0,
                avaliacao=None, data_inicio=None,
                modelo_console=extra.get("modelo_console", ""),
                armazenamento=extra.get("armazenamento", "")
            )
        else:  # mobile
            jogo = JogoMobile(
                titulo, genero, plataforma_inferida,
                status="Não iniciado", horas_jogadas=0,
                avaliacao=None, data_inicio=None,
                tamanho_app=extra.get("tamanho_app", ""),
                loja=extra.get("loja", ""),
                versao=extra.get("versao", "")
            )

        try:
            self.jogador.adicionar_jogo(jogo)
            print("Jogo adicionado com sucesso.")
        except Exception as e:
            print("Erro ao adicionar jogo:", e)

    def op_listar(self):
        print("\n" + "-" * 30)
        print("=== LISTA DE JOGOS ===")
        print("-" * 30 + "\n")
        if not self.jogador.jogos:
            print("Nenhum jogo cadastrado.\n")
            return

        for idx, j in enumerate(self.jogador.jogos, start=1):
            print(f"{idx:2d}. {j.titulo} ({j.plataforma}) - {j._status} - {j._horas_jogadas}h")
        print()  # linha em branco no final

    def op_progresso(self):
        print("\n" + "-" * 30)
        print("=== REGISTRAR PROGRESSO ===")
        print("-" * 30 + "\n")

        jogo = self.buscar_jogo_interativo()
        if not jogo:
            return

        while True:
            entrada = input("Horas a adicionar (ex: 1.5): ").strip()
            try:
                horas = float(entrada)
                if horas < 0:
                    raise ValueError()
                break
            except Exception:
                print("Entrada inválida. Informe um número >= 0 (ex: 0.5, 2).")

        try:
            jogo.registrar_progresso(horas)
            print("Progresso registrado.")
        except Exception as e:
            print("Erro ao registrar progresso:", e)

    def op_avaliar(self):
        print("\n" + "-" * 30)
        print("=== AVALIAR JOGO ===")
        print("-" * 30 + "\n")

        jogo = self.buscar_jogo_interativo()
        if not jogo:
            return

        while True:
            entrada = input("Nota (0-10): ").strip()
            try:
                nota = float(entrada)
                if nota < 0 or nota > 10:
                    raise ValueError()
                break
            except Exception:
                print("Entrada inválida. Informe um número entre 0 e 10.")

        try:
            jogo.avaliar(nota)
            print("Avaliação registrada.")
        except Exception as e:
            print("Erro ao registrar avaliação:", e)

    # ----- UTILITÁRIOS -----
    def buscar_jogo_interativo(self) -> Optional[object]:
        """
        Busca por título (trecho) de forma case-insensitive.
        Se houver múltiplos resultados, mostra lista numerada e pede seleção.
        Retorna o objeto Jogo ou None se não encontrado / cancelado.
        """
        if not self.jogador.jogos:
            print("Nenhum jogo cadastrado.")
            return None

        consulta = input("Digite o título (ou trecho) do jogo: ").strip().lower()
        if not consulta:
            print("Consulta vazia. Operação cancelada.")
            return None

        matches = [j for j in self.jogador.jogos if consulta in j.titulo.lower()]

        if not matches:
            print("Jogo não encontrado para a consulta informada.")
            return None

        if len(matches) == 1:
            return matches[0]

        # Múltiplos resultados -> selecionar
        print("\nForam encontrados vários jogos:")
        for i, j in enumerate(matches, start=1):
            print(f"  {i}) {j.titulo} ({j.plataforma}) - {j._status}")

        while True:
            escolha = input(f"Escolha um número (1-{len(matches)}) ou 'c' para cancelar: ").strip().lower()
            if escolha == "c":
                print("Operação cancelada.")
                return None
            if escolha.isdigit():
                idx = int(escolha)
                if 1 <= idx <= len(matches):
                    return matches[idx - 1]
            print("Escolha inválida. Tente novamente.")