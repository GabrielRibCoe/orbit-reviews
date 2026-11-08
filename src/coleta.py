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
        timeout = 10
        resp = requests.get(
   
            "https://store.steampowered.com/api/storesearch/",
            params={"term": nome, "l": "english", "cc": "US"},
    
        )
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar jogo: {e}")
            return []
    
    print(resp.status_code)
    dados = resp.json()
    print(dados)

    resultado = []

    for jogo in dados["items"]:
        resultado.append({"ident": jogo["id"], "nome": jogo["name"]})
    
    return resultado

entrada = {
    "appid": "ident",
    "filter": 1,                 # 1 = mais recentes primeiro
    "languages": ["english"],    # atenção: agora é uma LISTA, e o nome é "languages"
    "purchase_type": 1,          # 1 = todas as compras
    "num_per_page": 5,
    "cursor": "*",
}



def buscar_reviews(appid: int, n: int = 100, idioma: str = "english") -> list[str]:
    
    entrada["appid"] = appid
    resp = requests.get(
        "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/",
        params={"input_json": json.dumps(entrada)},
        timeout=10,
)
    print(resp.status_code)
    print(resp.url)
    dados = resp.json()
    print(dados.keys())
    print(dados["response"].keys())

    reviews = dados["response"]["reviews"]
    print(len(reviews))
    print(reviews[0])


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
