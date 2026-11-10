import pandas as pd

linhas = [
    {"texto": "adorei", "rotulo": 1, "appid": 570},
    {"texto": "horrível", "rotulo": 0, "appid": 570},
]
df = pd.DataFrame(linhas)
print(df)
print(df.shape)                   # (2, 3): 2 linhas, 3 colunas
print(df["rotulo"].value_counts())  # conta quantos 1 e quantos 0