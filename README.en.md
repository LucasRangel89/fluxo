# Fluxo 🎬 — AI-Assisted Analysis of Films & Series

> 🇧🇷 [Leia em português](README.md)

![MIT License](https://img.shields.io/badge/license-MIT-blue)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)
![Version](https://img.shields.io/badge/version-0.1.0-green)

A **specialized 3-stage prompt flow** for dissecting films and series with the
help of an AI (Claude, ChatGPT, Gemini, etc.) across their narrative,
technical, artistic and cultural layers. Instead of a generic summary, the
flow drives a progressive analysis: **map → deepen → synthesize**.

> **Note:** the prompt templates themselves are written in Brazilian
> Portuguese (they work great as-is with any LLM). English translations are on
> the roadmap — contributions welcome!

---

## The 3-stage flow

| Stage | What it does | Template | Command |
| ----- | ------------ | -------- | ------- |
| **1 · 360° Audiovisual Analysis** | An "X-ray" of the work across **7 dimensions**: production context, narrative, image, sound, editing, sociocultural representation, and reception/legacy | [`etapa-01`](prompts/etapa-01-analise-360.md) | `fluxo gerar 1` |
| **2.1 · Deep-Dive Proposal** | Based on Stage 1's map, the AI proposes **3–5 analytical questions** — you pick one | [`etapa-02.1`](prompts/etapa-02.1-proposta-aprofundamento.md) | `fluxo gerar 2.1` |
| **2.2 · Focused Analysis** | A deep dive into the chosen question: **thesis → evidence → analysis → context** | [`etapa-02.2`](prompts/etapa-02.2-analise-focada.md) | `fluxo gerar 2.2` |
| **3 · Synthesis & Connections** | Consolidates the insights and suggests **works in dialogue**, reflection questions, and **essential sources** (criticism, film theory, behind the scenes) | [`etapa-03`](prompts/etapa-03-sintese-conexoes.md) | `fluxo gerar 3` |

> 📖 **Full guide (PT-BR):** [docs/fluxo.md](docs/fluxo.md) — the logic behind
> each stage, the 7 dimensions explained, adaptations for series and
> documentaries, best practices, limitations, and a glossary.

**Golden rule:** run all stages **in the same conversation, in order**. Each
prompt builds on what the AI said before.

---

## Quick start

### Option A — copy & paste (no installation)

1. Open [`prompts/etapa-01-analise-360.md`](prompts/etapa-01-analise-360.md);
2. Copy the text between the `<!-- INICIO DO PROMPT -->` and
   `<!-- FIM DO PROMPT -->` markers;
3. Replace the `{{TITULO_DA_OBRA}}` (title) and `{{DIRETOR_OU_CRIADOR}}`
   (director/creator) placeholders and paste it into your favorite AI;
4. Continue in the **same conversation** with stages 2.1, 2.2 and 3.

### Option B — CLI (Python 3.9+, zero dependencies)

```bash
# (on externally-managed Pythons — PEP 668 error — create a virtualenv first:
#  python -m venv .venv && source .venv/bin/activate)
pip install -e .

fluxo listar                       # list the stages and their requirements
fluxo gerar 1 --titulo "City of God (2002)" --diretor "Fernando Meirelles and Kátia Lund"
fluxo gerar 2.1 --titulo "City of God (2002)"
fluxo gerar 2.2 --pergunta "How does the frenetic editing turn violence into spectacle...?"
fluxo gerar 3 --titulo "City of God (2002)" --copiar   # --copiar: copy to clipboard

# Or scaffold a whole analysis folder (4 prompts + a notes file):
fluxo novo --titulo "City of God (2002)" --diretor "Fernando Meirelles and Kátia Lund"
```

No install needed — from the repo root you can also run
`PYTHONPATH=src python -m fluxo listar`.

| Command | Description |
| ------- | ----------- |
| `fluxo listar` | Lists the stages and what each one requires |
| `fluxo gerar <stage>` | Generates a stage prompt (`1`, `2.1`, `2.2`, `3`). Flags: `--titulo`, `--diretor`, `--pergunta`, `--salvar file`, `--copiar` |
| `fluxo novo --titulo "..."` | Creates `analises/<slug>/` with the 4 filled prompts plus a `registro.md` notes file |
| `fluxo --versao` | Prints the version |

---

## Example

[`exemplos/cidade-de-deus/`](exemplos/cidade-de-deus) contains the complete
flow filled in for **City of God (2002)**: the 4 ready-to-paste prompts, an
illustrative set of Stage 2.1 questions, and the analysis record.

## Repository structure

```
fluxo/
├── README.md / README.en.md       # This guide (PT-BR / English)
├── docs/fluxo.md                  # Full guide to the flow (PT-BR)
├── prompts/                       # ★ The stage templates (single source of truth)
├── templates/registro-de-analise.md
├── exemplos/cidade-de-deus/       # Worked example, end to end
├── src/fluxo/                     # Python CLI (no dependencies)
└── tests/                         # Automated tests (unittest)
```

## Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Roadmap ideas

- [ ] English/Spanish translations of the prompt templates
- [ ] Prompt variants per work type (documentary, animation, shorts)
- [ ] Bundle the prompts with the package so the CLI works from any folder
- [ ] Interactive CLI mode (guided questions in the terminal)
- [ ] Optional LLM-API integration to run the whole flow end to end

## Contributing

Prompt improvements are very welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © Lucas Rangel — use, adapt and share freely. Happy watching! 🍿
