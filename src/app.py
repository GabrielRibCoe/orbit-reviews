"""Tela única (Streamlit).  (Responsável: Pessoa 3)

Para rodar, na raiz do projeto:  streamlit run src/app.py
"""
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import streamlit as st

USAR_MOCKS = False  # True = dados falsos (para testar só a tela)

if USAR_MOCKS:
    from src.mocks import analisar, buscar_jogo, buscar_reviews, prever, resumir
else:
    from src.analise import analisar, resumir
    from src.coleta import buscar_jogo, buscar_reviews
    from src.modelo import CAMINHO_MODELO, prever

st.title("Analisador de emoção de reviews de jogos")

if not USAR_MOCKS and not os.path.exists(CAMINHO_MODELO):
    st.error("Modelo não encontrado. Treine primeiro, na raiz do projeto: python -m src.modelo")
    st.stop()

nome = st.text_input("Nome do jogo")

if st.button("Analisar") and nome.strip():
    jogos = buscar_jogo(nome)
    if not jogos:
        st.warning("Nenhum jogo encontrado. Tente outro nome.")
    else:
        jogo = jogos[0]  # TODO: se houver vários resultados, deixar o usuário escolher (st.selectbox)
        with st.spinner("Buscando e analisando as reviews..."):
            textos = buscar_reviews(jogo["appid"], n=100)
        if not textos:
            st.warning("Esse jogo não tem reviews suficientes.")
        else:
            with st.spinner("Classificando com a rede neural..."):
                probs = prever(textos)
            est = analisar(jogo["nome"], textos, probs)

            st.subheader(est["jogo"])
            col1, col2 = st.columns(2)
            col1.metric("Positivas", f"{est['pct_positivas']:.0f}%")
            col2.metric("Negativas", f"{est['pct_negativas']:.0f}%")
            st.progress(est["pct_positivas"] / 100)

            st.write(resumir(est))

            with st.expander("Exemplos de reviews"):
                st.markdown("**Positivas**")
                for t in est["exemplos_positivos"]:
                    st.write(f"- {t}")
                st.markdown("**Negativas**")
                for t in est["exemplos_negativos"]:
                    st.write(f"- {t}")