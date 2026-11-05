"""Coleta de jogos e reviews na API pública da Steam.  (Responsável: Pessoa 1)

Endpoints úteis (não precisam de chave):
  - Busca por nome:  https://store.steampowered.com/api/storesearch/?term=<nome>&l=english&cc=US
  - Reviews:         https://store.steampowered.com/appreviews/<appid>?json=1&num_per_page=100&filter=recent&language=english
    (a resposta traz um "cursor" para paginar; cada review tem "review" (texto) e "voted_up" (True/False))

Cuidados: coloque uma pausa (time.sleep) entre chamadas e trate jogos sem reviews.
"""
import pandas as pd


def buscar_jogo(nome: str) -> list[dict]:
    """Busca jogos pelo nome.

    Retorna uma lista de dicts, por exemplo:
        [{"appid": 570, "nome": "Dota 2"}, ...]
    Lista vazia se nada for encontrado.
    """
    raise NotImplementedError


def buscar_reviews(appid: int, n: int = 100, idioma: str = "english") -> list[str]:
    """Baixa até `n` reviews recentes de um jogo (paginando com o cursor).

    Retorna apenas os textos das reviews.
    """
    raise NotImplementedError


def coletar_dataset(appids: list[int], n_por_jogo: int = 1000, idioma: str = "english") -> pd.DataFrame:
    """Monta o dataset de TREINO com reviews rotuladas.

    Retorna um DataFrame com as colunas:
        texto (str), rotulo (1 = recomendou / 0 = não recomendou), appid (int)
    Dica: salve em data/reviews.csv (o .gitignore já ignora CSVs).
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Teste rápido: python -m src.coleta
    print(buscar_jogo("Dota 2"))
