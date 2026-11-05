# Analisador de emoção de reviews de jogos

Trabalho de faculdade (grupo de 3). O usuário digita o nome de um jogo, o programa busca as
reviews na Steam, uma rede neural classifica cada uma como positiva ou negativa e a tela mostra
o resultado com um resumo em texto.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run src/app.py         # a tela já funciona com dados falsos (USAR_MOCKS = True)
```

Para treinar o modelo (depois que o dataset existir em `data/reviews.csv`):
```bash
python -m src.modelo
```

## Estrutura

| Pasta/arquivo | O que tem | Responsável |
|---|---|---|
| `src/coleta.py` | Busca de jogos e reviews na Steam, montagem do dataset | Pessoa 1 |
| `src/limpeza.py` | Limpeza e balanceamento dos textos | Pessoa 1 |
| `src/modelo.py` | Treino, avaliação e previsão da rede neural | Pessoa 2 |
| `src/analise.py` | Estatísticas e resumo em texto | Pessoa 3 |
| `src/app.py` | Tela única (Streamlit) | Pessoa 3 |
| `src/mocks.py` | Funções falsas para testar a tela antes do resto ficar pronto | Pessoa 3 |
| `data/`, `models/` | Dataset e modelo treinado | — |
| `docs/` | Relatório, prints e roteiro | Todos |

## Contrato entre as partes

```python
buscar_jogo(nome) -> list[dict]                  # [{"appid": 570, "nome": "Dota 2"}]
buscar_reviews(appid, n) -> list[str]            # textos das reviews
prever(textos) -> list[float]                    # probabilidade de ser positiva (0 a 1)
analisar(nome_jogo, textos, probabilidades) -> dict
resumir(estatisticas) -> str
```

O formato do dict de estatísticas está descrito em `src/analise.py`.

## Fluxo de trabalho no Git

- A branch `main` deve estar sempre funcionando.
- Cada um trabalha em uma branch própria (`feature/coleta`, `feature/modelo`, `feature/app`).
- Para entrar na `main`: Pull Request revisado por um colega.
- Commits pequenos, com mensagens claras. Rode `git pull` antes de começar a trabalhar.
- Cada pessoa mexe nos seus arquivos, para evitar conflitos.
