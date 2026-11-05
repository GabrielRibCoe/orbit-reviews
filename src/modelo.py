"""Rede neural de classificação (positiva x negativa).  (Responsável: Pessoa 2)

Sugestão: Keras com TextVectorization -> Embedding -> GlobalAveragePooling1D -> Dense -> sigmoide.
Alternativa mais leve: TF-IDF + MLPClassifier (scikit-learn).
"""
CAMINHO_MODELO = "models/modelo_reviews.keras"


def treinar(caminho_csv: str = "data/reviews.csv", salvar_em: str = CAMINHO_MODELO) -> dict:
    """Treina o modelo, avalia no conjunto de teste e salva em `salvar_em`.

    Retorna as métricas, por exemplo: {"acuracia": 0.85, "f1": 0.84}.
    Dica: guarde também a matriz de confusão para o relatório.
    """
    raise NotImplementedError


def carregar_modelo(caminho: str = CAMINHO_MODELO):
    """Carrega o modelo já treinado (chamado uma vez pelo app)."""
    raise NotImplementedError


def prever(textos: list[str]) -> list[float]:
    """Recebe textos e devolve, para cada um, a probabilidade (0 a 1) de ser POSITIVO."""
    raise NotImplementedError


if __name__ == "__main__":
    # Para treinar: python -m src.modelo
    print(treinar())
