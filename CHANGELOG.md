# Changelog

Todas as mudanças relevantes deste projeto serão documentadas aqui.
O formato segue o [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e o projeto adota [Versionamento Semântico](https://semver.org/lang/pt-BR/).

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
