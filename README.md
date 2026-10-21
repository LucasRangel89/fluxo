# Fluxo 🎬 — Análise de Obras Audiovisuais com IA

> 🇺🇸 [Read this in English](README.en.md)

![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-blue)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)
![Versão](https://img.shields.io/badge/vers%C3%A3o-1.1.0-green)

Um **fluxo de prompts especializado** para dissecar filmes e séries com a
ajuda de uma IA (Claude, ChatGPT, Gemini etc.) — em suas camadas narrativas,
técnicas, artísticas e culturais. Em vez de um resumo genérico, o Fluxo
conduz uma **sessão guiada**: **preparar → pesquisar → mapear → aprofundar →
sintetizar**, com um modo **Prompt Maestro** que coloca a jornada inteira em
uma única conversa.

---

## O fluxo (três atos, com preparação e variações)

| Etapa | O que faz | Template | Comando |
| ----- | --------- | -------- | ------- |
| **0 · Preparação** *(opcional)* | Identifica a obra, calibra seu objetivo/nível e **registra sua hipótese antes de a IA opinar** — revisitada na Etapa 3 | [`etapa-00`](prompts/etapa-00-preparacao.md) | `fluxo gerar 0` |
| **R · Pesquisa e Dossiê de Fontes** *(recomendada)* | Separa **fato de interpretação**: ficha verificável, produção, recepção, debates e fontes nomeadas, sem afirmar o que não pode ser confirmado | [`etapa-00r`](prompts/etapa-00r-pesquisa-fontes.md) | `fluxo gerar r` |
| **1 · Análise Audiovisual 360°** | "Raio-x" da obra em **7 dimensões**: contexto de produção, narrativa, imagem, som, montagem, sociocultural e recepção | [`etapa-01`](prompts/etapa-01-analise-360.md) | `fluxo gerar 1` |
| **1A + 1B · 360° em dois tempos** *(alternativa à Etapa 1)* | O mesmo raio-x dividido: **Texto** (narrativa, imagem, som, montagem) → **Contexto** (produção, sociocultural, recepção), fechando com a tabela completa das 7 dimensões | [`etapa-01a`](prompts/etapa-01a-analise-texto.md) · [`etapa-01b`](prompts/etapa-01b-analise-contexto.md) | `fluxo gerar 1a` / `1b` |
| **1S · Análise 360° de Série** *(variante para séries)* | O raio-x pensado para temporadas: **arcos em 3 níveis** (série, temporada, episódio), piloto, cliffhangers, **showrunner** e modelo de exibição | [`etapa-01s`](prompts/etapa-01s-analise-serie.md) | `fluxo gerar 1s` |
| **2.1 · Proposta de Aprofundamento** | A IA propõe de **3 a 5 perguntas analíticas** com base no mapa da Etapa 1 — você escolhe uma | [`etapa-02.1`](prompts/etapa-02.1-proposta-aprofundamento.md) | `fluxo gerar 2.1` |
| **2.2 · Análise Focada** | Mergulho na pergunta escolhida: **tese → evidências → análise → contexto** | [`etapa-02.2`](prompts/etapa-02.2-analise-focada.md) | `fluxo gerar 2.2` |
| **2.3 · Close Reading** *(opcional)* | **Uma sequência dissecada plano a plano**: decupagem, mise-en-scène, som, montagem e o sentido construído pela forma | [`etapa-02.3`](prompts/etapa-02.3-close-reading.md) | `fluxo gerar 2.3` |
| **3 · Síntese e Conexões** | Consolida os insights, julga a obra (balanço crítico), sugere **obras em diálogo**, perguntas de reflexão — incluindo o **antes/depois da sua leitura** — e **fontes** | [`etapa-03`](prompts/etapa-03-sintese-conexoes.md) | `fluxo gerar 3` |
| **4 · Comparativa** *(variante)* | **Duas obras frente a frente** sob um eixo (remake, mesmo diretor, mesmo tema): cartões, comparação em pares, juízo por critérios e **tabela-síntese** | [`etapa-04`](prompts/etapa-04-comparativa.md) | `fluxo gerar 4` |

> 📖 **Guia completo:** [docs/fluxo.md](docs/fluxo.md) — lógica de cada etapa,
> as 7 dimensões explicadas, adaptações para séries/documentários, boas
> práticas, limitações e glossário.

---

## Início rápido

### Opção A — Interface web (recomendado) 🌐

A forma mais simples de usar o Fluxo: diga **qual obra**, escolha
**filme/longa, dois tempos, série ou comparativa** e clique em **“Montar
minha sessão”**. A interface busca metadados sem chave (Wikipedia/Wikidata e
TVMaze), monta um dossiê editável e libera os cartões na ordem certa, com
progresso, dependências e uma “próxima ação” sempre visível. O caminho padrão
continua gratuito: copiar o prompt e abrir a sua IA. Opcionalmente, você pode
executar no próprio navegador com **Puter** (conta/créditos seus), **sua API**
(BYOK compatível com OpenAI) ou **IA local** quando o Chrome oferecer esse
recurso. Também é possível colar as respostas de volta para selecionar a
pergunta da Etapa 2.1, gerar um contexto de continuidade e exportar a sessão.

- **Rodando localmente:** na raiz do repo, `python -m http.server 8000` e abra
  `http://localhost:8000` (precisa ser via HTTP: a página lê os templates de
  `prompts/` em tempo real — a mesma fonte da CLI, sem duplicação).
- **Publicando no GitHub Pages:** *Settings → Pages → Deploy from a branch →
  `main`, pasta `/ (root)`*. O arquivo `.nojekyll` já incluso garante que os
  templates sejam servidos como estão.

### Opção B — copiar e colar (sem instalar nada)

1. Abra [`prompts/etapa-01-analise-360.md`](prompts/etapa-01-analise-360.md);
2. Copie o texto entre os marcadores `<!-- INICIO DO PROMPT -->` e
   `<!-- FIM DO PROMPT -->`;
3. Substitua os placeholders `{{TITULO_DA_OBRA}}` e `{{DIRETOR_OU_CRIADOR}}`
   e cole na sua IA favorita;
4. **Na mesma conversa**, siga para as etapas 2.1, 2.2 e 3.

### Opção C — CLI (Python 3.9+, zero dependências)

```bash
# Instale a CLI a partir do repositório
# (se o seu Python for gerenciado pelo sistema — erro "PEP 668" —, crie um
#  ambiente virtual antes: python -m venv .venv && source .venv/bin/activate)
pip install -e .

# Veja as etapas e o que cada uma requer
fluxo listar

# Sessão guiada: só as etapas da trilha + Prompt Maestro + manifesto JSON
fluxo sessao --trilha padrao --titulo "Cidade de Deus (2002)" \
  --diretor "Fernando Meirelles e Kátia Lund"

# Ou um único prompt para conduzir a conversa inteira (com pausas de escolha)
fluxo maestro --trilha serie --titulo "Dark — Temporada 1 (2017)" \
  --diretor "Baran bo Odar e Jantje Friese" --copiar

# Etapa 0 (opcional) — preparação: sua hipótese registrada antes da IA opinar
fluxo gerar 0 --titulo "Cidade de Deus (2002)" --diretor "Fernando Meirelles e Kátia Lund" \
  --tipo "Filme" --objetivo "Estudar um clássico" --nivel "Intermediário" \
  --impressoes "Achei a violência espetacularizada demais; quero testar essa impressão."

# Etapa 1 — Análise 360° (alternativa em dois tempos: `gerar 1a`, depois `gerar 1b`)
fluxo gerar 1 --titulo "Cidade de Deus (2002)" --diretor "Fernando Meirelles e Kátia Lund"

# Etapa 2.1 — proposta de perguntas
fluxo gerar 2.1 --titulo "Cidade de Deus (2002)"

# Etapa 2.2 — cole aqui a pergunta escolhida
fluxo gerar 2.2 --pergunta "Como a montagem acelerada transforma a violência em espetáculo...?"

# Etapa 2.3 (opcional) — close reading de uma sequência
fluxo gerar 2.3 --titulo "Cidade de Deus (2002)" --sequencia "A abertura: perseguição ao frango (≈0:00–3:30)"

# Etapa 3 — síntese final, já copiada para a área de transferência
fluxo gerar 3 --titulo "Cidade de Deus (2002)" --copiar

# Comparativa (variante) — duas obras sob um eixo; --modo calibra o tom
fluxo gerar 4 --obra-a "Cidade de Deus (2002)" --diretor-a "Fernando Meirelles e Kátia Lund" \
  --obra-b "Tropa de Elite (2007)" --diretor-b "José Padilha" \
  --eixo "Duas visões da violência urbana brasileira" --modo iniciante
```

Sem instalar, direto da raiz do repo: `PYTHONPATH=src python -m fluxo listar`.

**Atalho:** crie de uma vez a pasta da análise com os prompts de todas as
etapas, o Prompt Maestro, um manifesto `sessao.json`, um dossiê de fontes e
um registro para suas anotações:

```bash
fluxo novo --titulo "Cidade de Deus (2002)" --diretor "Fernando Meirelles e Kátia Lund"
# cria analises/cidade-de-deus-2002/ com todos os prompts e um registro.md
```

**Sem decorar flags?** Rode `fluxo interativo` e responda às perguntas no
terminal — ele pergunta só o que cada etapa precisa e monta os prompts para
você.

### Comandos da CLI

| Comando | Descrição |
| ------- | --------- |
| `fluxo listar` | Lista as etapas e os dados que cada uma requer |
| `fluxo gerar <etapa>` | Gera o prompt da etapa (`0`, `r`, `1`, `1a`, `1b`, `1s`, `2.1`, `2.2`, `2.3`, `3`, `4`). Flags: `--titulo`, `--diretor`, `--tipo`, `--objetivo`, `--nivel`, `--impressoes`, `--pergunta`, `--sequencia`, `--obra-a`/`--diretor-a`/`--obra-b`/`--diretor-b`/`--eixo` (comparativa), `--dossie`/`--dossie-arquivo`, `--modo` (`padrao`/`iniciante`/`academico`), `--salvar arquivo`, `--copiar` |
| `fluxo sessao` | Cria só a trilha escolhida (`padrao`, `dois-tempos`, `serie`, `comparativa`), já preparada para importar respostas; inclui Prompt Maestro, `sessao.json` e dossiê |
| `fluxo maestro` | Gera um prompt único que conduz todas as etapas em uma conversa, parando para você escolher a pergunta da 2.1 e a sequência da 2.3 |
| `fluxo novo --titulo "..."` | Cria `analises/<slug>/` com os prompts de **todas as etapas**, Prompt Maestro, manifesto, dossiê e um `registro.md`. Aceita as mesmas flags do `gerar`, mais `--slug`, `--destino`, `--forcar` |
| `fluxo interativo` | Modo guiado: responde às perguntas no terminal e monta os prompts etapa por etapa (sem decorar flags) |
| `fluxo --versao` | Mostra a versão |

---

## Exemplo

Em [`exemplos/cidade-de-deus/`](exemplos/cidade-de-deus) você encontra o fluxo
completo já preenchido para **Cidade de Deus (2002)** — os prompts das 11
etapas prontos para colar, o Prompt Maestro, o dossiê de fontes, o manifesto
da sessão, um exemplo de perguntas que a Etapa 2.1 costuma gerar e o registro
da análise.

---

## Estrutura do repositório

```
fluxo/
├── README.md / README.en.md       # Este guia (PT-BR / English)
├── index.html + assets/           # 🌐 Interface web (lê os templates de prompts/)
├── docs/
│   └── fluxo.md                   # Guia completo do fluxo
├── prompts/                       # ★ Os templates das etapas (fonte da verdade)
│   ├── etapa-00-preparacao.md
│   ├── etapa-00r-pesquisa-fontes.md
│   ├── etapa-01-analise-360.md
│   ├── etapa-01a-analise-texto.md
│   ├── etapa-01b-analise-contexto.md
│   ├── etapa-01s-analise-serie.md
│   ├── etapa-02.1-proposta-aprofundamento.md
│   ├── etapa-02.2-analise-focada.md
│   ├── etapa-02.3-close-reading.md
│   ├── etapa-03-sintese-conexoes.md
│   └── etapa-04-comparativa.md
├── templates/
│   └── registro-de-analise.md     # Modelo para registrar os achados
├── exemplos/
│   └── cidade-de-deus/            # Exemplo preenchido, ponta a ponta
├── src/fluxo/                     # CLI em Python (sem dependências)
│   ├── core.py                    # Leitura dos templates e preenchimento
│   ├── cli.py                     # Comandos listar / gerar / novo / interativo
│   └── _templates/                # Cópias empacotadas dos templates (fallback p/ pip)
├── scripts/
│   └── sincronizar_templates.py   # Atualiza _templates/ a partir de prompts/
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
- [x] **Fase 2 — UI web**: página estática para montar e copiar os prompts sem terminal
- [x] **Fase 3 — Estrutura**: Etapa 0 (setup + sua hipótese), Etapa 1 em dois tempos, close reading (2.3)
- [x] **Fase 4 — Variantes e base**: séries (1S), comparativa (Etapa 4),
  modos iniciante × acadêmico, CLI interativa e empacotamento dos
  prompts — **v1.0.0** 🎉
- [x] **Fase 5 — Sessão guiada**: Etapa R (fontes), busca gratuita de
  metadados, jornada por trilhas, Prompt Maestro, importação de respostas,
  continuidade entre conversas e executores opcionais sem chave do projeto
  — **v1.1.0**

Ideias para mais adiante: tradução dos prompts (EN/ES), mais fontes públicas
de metadados e exportações editoriais da análise.

## Contribuindo

Sugestões de melhoria nos prompts são muito bem-vindas — veja
[CONTRIBUTING.md](CONTRIBUTING.md).

## Licença

[MIT](LICENSE) © Lucas Rangel — use, adapte e compartilhe à vontade. Bons filmes! 🍿


[MIT](LICENSE) © Lucas Rangel — use, adapte e compartilhe à vontade. Bons filmes! 🍿
