"""Versões FALSAS das funções, para a tela funcionar antes das partes reais ficarem prontas.

Quando as funções reais estiverem prontas, ponha USAR_MOCKS = False em src/app.py.
"""
import random
from collections import Counter

_JOGOS = [{"appid": 570, "nome": "Dota 2"}, {"appid": 730, "nome": "Counter-Strike 2"},
          {"appid": 1245620, "nome": "Elden Ring"}]
_POSITIVAS = ["Great game, super fun with friends", "Amazing graphics and story", "Best purchase this year"]
_NEGATIVAS = ["Too many bugs, constant crashes", "Overpriced and repetitive", "Servers are terrible"]


def buscar_jogo(nome: str) -> list[dict]:
    return [j for j in _JOGOS if nome.lower() in j["nome"].lower()]


def buscar_reviews(appid: int, n: int = 100, idioma: str = "english") -> list[str]:
    rnd = random.Random(appid)
    return [rnd.choice(_POSITIVAS + _NEGATIVAS) for _ in range(n)]


def prever(textos: list[str]) -> list[float]:
    return [0.9 if t in _POSITIVAS else 0.1 for t in textos]


def analisar(nome_jogo: str, textos: list[str], probabilidades: list[float]) -> dict:
    pares = list(zip(textos, probabilidades))
    pos = [t for t, p in pares if p >= 0.5]
    neg = [t for t, p in pares if p < 0.5]
    total = len(pares) or 1
    palavras = Counter(w for t in neg for w in t.lower().split() if len(w) > 4)
    return {
        "jogo": nome_jogo,
        "total": len(pares),
        "pct_positivas": 100 * len(pos) / total,
        "pct_negativas": 100 * len(neg) / total,
        "exemplos_positivos": pos[:3],
        "exemplos_negativos": neg[:3],
        "palavras_negativas": [w for w, _ in palavras.most_common(3)],
    }


def resumir(est: dict) -> str:
    texto = (f"{est['pct_positivas']:.0f}% das {est['total']} reviews analisadas de "
             f"{est['jogo']} são positivas.")
    if est["palavras_negativas"]:
        texto += " As críticas mais comuns citam: " + ", ".join(est["palavras_negativas"]) + "."
    return texto
