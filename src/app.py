"""Tela única (Streamlit).  (Responsável: Pessoa 3)

Para rodar, na raiz do projeto:  streamlit run src/app.py
"""
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import streamlit as st

USAR_MOCKS = False  # True = dados falsos (para testar só a tela)

if USAR_MOCKS:
    from src.mocks import analisar, buscar_jogo, buscar_reviews, prever, resumir
else:
    from src.analise import analisar, resumir
    from src.coleta import buscar_jogo, buscar_reviews
    from src.modelo import CAMINHO_MODELO, prever

# ---------------------------------------------------------------- identidade
ASSETS = RAIZ / "assets"
ROXO = "#8F06E4"       # cor primária da Orbit
ROXO_ESCURO = "#2A0A45"  # texto e títulos
LAVANDA = "#F1E3FB"    # superfícies e trilhos
ROSA = "#E8457C"       # único contraponto: reviews negativas

st.set_page_config(
    page_title="Orbit | Reviews de jogos",
    page_icon=str(ASSETS / "favicon.png"),
    layout="centered",
)


def _b64(nome: str) -> str:
    return base64.b64encode((ASSETS / nome).read_bytes()).decode()


LOGO_BRANCA = _b64("orbit_logo_branca.png")
PLANETA_ROXO = _b64("orbit_planeta_roxo.png")

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&display=swap');

html, body, .stApp, .stApp p, .stApp label, .stApp button, .stApp input,
.stApp h1, .stApp h2, .stApp h3, .stApp li, [data-testid="stMetric"] * {{
    font-family: 'Jost', 'Futura', 'Segoe UI', sans-serif;
}}
/* mantém a fonte de ícones do Streamlit (setas do expander etc.) */
[data-testid="stIconMaterial"], .material-icons, [class*="material-symbols"] {{
    font-family: 'Material Symbols Rounded', 'Material Icons' !important;
}}
#MainMenu, footer {{ visibility: hidden; }}
/* a barra superior do Streamlit é fixa: deixa espaço para o banner não ficar escondido */
[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{ padding-top: 5rem; max-width: 760px; }}

/* cabeçalho com a marca */
.orbit-header {{
    background: {ROXO};
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 1.75rem;
}}
.orbit-header img {{ height: 44px; display: block; }}
.orbit-header p {{
    color: #fff; opacity: .9; margin: 14px 0 0; font-size: 1.05rem; letter-spacing: .01em;
}}

/* títulos */
h1, h2, h3 {{ color: {ROXO_ESCURO}; font-weight: 600; letter-spacing: -.01em; }}

/* campo e botão */
.stTextInput input {{ border: 1.5px solid #D9B8F2; border-radius: 10px; background: #fff; }}
.stTextInput input:focus {{ border-color: {ROXO}; box-shadow: 0 0 0 3px rgba(143,6,228,.18); }}
.stButton > button {{
    background: {ROXO}; color: #fff; border: 0; border-radius: 10px;
    padding: .55rem 1.6rem; font-weight: 500;
}}
.stButton > button:hover {{ background: #7A05C2; color: #fff; }}
.stButton > button:focus-visible {{ outline: 3px solid rgba(143,6,228,.35); outline-offset: 2px; }}

/* métricas */
[data-testid="stMetricValue"] {{ font-weight: 600; font-size: 2.6rem; }}
[data-testid="stMetric"]:nth-of-type(1) [data-testid="stMetricValue"] {{ color: {ROXO}; }}
[data-testid="stColumn"]:nth-of-type(2) [data-testid="stMetricValue"] {{ color: {ROSA}; }}

/* barra positivas x negativas */
.barra {{ display: flex; height: 14px; border-radius: 999px; overflow: hidden; background: {LAVANDA}; }}
.barra .pos {{ background: {ROXO}; }}
.barra .neg {{ background: {ROSA}; }}

/* resumo */
.resumo {{
    background: {LAVANDA}; border-left: 5px solid {ROXO};
    border-radius: 0 12px 12px 0; padding: 16px 20px; margin: 1.25rem 0;
    color: {ROXO_ESCURO}; font-size: 1.05rem;
}}

/* exemplos */
[data-testid="stExpander"] {{ border: 1.5px solid #E6CDF7; border-radius: 12px; background: #fff; }}

/* rodapé */
.orbit-rodape {{ display: flex; align-items: center; gap: 10px; margin-top: 3rem; color: {ROXO_ESCURO}; opacity: .7; font-size: .9rem; }}
.orbit-rodape img {{ height: 28px; }}
</style>

<div class="orbit-header">
    <img src="data:image/png;base64,{LOGO_BRANCA}" alt="Orbit">
    <p>Descubra o que os jogadores realmente sentem sobre um jogo.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- tela
st.title("Analisador de emoção de reviews de jogos")
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
            st.markdown(
                f'<div class="barra" role="img" aria-label="{est["pct_positivas"]:.0f}% positivas">'
                f'<div class="pos" style="width:{est["pct_positivas"]}%"></div>'
                f'<div class="neg" style="width:{est["pct_negativas"]}%"></div></div>',
                unsafe_allow_html=True,
            )

            st.markdown(f'<div class="resumo">{resumir(est)}</div>', unsafe_allow_html=True)

            with st.expander("Exemplos de reviews"):
                st.markdown("**Positivas**")
                for t in est["exemplos_positivos"]:
                    st.write(f"- {t}")
                st.markdown("**Negativas**")
                for t in est["exemplos_negativos"]:
                    st.write(f"- {t}")
