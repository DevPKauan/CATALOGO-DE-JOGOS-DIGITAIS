"""
Modelos de jogo: Jogo (base) e subclasses.
Observação: funcionalidade de "finalizar jogo" removida.
"""
from datetime import date
from typing import Optional


class Jogo:
    def __init__(self, titulo: str, genero: str, plataforma: str,
                 status: str = "Não iniciado", horas_jogadas: float = 0.0,
                 avaliacao: Optional[float] = None,
                 data_inicio: Optional[date] = None):
        self.titulo = titulo
        self.genero = genero
        self.plataforma = plataforma

        self._status = status
        self._horas_jogadas = horas_jogadas

        self.__avaliacao = avaliacao
        self.__data_inicio = data_inicio

    # ======== Regra: avaliação liberada independentemente de "finalizado" ========
    def avaliar(self, nota: float):
        if nota < 0 or nota > 10:
            raise ValueError("A avaliação deve estar entre 0 e 10.")
        self.__avaliacao = nota

    # ======== Regra: Horas só progridem (>=0) ========
    def registrar_progresso(self, horas: float):
        if horas < 0:
            raise ValueError("Horas jogadas devem ser ≥ 0.")
        self._horas_jogadas += horas

    def iniciar_jogo(self, data_inicio: date):
        self._status = "Jogando"
        self.__data_inicio = data_inicio

    def reiniciar_jogo(self):
        self._status = "Não iniciado"
        self._horas_jogadas = 0
        self.__data_inicio = None

    # Serialização
    def to_dict(self):
        def d_or_none(d):
            return d.isoformat() if d is not None else None

        return {
            "tipo": self.__class__.__name__,
            "titulo": self.titulo,
            "genero": self.genero,
            "plataforma": self.plataforma,
            "status": self._status,
            "horas_jogadas": self._horas_jogadas,
            "avaliacao": getattr(self, "_Jogo__avaliacao", None),
            "data_inicio": d_or_none(getattr(self, "_Jogo__data_inicio", None)),
        }

    @staticmethod
    def _parse_date(d):
        from datetime import date
        if d is None:
            return None
        if isinstance(d, date):
            return d
        return date.fromisoformat(d)

    @classmethod
    def from_dict(cls, d: dict):
        """Fábrica para instanciar a subclasse correta a partir do dict."""
        tipo = d.get("tipo", "Jogo")
        # Campos comuns
        titulo = d.get("titulo")
        genero = d.get("genero")
        plataforma = d.get("plataforma")
        status = d.get("status", "Não iniciado")
        horas_jogadas = d.get("horas_jogadas", 0.0)
        avaliacao = d.get("avaliacao", None)
        data_inicio = cls._parse_date(d.get("data_inicio"))

        if tipo == "JogoPC":
            requisitos = d.get("requisitos_minimos")
            return JogoPC(titulo, genero, plataforma, status, horas_jogadas,
                          avaliacao, data_inicio, requisitos)
        elif tipo == "JogoConsole":
            modelo = d.get("modelo_console")
            armazenamento = d.get("armazenamento")
            return JogoConsole(titulo, genero, plataforma, status, horas_jogadas,
                               avaliacao, data_inicio, modelo, armazenamento)
        elif tipo == "JogoMobile":
            tamanho = d.get("tamanho_app")
            loja = d.get("loja")
            versao = d.get("versao")
            return JogoMobile(titulo, genero, plataforma, status, horas_jogadas,
                              avaliacao, data_inicio, tamanho, loja, versao)
        else:
            return Jogo(titulo, genero, plataforma, status, horas_jogadas,
                        avaliacao, data_inicio)


class JogoPC(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas,
                 avaliacao, data_inicio, requisitos_minimos: str = ""):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas,
                         avaliacao, data_inicio)
        self.__requisitos_minimos = requisitos_minimos

    def to_dict(self):
        d = super().to_dict()
        d.update({"requisitos_minimos": self.__requisitos_minimos})
        return d


class JogoConsole(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas,
                 avaliacao, data_inicio, modelo_console: str = "",
                 armazenamento: str = ""):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas,
                         avaliacao, data_inicio)
        self._modelo_console = modelo_console
        self._armazenamento = armazenamento

    def to_dict(self):
        d = super().to_dict()
        d.update({
            "modelo_console": self._modelo_console,
            "armazenamento": self._armazenamento
        })
        return d


class JogoMobile(Jogo):
    def __init__(self, titulo, genero, plataforma, status, horas_jogadas,
                 avaliacao, data_inicio, tamanho_app: str = "",
                 loja: str = "", versao: str = ""):
        super().__init__(titulo, genero, plataforma, status, horas_jogadas,
                         avaliacao, data_inicio)
        self._tamanho_app = tamanho_app
        self._loja = loja
        self.__versao = versao

    def to_dict(self):
        d = super().to_dict()
        d.update({
            "tamanho_app": self._tamanho_app,
            "loja": self._loja,
            "versao": self.__versao
        })
        return d