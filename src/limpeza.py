"""Limpeza e balanceamento dos textos.  (Responsável: Pessoa 1)"""
import pandas as pd


def limpar_texto(texto: str) -> str:
    """Normaliza um texto (minúsculas, espaços, remove lixo como ASCII art)."""
    raise NotImplementedError


def limpar_dataframe(df: pd.DataFrame, min_palavras: int = 3) -> pd.DataFrame:
    """Aplica limpar_texto, remove reviews muito curtas e duplicadas."""
    raise NotImplementedError


def balancear(df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """Equilibra positivas e negativas (a Steam tem muito mais positivas)."""
    raise NotImplementedError
