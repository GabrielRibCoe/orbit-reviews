"""Coleta de jogos e reviews na API pública da Steam.  (Responsável: Pessoa 1)

Endpoints úteis (não precisam de chave):
  - Busca por nome:  https://store.steampowered.com/api/storesearch/?term=<nome>&l=english&cc=US
  - Reviews:         https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/ (a API foi alterada pois a antiga foi desligada.)
    (a resposta traz um "cursor" para paginar; cada review tem "review" (texto) e "voted_up" (True/False))

Como as funções agem:
- buscar_jogo(nome) -> lista de {appid, nome} //Usa o nome digitado pelo usuário(por hora jogos pré-definidos para teste e treino da rede neural), e posteriormente o appid é usado para buscar as reviews do jogo.
- buscar_pagina(appid, n, idioma, cursor) -> (lista de reviews, novo_cursor) //Salva a lista com reviews e o cursor para a próxima página de reviews.
- buscar_reviews(appid, n, idioma) -> lista de textos (até n) //Salva apenas os textos das reviews, sem o resto das informações.
- buscar_reviews_completo(appid, n, idioma) -> lista de {review, voted_up, ...} (até n) //Salva todas as informações das reviews, incluindo o texto e se a review foi positiva ou negativa.
- coletar_dataset(appids, n_por_jogo, idioma) -> DataFrame com colunas ["texto", "rotulo", "appid"], onde rotulo = 1 se positivo, 0 se negativo. (O dataset pode ser salvo em CSV para treinar o modelo.)  //Armazena informações das reviews em um DataFrame, com o texto da review, o rótulo (1 se positivo, 0 se negativo) e o appid do jogo. O dataset pode ser salvo em CSV para treinar o modelo.
  
"""


import pandas as pd
import json
import requests
import time


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

def _buscar_pagina(appid, n, idioma, cursor) -> tuple[list[dict], str]:
    
    entrada = {
    "appid": appid,
    "filter": 1,                  # 1 = mais recentes primeiro
    "languages": [idioma],        # LISTA, e o nome é "languages"
    "purchase_type": 1,           # 1 = todas as compras
    "num_per_page": min(100, max(1, n)),
    "cursor": cursor,
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
        return [], cursor

    resposta = dados.get("response", {})
    reviews = resposta.get("reviews", [])
    novo_cursor = resposta.get("cursor", cursor)

    return reviews, novo_cursor

def _buscar_reviews_completo(appid: int, n, idioma: str = "english") -> list[dict]:
    
    todas = []
    cursor = "*"
    
    while len(todas) < n:
        reviews, novo_cursor = _buscar_pagina(appid, n - len(todas), idioma, cursor)
        if not reviews:
            break
        todas.extend(reviews)
        if novo_cursor == cursor:
                break
        cursor = novo_cursor
        time.sleep(1)  # pausa de 1 segundo entre chamadas
    
    return todas[:n]

def buscar_reviews(appid: int, n: int = 100, idioma: str = "english") -> list[str]:
    completas = _buscar_reviews_completo(appid, n, idioma)
    return [r.get("review", "") for r in completas]

def coletar_dataset(appids: list[int], n_por_jogo: int = 1000, idioma: str = "english") -> pd.DataFrame:
     
    linhas = []
    
    for appid in appids:
        print(f"Coletando reviews para appid {appid}...")
        reviews = _buscar_reviews_completo(appid, n_por_jogo, idioma)
        for r in reviews:
            linhas.append({"texto": r.get("review"), "rotulo": 1 if r.get("voted_up") else 0, "appid": appid})
    return pd.DataFrame(linhas)

# appids usados no dataset de treino (misture jogos bem e mal avaliados).
JOGOS_TREINO = [
    620, 814380, 1145350, 1145360, 1325200, 1340990, 1448440, 1771300,
    1875580, 1938010, 2114740, 2138710, 2277560, 2288150, 2437170, 2584990,
    2622380, 2753000, 2767030, 2784470, 2868840, 3061570, 3164330, 3681010,
    4262460, 4656000,
]

if __name__ == "__main__":
    # python -m src.coleta   (demora alguns minutos por causa da pausa entre as páginas)
    import os

    caminho = "data/reviews.csv"
    if os.path.exists(caminho):
        resp = input(f"{caminho} já existe. Sobrescrever? (s/n) ")
        if resp.strip().lower() != "s":
            raise SystemExit("Coleta cancelada, o arquivo atual foi mantido.")

    df = coletar_dataset(JOGOS_TREINO, n_por_jogo=1500)
    df.to_csv(caminho, index=False, encoding="utf-8")
    print(df.shape)
    print(df["rotulo"].value_counts())
    print(df.groupby("appid")["rotulo"].mean())   # fração positiva por jogo