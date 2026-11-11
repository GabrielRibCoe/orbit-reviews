"""Rede neural de classificação (positiva x negativa).  (Responsável: Pessoa 2)

Arquitetura: TextVectorization -> Embedding -> GlobalAveragePooling1D -> Dense -> sigmoide.
A vetorização fica DENTRO do modelo salvo, então `prever` recebe texto puro.
"""
import json
import os

import numpy as np
import pandas as pd

CAMINHO_MODELO = "models/modelo_reviews.keras"
CAMINHO_METRICAS = "models/metricas.json"

VOCAB_MAX = 20000
TAMANHO_SEQ = 200
DIM_EMBEDDING = 64

_modelo = None  # cache: o modelo é carregado só uma vez


def _preparar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Usa a limpeza da Pessoa 1 se já existir; senão, faz uma limpeza mínima."""
    try:
        from src.limpeza import balancear, limpar_dataframe

        return balancear(limpar_dataframe(df))
    except NotImplementedError:
        df = df.dropna(subset=["texto"]).copy()
        df["texto"] = df["texto"].astype(str).str.strip()
        df = df[df["texto"].str.split().str.len() >= 3]
        return df.drop_duplicates(subset="texto")


def _dividir(df: pd.DataFrame, jogo_teste: int | None, seed: int):
    """Devolve (treino, validação, teste).

    Se `jogo_teste` for um appid, esse jogo inteiro vira o teste (mede se o
    modelo generaliza para um jogo que nunca viu). Senão, divisão aleatória.
    """
    from sklearn.model_selection import train_test_split

    if jogo_teste is not None:
        teste = df[df["appid"] == jogo_teste]
        resto = df[df["appid"] != jogo_teste]
    else:
        resto, teste = train_test_split(
            df, test_size=0.15, stratify=df["rotulo"], random_state=seed
        )
    treino, val = train_test_split(
        resto, test_size=0.15, stratify=resto["rotulo"], random_state=seed
    )
    return treino, val, teste


def _construir(textos_treino):
    import keras
    from keras import layers
    import tensorflow as tf

    vetorizador = layers.TextVectorization(
        max_tokens=VOCAB_MAX,
        output_mode="int",
        output_sequence_length=TAMANHO_SEQ,
    )
    vetorizador.adapt(textos_treino)  # vocabulário só com o treino

    entrada = keras.Input(shape=(), dtype=tf.string)
    x = vetorizador(entrada)
    x = layers.Embedding(VOCAB_MAX, DIM_EMBEDDING)(x)
    x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dense(32, activation="relu")(x)
    x = layers.Dropout(0.4)(x)
    saida = layers.Dense(1, activation="sigmoid")(x)

    modelo = keras.Model(entrada, saida)
    modelo.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return modelo


def treinar(
    caminho_csv: str = "data/reviews.csv",
    salvar_em: str = CAMINHO_MODELO,
    jogo_teste: int | None = None,
    epocas: int = 10,
    seed: int = 42,
) -> dict:
    """Treina o modelo, avalia no conjunto de teste e salva em `salvar_em`.

    Retorna as métricas: {"acuracia", "f1", "matriz_confusao", "n_teste"}.
    Use `jogo_teste=<appid>` para testar em um jogo que ficou fora do treino.
    """
    import keras
    from sklearn.metrics import accuracy_score, confusion_matrix, f1_score

    keras.utils.set_random_seed(seed)

    df = pd.read_csv(caminho_csv)
    df = _preparar_dados(df)
    treino, val, teste = _dividir(df, jogo_teste, seed)

    modelo = _construir(treino["texto"].to_numpy())
    modelo.fit(
        treino["texto"].to_numpy(),
        treino["rotulo"].to_numpy(),
        validation_data=(val["texto"].to_numpy(), val["rotulo"].to_numpy()),
        epochs=epocas,
        batch_size=64,
        callbacks=[keras.callbacks.EarlyStopping(patience=2, restore_best_weights=True)],
        verbose=2,
    )

    probs = modelo.predict(teste["texto"].to_numpy(), verbose=0).ravel()
    pred = (probs >= 0.5).astype(int)
    y = teste["rotulo"].to_numpy()

    metricas = {
        "acuracia": float(accuracy_score(y, pred)),
        "f1": float(f1_score(y, pred)),
        "matriz_confusao": confusion_matrix(y, pred).tolist(),  # [[TN, FP], [FN, TP]]
        "n_teste": int(len(y)),
    }

    os.makedirs(os.path.dirname(salvar_em) or ".", exist_ok=True)
    modelo.save(salvar_em)
    with open(CAMINHO_METRICAS, "w", encoding="utf-8") as f:
        json.dump(metricas, f, indent=2)

    global _modelo
    _modelo = modelo
    return metricas


def carregar_modelo(caminho: str = CAMINHO_MODELO):
    """Carrega o modelo já treinado (só na primeira chamada; depois usa o cache)."""
    global _modelo
    if _modelo is None:
        import keras

        _modelo = keras.models.load_model(caminho)
    return _modelo


def prever(textos: list[str]) -> list[float]:
    """Recebe textos e devolve, para cada um, a probabilidade (0 a 1) de ser POSITIVO."""
    if not textos:
        return []
    modelo = carregar_modelo()
    entrada = np.array([str(t) for t in textos], dtype=object)
    return modelo.predict(entrada, verbose=0).ravel().astype(float).tolist()


if __name__ == "__main__":
    # Para treinar: python -m src.modelo
    print(treinar())
