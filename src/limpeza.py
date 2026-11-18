"""Limpeza e balanceamento dos textos.  (Responsável: Pessoa 1)

Uso (na raiz do projeto):  python -m src.limpeza
Lê data/reviews.csv (bruto) e grava data/reviews_limpo.csv (limpo, sem balancear).
"""
import re
import unicodedata

import pandas as pd

def limpar_texto(texto: str) -> str:
    """Limpa UM texto: remove etiquetas do Steam ([b], [h1], [url=...]...) e links,
    junta espaços e quebras de linha, tira espaços das pontas e põe em minúsculas.
    Mantém pontuação e notas como "[10/10]". Deixa só caracteres ASCII (acentos são
    simplificados, emojis e símbolos removidos). Devolve "" se não for texto.
    """
    if not isinstance(texto, str):
        return ""
    texto = re.sub(r"\[/?(?:h[1-3]|b|i|u|strike|spoiler|noparse|hr|quote|url|list|olist|table|tr|th|td|code|img|\*)(?:=[^\]]*)?\]", " ", texto)  # remove BBCode
    texto = re.sub(r"https?://\S+", " ", texto)  # remove links
    # Só ASCII: acentos viram a letra simples (café -> cafe); emojis e símbolos somem.
    # Evita erro ao salvar o modelo no Windows (o vocabulário é gravado com a codificação padrão).
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"\s+", " ", texto)
    texto = texto.strip()
    texto = texto.lower()
    return texto


def limpar_dataframe(df: pd.DataFrame, min_palavras: int = 2) -> pd.DataFrame:
    """Limpa a tabela (colunas texto, rotulo, appid) e devolve uma cópia nova.

    Ordem: limpa os textos -> remove textos sem letras nem números -> remove textos
    com menos de `min_palavras` palavras -> remove textos que aparecem com rótulos
    contraditórios (por inteiro) -> remove duplicados -> renumera as linhas.
    """
    df = df.copy()
    df["texto"] = df["texto"].apply(limpar_texto)
    df = df[df["texto"].str.contains(r"\w", regex=True)]
    n_palavras = df["texto"].str.split().str.len()
    df = df[n_palavras >= min_palavras]
    rotulos_por_texto = df.groupby("texto")["rotulo"].nunique()
    conflitos = rotulos_por_texto[rotulos_por_texto > 1].index
    df = df[~df["texto"].isin(conflitos)]
    df = df.drop_duplicates(subset="texto")
    return df.reset_index(drop=True)


def balancear(df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """Iguala positivas e negativas sorteando linhas da classe maior (undersampling).

    Todas as linhas da classe menor são mantidas. `seed` torna o sorteio reproduzível.
    Se houver só uma classe, devolve a tabela sem alterar.
    """
    if df["rotulo"].nunique() < 2:
        print("Aviso: só existe uma classe, nada para balancear.")
        return df.reset_index(drop=True)
    menor = df["rotulo"].value_counts().min()
    equilibrado = df.groupby("rotulo").sample(n=menor, random_state=seed)
    return equilibrado.sample(frac=1, random_state=seed).reset_index(drop=True)  # embaralha

if __name__ == "__main__":
    df = pd.read_csv("data/reviews.csv", encoding="utf-8")
    limpo = limpar_dataframe(df, min_palavras=2)
    limpo.to_csv("data/reviews_limpo.csv", index=False, encoding="utf-8")

    print(f"{len(df)} -> {len(limpo)} linhas")
    print(limpo["rotulo"].value_counts())