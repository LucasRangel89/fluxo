# Fluxo 🎬 — AI-Assisted Analysis of Films & Series

> 🇧🇷 [Leia em português](README.md)

![MIT License](https://img.shields.io/badge/license-MIT-blue)
![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)
![Version](https://img.shields.io/badge/version-1.0.0-green)

A **specialized 3-stage prompt flow** for dissecting films and series with the
help of an AI (Claude, ChatGPT, Gemini, etc.) across their narrative,
technical, artistic and cultural layers. Instead of a generic summary, the
flow drives a progressive analysis: **map → deepen → synthesize**.

> **Note:** the prompt templates themselves are written in Brazilian
> Portuguese (they work great as-is with any LLM). English translations are on
> the roadmap — contributions welcome!

---

## The flow (three acts, with prep & variants)

| Stage | What it does | Template | Command |
| ----- | ------------ | -------- | ------- |
| **0 · Preparation** *(optional)* | Identifies the work, calibrates your goal/level and **records your own hypothesis before the AI weighs in** — revisited in Stage 3 | [`etapa-00`](prompts/etapa-00-preparacao.md) | `fluxo gerar 0` |
| **1 · 360° Audiovisual Analysis** | An "X-ray" of the work across **7 dimensions**: production context, narrative, image, sound, editing, sociocultural representation, and reception/legacy | [`etapa-01`](prompts/etapa-01-analise-360.md) | `fluxo gerar 1` |
| **1A + 1B · Two-part 360°** *(alternative to Stage 1)* | The same X-ray split in two: **Text** (narrative, image, sound, editing) → **Context** (production, sociocultural, reception), closing with the full 7-dimension summary table | [`etapa-01a`](prompts/etapa-01a-analise-texto.md) · [`etapa-01b`](prompts/etapa-01b-analise-contexto.md) | `fluxo gerar 1a` / `1b` |
| **1S · Series 360°** *(series variant)* | The X-ray designed for seasons: **arcs at 3 levels** (series, season, episode), pilot, cliffhangers, **showrunner**, and release model | [`etapa-01s`](prompts/etapa-01s-analise-serie.md) | `fluxo gerar 1s` |
| **2.1 · Deep-Dive Proposal** | Based on Stage 1's map, the AI proposes **3–5 analytical questions** — you pick one | [`etapa-02.1`](prompts/etapa-02.1-proposta-aprofundamento.md) | `fluxo gerar 2.1` |
| **2.2 · Focused Analysis** | A deep dive into the chosen question: **thesis → evidence → analysis → context** | [`etapa-02.2`](prompts/etapa-02.2-analise-focada.md) | `fluxo gerar 2.2` |
| **2.3 · Close Reading** *(optional)* | **One sequence dissected shot by shot**: breakdown, mise-en-scène, sound, editing, and the meaning built by form | [`etapa-02.3`](prompts/etapa-02.3-close-reading.md) | `fluxo gerar 2.3` |
| **3 · Synthesis & Connections** | Consolidates the insights, judges the work (critical balance), suggests **works in dialogue**, reflection questions — including the **before/after of your own reading** — and **essential sources** | [`etapa-03`](prompts/etapa-03-sintese-conexoes.md) | `fluxo gerar 3` |
| **4 · Comparative** *(variant)* | **Two works head-to-head** under one axis (remake, same director, same theme): card profiles, paired comparison, criteria-based verdict, and a **summary table** | [`etapa-04`](prompts/etapa-04-comparativa.md) | `fluxo gerar 4` |

> 📖 **Full guide (PT-BR):** [docs/fluxo.md](docs/fluxo.md) — the logic behind
> each stage, the 7 dimensions explained, adaptations for series and
> documentaries, best practices, limitations, and a glossary.

**Golden rule:** run all stages **in the same conversation, in order**. Each
prompt builds on what the AI said before.

---

## Quick start

### Option A — Web UI (recommended) 🌐

The easiest way to use Fluxo: fill in the title and director, pick a stage and
copy the ready-made prompt — no terminal, no placeholder hunting. It remembers
your inputs in the browser, marks stages you've already copied and can
download each prompt as `.md`.

- **Run locally:** from the repo root, `python -m http.server 8000`, then open
  `http://localhost:8000` (HTTP is required: the page reads the templates from
  `prompts/` at runtime — the same source the CLI uses, no duplication).
- **GitHub Pages:** *Settings → Pages → Deploy from a branch → `main`,
  `/ (root)`*. The included `.nojekyll` file makes sure the templates are
  served as-is.

### Option B — copy & paste (no installation)

1. Open [`prompts/etapa-01-analise-360.md`](prompts/etapa-01-analise-360.md);
2. Copy the text between the `<!-- INICIO DO PROMPT -->` and
   `<!-- FIM DO PROMPT -->` markers;
3. Replace the `{{TITULO_DA_OBRA}}` (title) and `{{DIRETOR_OU_CRIADOR}}`
   (director/creator) placeholders and paste it into your favorite AI;
4. Continue in the **same conversation** with stages 2.1, 2.2 and 3.

### Option C — CLI (Python 3.9+, zero dependencies)

```bash
# (on externally-managed Pythons — PEP 668 error — create a virtualenv first:
#  python -m venv .venv && source .venv/bin/activate)
pip install -e .

fluxo listar                       # list the stages and their requirements
fluxo gerar 0 --titulo "City of God (2002)" --diretor "Fernando Meirelles and Kátia Lund" --tipo "Feature film" --objetivo "Study a classic" --nivel "Intermediate" --impressoes "First take: the violence felt overly aestheticized."   # optional prep
fluxo gerar 1 --titulo "City of God (2002)" --diretor "Fernando Meirelles and Kátia Lund"   # or in two parts: 1a, then 1b
fluxo gerar 2.1 --titulo "City of God (2002)"
fluxo gerar 2.2 --pergunta "How does the frenetic editing turn violence into spectacle...?"
fluxo gerar 2.3 --titulo "City of God (2002)" --sequencia "The opening: the chicken chase (≈0:00–3:30)"   # optional close reading
fluxo gerar 3 --titulo "City of God (2002)" --copiar   # --copiar: copy to clipboard
fluxo gerar 4 --obra-a "City of God (2002)" --diretor-a "Fernando Meirelles and Kátia Lund" --obra-b "Elite Squad (2007)" --diretor-b "José Padilha" --eixo "Two views of Brazilian urban violence"   # comparative variant; add --modo iniciante|academico to calibrate the register
fluxo interativo   # guided mode: answer questions, get prompts (no flags to memorize)

# Or scaffold a whole analysis folder (all 10 stage prompts + a notes file):
fluxo novo --titulo "City of God (2002)" --diretor "Fernando Meirelles and Kátia Lund"
```

No install needed — from the repo root you can also run
`PYTHONPATH=src python -m fluxo listar`.

| Command | Description |
| ------- | ----------- |
| `fluxo listar` | Lists the stages and what each one requires |
| `fluxo gerar <stage>` | Generates a stage prompt (`0`, `1`, `1a`, `1b`, `1s`, `2.1`, `2.2`, `2.3`, `3`, `4`). Flags: `--titulo`, `--diretor`, `--tipo`, `--objetivo`, `--nivel`, `--impressoes`, `--pergunta`, `--sequencia`, `--obra-a`/`--diretor-a`/`--obra-b`/`--diretor-b`/`--eixo` (comparative), `--modo` (`padrao`/`iniciante`/`academico`), `--salvar file`, `--copiar` |
| `fluxo novo --titulo "..."` | Creates `analises/<slug>/` with **every stage's** prompt plus a `registro.md` notes file |
| `fluxo interativo` | Guided mode: answer questions in the terminal and build prompts stage by stage (no flags to memorize) |
| `fluxo --versao` | Prints the version |

---

## Example

[`exemplos/cidade-de-deus/`](exemplos/cidade-de-deus) contains the complete
flow filled in for **City of God (2002)**: all 10 prompts ready to paste, an
illustrative set of Stage 2.1 questions, and the analysis record.

## Repository structure

```
fluxo/
├── README.md / README.en.md       # This guide (PT-BR / English)
├── index.html + assets/           # 🌐 Web UI (reads the templates from prompts/)
├── docs/fluxo.md                  # Full guide to the flow (PT-BR)
├── prompts/                       # ★ The stage templates (single source of truth)
├── templates/registro-de-analise.md
├── exemplos/cidade-de-deus/       # Worked example, end to end
├── src/fluxo/                     # Python CLI (no dependencies; templates bundled as fallback)
├── scripts/sincronizar_templates.py  # Refreshes the bundled template copies
└── tests/                         # Automated tests (unittest)
```

## Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Roadmap (phased plan)

The project is evolving in phases, based on a
[critical analysis](docs/analise-critica.md) of the flow itself (in PT-BR):

- [x] **Phase 1 — Prompts v2**: critic persona and anti-hallucination rules,
  structured output format, built-in counterargument in Stage 2.2, new theory
  sub-items (performance, authorship, genre, spectator)
- [x] **Phase 2 — Web UI**: static page to build and copy prompts without a terminal
- [x] **Phase 3 — Structure**: Stage 0 (setup + your own hypothesis), two-part
  Stage 1, close-reading stage (2.3)
- [x] **Phase 4 — Variants & plumbing**: series variant (1S), comparative
  analysis (Stage 4), beginner × academic modes, interactive CLI, bundled
  prompts — **v1.0.0** 🎉

Later ideas: EN/ES prompt translations and optional LLM-API integration.

## Contributing

Prompt improvements are very welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE) © Lucas Rangel — use, adapt and share freely. Happy watching! 🍿
