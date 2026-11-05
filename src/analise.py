"""Agregação dos resultados e resumo em texto.  (Responsável: Pessoa 3)

Formato das estatísticas (dict) que `analisar` devolve e `resumir` consome:
    {
        "jogo": str,
        "total": int,                      # quantas reviews foram analisadas
        "pct_positivas": float,            # 0 a 100
        "pct_negativas": float,            # 0 a 100
        "exemplos_positivos": list[str],   # 2 ou 3 reviews
        "exemplos_negativos": list[str],   # 2 ou 3 reviews
        "palavras_negativas": list[str],   # termos mais frequentes nas negativas
    }
"""


def analisar(nome_jogo: str, textos: list[str], probabilidades: list[float]) -> dict:
    """Junta textos + probabilidades da rede e calcula as estatísticas acima."""
    raise NotImplementedError


def resumir(estatisticas: dict) -> str:
    """Gera o textinho explicativo.

    Comece por um template (frase montada a partir dos números).
    Opcional: trocar por um modelo de linguagem depois.
    """
    raise NotImplementedError
