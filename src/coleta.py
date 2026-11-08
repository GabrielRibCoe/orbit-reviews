"""Coleta de jogos e reviews na API pública da Steam.  (Responsável: Pessoa 1)

Endpoints úteis (não precisam de chave):
  - Busca por nome:  https://store.steampowered.com/api/storesearch/?term=<nome>&l=english&cc=US
  - Reviews:         https://store.steampowered.com/appreviews/<appid>?json=1&num_per_page=100&filter=recent&language=english
    (a resposta traz um "cursor" para paginar; cada review tem "review" (texto) e "voted_up" (True/False))

Cuidados: coloque uma pausa (time.sleep) entre chamadas e trate jogos sem reviews.
"""


import pandas as pd
import json
import requests


def buscar_jogo(nome: str) -> list[dict]:

    try: 
      
        resp = requests.get(
   
            "https://store.steampowered.com/api/storesearch/",
            params={"term": nome, "l": "english", "cc": "US"},
            timeout = 10,
        )
        resp.raise_for_status()
        dados = resp.json()
    except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar jogo: {e}")
            return []
    
  

    resultado = []

    for jogo in dados.get("items", []):
        resultado.append({"appid": jogo["id"], "nome": jogo["name"]})
        
    return resultado

def _buscar_pagina(appid, n, idioma, cursor) -> list[str]:
    """Busca uma página de reviews (até n) para um appid, retorna lista de textos."""
    entrada = {
        "appid": appid,
        "filter": 1,                 # 1 = mais recentes primeiro
        "languages": [idioma],    # atenção: agora é uma LISTA, e o nome é "languages"
        "purchase_type": 1,          # 1 = todas as compras
        "num_per_page": n,
        'cursor': cursor, 
    }
    resp = requests.get(
        "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/",
        params={"input_json": json.dumps(entrada)},
        timeout=10,
    )
    resp.raise_for_status()
    dados = resp.json()
    reviews = []
    for texto in dados.get("response", {}).get("reviews", []):
        reviews.append(texto["review"])
    return reviews  # pega só os n primeiros

def buscar_reviews(appid: int, n: int = 100, idioma: str = "english") -> list[str]:

    
    
    entrada = {
        "appid": appid,
        "filter": 1,                 # 1 = mais recentes primeiro
        "languages": [idioma],    # atenção: agora é uma LISTA, e o nome é "languages"
        "purchase_type": 1,          # 1 = todas as compras
        "num_per_page": n,
        'cursor': "*",
    }
    

    try: 
        resp = requests.get(
        "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/",
        params={"input_json": json.dumps(entrada)},
        timeout=10,
        )
        resp.raise_for_status()
        dados = resp.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar reviews: {e}")
        return []
    reviews = []
    for texto in dados.get("response", {}).get("reviews", []):
        reviews.append(texto["review"])

        return reviews  # pega só os n primeiros


def coletar_dataset(appids: list[int], n_por_jogo: int = 1000, idioma: str = "english") -> pd.DataFrame:
    """Monta o dataset de TREINO com reviews rotuladas.

    Retorna um DataFrame com as colunas:
        texto (str), rotulo (1 = recomendou / 0 = não recomendou), appid (int)
    Dica: salve em data/reviews.csv (o .gitignore já ignora CSVs).
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Teste rápido
    print(buscar_jogo("Dota 2"))
    print(buscar_reviews(570, n=5))

