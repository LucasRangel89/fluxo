# Changelog

Todas as mudanças relevantes deste projeto serão documentadas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.1.0] — 2026-10-21

### Adicionado
- **Fase 5 — sessão guiada e acessibilidade sem backend:**
  - **Etapa R · Pesquisa e Dossiê de Fontes** (`etapa r`): fato antes da
    interpretação, com identidade da obra, ficha, produção, recepção,
    controvérsias, incertezas e fontes nomeadas;
  - **Trilhas de sessão** (`padrao`, `dois-tempos`, `serie`, `comparativa`)
    compartilhadas por CLI e web, com dependências e próxima ação;
  - **Prompt Maestro** (`fluxo maestro`): um único prompt conduz a análise
    inteira em uma conversa, parando para a escolha da Etapa 2.1 e para a
    sequência opcional da 2.3;
  - comando **`fluxo sessao`**, que gera apenas a trilha escolhida, o
    Prompt Maestro, o manifesto `sessao.json` e o dossiê editável;
  - marcadores opcionais de resposta para a sessão guiada (`RESUMO:`,
    `PERGUNTA:`, `SEQUENCIA_SUGERIDA:` e `FONTE:`) e parsers para importar
    respostas, selecionar perguntas/sequências e montar continuidade;
  - busca de metadados sem chave na web via **Wikipedia/Wikidata** e
    **TVMaze**, com confirmação manual, atribuição e URLs no dossiê;
  - executores opcionais, sem chave do projeto: sua IA externa por
    copiar/abrir, **Puter** com a conta do usuário, **BYOK** compatível
    com OpenAI e IA local do Chrome via `LanguageModel`, quando disponível;
  - exportação/importação da sessão web em Markdown e JSON;
  - flags `--dossie` e `--dossie-arquivo`; `fluxo novo` agora inclui
    Etapa R, Prompt Maestro, manifesto e dossiê no kit completo;
  - exemplo *Cidade de Deus* regenerado com os novos arquivos e testes
    dedicados da Fase 5.

### Corrigido
- A inferência de trilha da CLI não classifica um kit como comparativo
  apenas porque ele também contém obras A/B quando há uma obra principal.

## [1.0.0] — 2026-10-21

### Adicionado
- **Fase 4 do plano — variantes e base técnica (fecha o plano faseado):**
  - **Etapa 1S · Análise 360° de Série/Temporada**
    (`prompts/etapa-01s-analise-serie.md`): as 7 dimensões traduzidas para a
    lógica seriada — arcos em 3 níveis (série, temporada, episódio), piloto
    e *finale*, cliffhangers, showrunner, modelo de exibição (semanal ×
    maratona) e episódio-síntese;
  - **Etapa 4 · Análise Comparativa** (`prompts/etapa-04-comparativa.md`):
    duas obras frente a frente sob um eixo — cartões, terreno comum,
    comparação dimensão a dimensão em pares, diálogo entre elas, juízo por
    critérios e tabela comparativa;
  - **Modos de análise** (`--modo padrao|iniciante|academico`, seletor na
    interface web): calibrados nas etapas de abertura (1, 1A, 1S e 4) pelo
    novo placeholder opcional `{{MODO_DE_ANALISE}}` — nunca conta como
    pendente e não deixa buracos no texto;
  - **CLI interativa** (`fluxo interativo`): perguntas no terminal, pede só
    o que cada etapa precisa e oferece copiar/salvar o prompt;
  - **Templates empacotados**: cópias em `src/fluxo/_templates/`
    (sincronizadas por `scripts/sincronizar_templates.py` e verificadas por
    testes) permitem usar a CLI instalada via pip, fora do repositório.
- CLI: etapas `1s` e `4` (com aliases como `serie`, `temporada` e
  `comparativa`), flags `--obra-a`, `--diretor-a`, `--obra-b`,
  `--diretor-b`, `--eixo` e `--modo`; o comando `novo` gera os 10 prompts.
- Interface web: 10 etapas no stepper, campos da comparativa e seletor de
  modo; o exemplo embutido também preenche a comparativa (Cidade de Deus ×
  Tropa de Elite).
- Exemplo regenerado com os 10 prompts preenchidos, incluindo a
  comparativa; guia `docs/fluxo.md` com a variante 1S, a Etapa 4, novos
  termos no glossário e FAQ sobre modos.

## [0.4.0] — 2026-10-20

### Adicionado
- **Fase 3 do plano — estrutura do fluxo:**
  - **Etapa 0 · Preparação** (`prompts/etapa-00-preparacao.md`): identifica a
    obra sem ambiguidade, calibra tipo/objetivo/nível e **registra as
    impressões e a hipótese do usuário antes de a IA opinar** (contra a
    ancoragem), com pontos de atenção para assistir/reassistir;
  - **Etapas 1A/1B** — a Análise 360° em dois tempos, como alternativa à
    Etapa 1: **1A Texto** (dimensões 2–5) → **1B Contexto** (1, 6 e 7),
    conectando o contexto aos achados formais e fechando com a tabela-resumo
    completa das 7 dimensões;
  - **Etapa 2.3 · Close Reading** (opcional): uma sequência dissecada plano a
    plano — decupagem, mise-en-scène e som, ritmo interno e sentido;
  - A Etapa 3 agora **revisita a hipótese inicial** registrada na Etapa 0
    (o que se confirmou, o que caiu por terra), e a ficha-resumo registra o
    antes/depois da leitura.
- CLI: novas etapas `0`, `1a`, `1b` e `2.3` (com aliases como `setup`,
  `texto`, `contexto`, `close`) e flags `--tipo`, `--objetivo`, `--nivel`,
  `--impressoes` e `--sequencia`; o comando `novo` gera os 8 prompts.
- Interface web: 8 etapas no stepper e **campos dinâmicos por etapa**
  (derivados dos placeholders do próprio template); o exemplo embutido cobre
  todos os campos e a etapa inicial passa a ser a 0 (Preparação).
- Template de registro com seção da Etapa 0 (hipótese e pontos de atenção),
  subitens novos nas dimensões, bloco de close reading e o confronto
  "minha leitura inicial mudou?".
- Exemplo *Cidade de Deus* regenerado com as 8 etapas — incluindo a hipótese
  inicial e a sequência de abertura para o close reading.
- Testes da Fase 3 (`tests/test_fase3.py`) e cobertura web estendida a todos
  os placeholders.

### Corrigido
- Placeholder da Etapa 0 definido como `{{META_DA_ANALISE}}`, dentro do
  padrão `{{MAIUSCULAS_COM_UNDERSCORE}}` que o motor reconhece.

## [0.3.0] — 2026-10-20

### Adicionado
- **Fase 2 do plano — Interface web estática** (`index.html` + `assets/`):
  - Stepper das 4 etapas com formulário (título, diretor, pergunta) e prompt
    gerado ao vivo, editável antes de copiar;
  - Botões **Copiar** e **Baixar .md**, aviso de campos pendentes, contador de
    caracteres e marcação (✓) das etapas já copiadas;
  - Lê os templates direto de `prompts/` via fetch — mesma fonte da CLI, sem
    duplicação — e lembra os dados no navegador (localStorage);
  - Exemplo embutido (*Cidade de Deus*), tema escuro "sala de cinema" e layout
    responsivo para celular.
- Arquivo `.nojekyll` para publicar no GitHub Pages servindo tudo como está.
- `tests/test_web.py`: testes de integração garantindo que a UI usa os mesmos
  templates, marcadores, placeholders e versão da CLI.

### Corrigido
- Restauradas edições da Fase 1 que não haviam persistido no guia
  `docs/fluxo.md` (tabela das 7 dimensões com os novos subitens, estrutura da
  Etapa 2.2 com contra-argumento, boas práticas) e os badges de versão dos
  READMEs.

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
