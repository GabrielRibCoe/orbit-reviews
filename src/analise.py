"""Agregação dos resultados e resumo em texto.  (Responsável: Pessoa 3)

Formato das estatísticas (dict) que `analisar` devolve e `resumir` consome:
    {
        "jogo": str,
        "total": int,                      # quantas reviews foram analisadas
        "pct_positivas": float,            # 0 a 100
        "pct_negativas": float,            # 0 a 100
        "exemplos_positivos": list[str],   # 2 ou 3 reviews
        "exemplos_negativos": list[str],   # 2 ou 3 reviews
        "palavras_negativas": list[str],   # termos mais frequentes nas negativas
    }
"""
from collections import Counter


def analisar(nome_jogo: str, textos: list[str], probabilidades: list[float]) -> dict:
    """Junta textos + probabilidades da rede e calcula as estatísticas acima."""
    pares = list(zip(textos, probabilidades))
    
    # Separando positivas (probabilidade >= 0.5) e negativas (probabilidade < 0.5)
    pos = [t for t, p in pares if p >= 0.5]
    neg = [t for t, p in pares if p < 0.5]
    
    total = len(pares) if len(pares) > 0 else 1
    
    pct_positivas = (len(pos) / total) * 100
    pct_negativas = (len(neg) / total) * 100
    
    # Extraindo palavras mais frequentes nas reviews negativas (ignorando palavras muito curtas)
    palavras_totais = []
    for t in neg:
        for w in t.lower().split():
            # Limpa pontuação simples e pega palavras com mais de 3 letras
            w_limpa = "".join(ch for ch in w if ch.isalnum())
            if len(w_limpa) > 3:
                palavras_totais.append(w_limpa)
                
    contador_palavras = Counter(palavras_totais)
    palavras_negativas = [palavra for palavra, _ in contador_palavras.most_common(3)]

    return {
        "jogo": nome_jogo,
        "total": len(pares),
        "pct_positivas": pct_positivas,
        "pct_negativas": pct_negativas,
        "exemplos_positivos": pos[:3],         # Pega até 3 exemplos
        "exemplos_negativos": neg[:3],         # Pega até 3 exemplos
        "palavras_negativas": palavras_negativas,
    }


def resumir(estatisticas: dict) -> str:
    """Gera o textinho explicativo baseado nas estatísticas calculadas."""
    total = estatisticas["total"]
    jogo = estatisticas["jogo"]
    pct_pos = estatisticas["pct_positivas"]
    
    texto = f"{pct_pos:.0f}% das {total} reviews analisadas de {jogo} são positivas."
    
    if estatisticas["palavras_negativas"]:
        termos = ", ".join(estatisticas["palavras_negativas"])
        texto += f" As críticas mais comuns citam termos como: {termos}."
        
    return texto