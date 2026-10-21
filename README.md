# Fluxo 🎬 — Análise de Obras Audiovisuais com IA

> 🇺🇸 [Read this in English](README.en.md)

![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)
![Versão](https://img.shields.io/badge/vers%C3%A3o-0.1.0-green)

Um **fluxo de prompts especializado em 3 etapas** para dissecar filmes e
séries com a ajuda de uma IA (Claude, ChatGPT, Gemini etc.) — em suas camadas
narrativas, técnicas, artísticas e culturais. Em vez de um resumo genérico, o
fluxo conduz uma análise progressiva: **mapear → aprofundar → sintetizar**.

---

## O fluxo em 3 etapas

| Etapa | O que faz | Template | Comando |
| ----- | --------- | -------- | ------- |
| **1 · Análise Audiovisual 360°** | "Raio-x" da obra em **7 dimensões**: contexto de produção, narrativa, imagem, som, montagem, sociocultural e recepção | [`etapa-01`](prompts/etapa-01-analise-360.md) | `fluxo gerar 1` |
| **2.1 · Proposta de Aprofundamento** | A IA propõe de **3 a 5 perguntas analíticas** com base no mapa da Etapa 1 — você escolhe uma | [`etapa-02.1`](prompts/etapa-02.1-proposta-aprofundamento.md) | `fluxo gerar 2.1` |
| **2.2 · Análise Focada** | Mergulho na pergunta escolhida: **tese → evidências → análise → contexto** | [`etapa-02.2`](prompts/etapa-02.2-analise-focada.md) | `fluxo gerar 2.2` |
| **3 · Síntese e Conexões** | Consolida os insights, sugere **obras em diálogo**, perguntas de reflexão e **fontes** (crítica, teoria e bastidores) | [`etapa-03`](prompts/etapa-03-sintese-conexoes.md) | `fluxo gerar 3` |

> 📖 **Guia completo:** [docs/fluxo.md](docs/fluxo.md) — lógica de cada etapa,
> as 7 dimensões explicadas, adaptações para séries/documentários, boas
> práticas, limitações e glossário.

---

## Início rápido

### Opção A — copiar e colar (sem instalar nada)

1. Abra [`prompts/etapa-01-analise-360.md`](prompts/etapa-01-analise-360.md);
2. Copie o texto entre os marcadores `<!-- INICIO DO PROMPT -->` e
   `<!-- FIM DO PROMPT -->`;
3. Substitua os placeholders `{{TITULO_DA_OBRA}}` e `{{DIRETOR_OU_CRIADOR}}`
   e cole na sua IA favorita;
4. **Na mesma conversa**, siga para as etapas 2.1, 2.2 e 3.

### Opção B — CLI (Python 3.9+, zero dependências)

```bash
# Instale a CLI a partir do repositório
# (se o seu Python for gerenciado pelo sistema — erro "PEP 668" —, crie um
#  ambiente virtual antes: python -m venv .venv && source .venv/bin/activate)
pip install -e .

# Veja as etapas e o que cada uma requer
fluxo listar

# Etapa 1 — Análise 360°
fluxo gerar 1 --titulo "Cidade de Deus (2002)" --diretor "Fernando Meirelles e Kátia Lund"

# Etapa 2.1 — proposta de perguntas
fluxo gerar 2.1 --titulo "Cidade de Deus (2002)"

# Etapa 2.2 — cole aqui a pergunta escolhida
fluxo gerar 2.2 --pergunta "Como a montagem acelerada transforma a violência em espetáculo...?"

# Etapa 3 — síntese final, já copiada para a área de transferência
fluxo gerar 3 --titulo "Cidade de Deus (2002)" --copiar
```

Sem instalar, direto da raiz do repo: `PYTHONPATH=src python -m fluxo listar`.

**Atalho:** crie de uma vez a pasta da análise com os 4 prompts + um registro
para suas anotações:

```bash
fluxo novo --titulo "Cidade de Deus (2002)" --diretor "Fernando Meirelles e Kátia Lund"
# cria analises/cidade-de-deus-2002/ com todos os prompts e um registro.md
```

### Comandos da CLI

| Comando | Descrição |
| ------- | --------- |
| `fluxo listar` | Lista as etapas e os dados que cada uma requer |
| `fluxo gerar <etapa>` | Gera o prompt da etapa (`1`, `2.1`, `2.2`, `3`). Flags: `--titulo`, `--diretor`, `--pergunta`, `--salvar arquivo`, `--copiar` |
| `fluxo novo --titulo "..."` | Cria `analises/<slug>/` com os 4 prompts preenchidos e um `registro.md`. Flags: `--diretor`, `--pergunta`, `--slug`, `--destino`, `--forcar` |
| `fluxo --versao` | Mostra a versão |

---

## Exemplo

Em [`exemplos/cidade-de-deus/`](exemplos/cidade-de-deus) você encontra o fluxo
completo já preenchido para **Cidade de Deus (2002)** — os 4 prompts prontos
para colar, um exemplo de perguntas que a Etapa 2.1 costuma gerar e o registro
da análise.

---

## Estrutura do repositório

```
fluxo/
├── README.md / README.en.md       # Este guia (PT-BR / English)
├── docs/
│   └── fluxo.md                   # Guia completo do fluxo
├── prompts/                       # ★ Os templates das etapas (fonte da verdade)
│   ├── etapa-01-analise-360.md
│   ├── etapa-02.1-proposta-aprofundamento.md
│   ├── etapa-02.2-analise-focada.md
│   └── etapa-03-sintese-conexoes.md
├── templates/
│   └── registro-de-analise.md     # Modelo para registrar os achados
├── exemplos/
│   └── cidade-de-deus/            # Exemplo preenchido, ponta a ponta
├── src/fluxo/                     # CLI em Python (sem dependências)
│   ├── core.py                    # Leitura dos templates e preenchimento
│   └── cli.py                     # Comandos listar / gerar / novo
└── tests/                         # Testes automatizados (unittest)
```

As análises que você criar com `fluxo novo` vão para `analises/` — versione-as
ou ignore-as, como preferir.

---

## Testes

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Próximos passos (plano faseado)

O projeto está evoluindo em fases, a partir de uma
[análise crítica](docs/analise-critica.md) do próprio fluxo:

- [x] **Fase 1 — Prompts v2**: persona e regras anti-alucinação, formato de
  saída estruturado, contra-argumento na Etapa 2.2 e novos subitens teóricos
  (atuação, autoria, gênero, espectador)
- [ ] **Fase 2 — UI web**: página estática para montar e copiar os prompts sem terminal
- [ ] **Fase 3 — Estrutura**: Etapa 0 (setup + sua hipótese), Etapa 1 em dois tempos, close reading (2.3)
- [ ] **Fase 4 — Variantes e base**: séries, análise comparativa, modos
  iniciante × acadêmico, CLI interativa e empacotamento dos prompts

Ideias para mais adiante: tradução dos prompts (EN/ES) e integração opcional
com APIs de LLMs.

## Contribuindo

Sugestões de melhoria nos prompts são muito bem-vindas — veja
[CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

[MIT](LICENSE) © Lucas Rangel — use, adapte e compartilhe à vontade. Bons filmes! 🍿
