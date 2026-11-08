import json
import requests

entrada = {
    "appid": 570,
    "filter": 1,                 # 1 = mais recentes primeiro
    "languages": ["english"],    # atenção: agora é uma LISTA, e o nome é "languages"
    "purchase_type": 1,          # 1 = todas as compras
    "num_per_page": 5,
    "cursor": "*",
}

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
print(dados.get("cursor"))