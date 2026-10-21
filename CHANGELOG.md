# Changelog

Todas as mudanças relevantes deste projeto serão documentadas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [0.2.0] — 2026-10-20

### Adicionado
- `docs/analise-critica.md`: avaliação crítica de teoria e técnica do fluxo,
  backlog de propostas (P1–P17), decisões registradas e plano faseado.
- **Fase 1 do plano — prompts v2:**
  - Persona de crítico/professor e regras de rigor anti-alucinação
    (marcar "(a confirmar)", separar fato de interpretação, desambiguar
    obras homônimas/remakes);
  - Formato de saída estruturado: cabeçalhos por dimensão e tabela-resumo
    na Etapa 1; evidências com minutagem/episódio nas Etapas 1 e 2.2;
  - Novos subitens teóricos, mantendo as 7 dimensões: atuação e elenco,
    gênero e convenções, autoria, focalização, posição do espectador e
    modelo de produção/streaming; neutralização do viés de estrutura
    clássica (comprovação de rótulos, estruturas não-ocidentais);
  - Etapa 2.1 com diversidade obrigatória de tipos de pergunta e espaço
    para pergunta do próprio usuário;
  - Etapa 2.2 com passo de contra-argumento e falsificabilidade;
  - Etapa 3 com **Balanço Crítico** (julgamento fundamentado),
    **Ficha-Resumo** salvável e regra de só citar fontes confiáveis.
- Exemplo `exemplos/cidade-de-deus` regenerado com os prompts v2.
- Testes cobrindo as características v2 dos prompts.

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
