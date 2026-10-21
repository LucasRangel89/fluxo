# Changelog

Todas as mudanças relevantes deste projeto serão documentadas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.1.0] — 2026-10-20

### Adicionado

- **Templates do fluxo** em `prompts/`:
  - Etapa 1 — Análise Audiovisual 360° (7 dimensões críticas);
  - Etapa 2.1 — Proposta de Aprofundamento Crítico (3 a 5 perguntas analíticas);
  - Etapa 2.2 — Execução da Análise Focada (tese, evidências, análise, contexto);
  - Etapa 3 — Consolidação, Diálogos e Expansão.
- **CLI `fluxo`** em Python (sem dependências), com os comandos:
  - `listar` — mostra as etapas e seus requisitos;
  - `gerar` — preenche os placeholders e entrega o prompt pronto
    (com `--salvar` e `--copiar`);
  - `novo` — cria a pasta de uma análise com os 4 prompts e um `registro.md`.
- **Template de registro** de análise em `templates/registro-de-analise.md`.
- **Guia completo** do fluxo em `docs/fluxo.md` (lógica das etapas, as 7
  dimensões, adaptações, boas práticas, glossário e FAQ).
- **Exemplo ponta a ponta** com *Cidade de Deus (2002)* em `exemplos/`.
- README em português e inglês, testes automatizados e licença MIT.
