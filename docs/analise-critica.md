# Análise Crítica do Fluxo — Documento de Discussão e Plano

> **objetivo:** registrar uma avaliação crítica da **teoria** (fundamentação em
> estudos de cinema) e da **técnica** (engenharia de prompt + base técnica) do
> Fluxo, e servir como backlog de decisões. Cada proposta tem um ID; as
> decisões tomadas estão na [seção 5](#5-decisões-registradas) e o plano de
> execução na [seção 6](#6-plano-faseado-decidido).
>
> **Status:** Fases 1 (prompts v2), 2 (UI web) e 3 (estrutura) implementadas
> em 2026-10-20; Fase 4 planejada.

---

## 1. Resumo executivo

O Fluxo tem um método sólido — mapear (Etapa 1) → aprofundar com agência do
usuário (Etapas 2.1/2.2) → sintetizar e conectar (Etapa 3) — e uma base
técnica limpa (templates Markdown como fonte única + CLI sem dependências).
Os principais riscos identificados foram: **(a)** alucinação factual da IA sem
nenhuma blindagem nos prompts; **(b)** lacunas teóricas (atuação, autoria,
gênero, especificidade das séries); **(c)** uma Etapa 1 monolítica que tende
ao checklist superficial; e **(d)** uma barreira de adoção — sem interface, o
público natural do projeto (cinéfilos, estudantes, professores) não chega ao
conteúdo. Os itens (a) e (d) foram tratados nas Fases 1 e 2; (b) e (c)
avançaram nas Fases 1 e 3. O que falta está concentrado na Fase 4 (variantes
por tipo de obra e base técnica).

---

## 2. Pontos fortes

### Teoria
- Método em funil (descrever → analisar → sintetizar/avaliar), alinhado ao
  método acadêmico e à progressão cognitiva.
- As 7 dimensões dialogam com as categorias canônicas de Bordwell & Thompson
  (*Film Art*) e somam produção + recepção: forma, conteúdo e contexto.
- Etapa 2.1 como diferencial: a IA propõe perguntas, o usuário escolhe —
  coautoria em vez de consumo passivo.
- Etapa 2.2 com estrutura argumentativa (tese → evidências → análise),
  padrão da boa crítica.
- Etapa 3 promove transferência: obras em diálogo, teoria, bastidores e
  reflexão pessoal.

### Técnica
- Prompts estruturados (listas, âncoras em negrito) e exemplos inline que
  elevam o registro técnico das respostas.
- Bom uso do contexto conversacional entre etapas; placeholders mínimos.
- Instrução "rica em exemplos de cenas" combate respostas genéricas.
- Base: fonte única em Markdown, CLI fina e testada, zero dependências.

## 3. Pontos fracos e lacunas

### Teoria
1. **Dimensões submersas/ausentes:** atuação e performance (diluídas na
   mise-en-scène), *star persona*, gênero e suas convenções, autoria como
   lente (auteur × indústria; showrunner na TV), espectatorialidade
   (identificação, olhar), narratologia fina (focalização, narrador
   não-confiável), economia do streaming/franquias, tecnologia do meio
   (formato, VFX). → *Tratado em grande parte por P10 (Fase 1).*
2. **Viés clássico-narrativo:** exemplos (jornada do herói, três atos) podem
   forçar obras não-clássicas (cinema lento, experimental, kishōtenketsu,
   antologias) em moldes inadequados. → *Tratado por P11 (Fase 1).*
3. **Séries como "filmes longos":** faltam serialidade, arco de
   episódio/temporada/série, piloto, cliffhanger, maratona × semanal,
   "TV complexa" (Mittell). → *P12 (Fase 4).*
4. **Sem momento avaliativo:** descreve e interpreta, mas não julga com
   critérios ("funciona? nos seus próprios termos?").
   → *Tratado por P9 (Fase 1: Balanço Crítico na Etapa 3).*
5. **Ancoragem:** o usuário só entra na Etapa 2.1; suas impressões iniciais
   nunca são registradas antes do enquadramento da IA.
   → *Tratado por P4 (Fase 3: Etapa 0 registra a hipótese; a Etapa 3 a revisita).*
6. **Sem modo comparativo** (duas obras) nem entrada "testar minha tese".
   → *P13 (Fase 4); a pergunta própria já é aceita na 2.1 desde a Fase 1.*

### Técnica
1. **Sem guardrails anti-alucinação:** nada pede sinalizar incerteza, separar
   fato de interpretação ou não inventar cenas/citações — e as Etapas 3
   (fontes) e 1-dimensao-7 (bilheteria/prêmios) são justamente as mais
   factuais. **Maior risco prático do projeto.** → *Tratado por P1/P2 (Fase 1).*
2. **Sem persona e sem desambiguação** (remakes/homônimos).
   → *Tratado por P1/P2 (Fase 1); a desambiguação ganhou também a Etapa 0 (Fase 3).*
3. **Etapa 1 monolítica:** respostas longas rareiam nas dimensões finais;
   risco de truncamento; sem cabeçalhos/orçamento por dimensão, difícil
   referenciar e reler.
   → *Mitigado por P3 (Fase 1) e resolvido estruturalmente por P5 (Fase 3: 1A/1B).*
4. **Priming pelos exemplos:** os "ex.:" podem ancorar rótulos indevidos.
   → *Mitigado por P11 (Fase 1: comprovar rótulos estruturais).*
5. **2.1 autorreferente:** perguntas derivadas do texto da própria IA, sem
   garantia de diversidade (forma × tema × ideologia × recepção).
   → *Tratado por P6 (Fase 1).*
6. **2.2 confirmatória:** sem contra-argumento nem falsificabilidade; sem
   calibragem de evidências (minutagem, T1:E5). → *Tratado por P7/P3 (Fase 1).*
7. **Sem personalização:** nível (iniciante × acadêmico), objetivo (estudo,
   resenha, aula) e profundidade não são variáveis — falta uma Etapa 0.
   → *P4 na Fase 3 (a Etapa 0 captura objetivo/nível e calibra a conversa);
   modos formais em P14 (Fase 4).*
8. **Base técnica:** CLI depende de localizar `prompts/` a partir do repo
   (quebra se instalada e usada em outra pasta); ausência de UI limita a
   adoção pelo público-alvo. → *UI tratada por P15 (Fase 2); P17 na Fase 4.*

---

## 4. Propostas (backlog)

### Grupo A — Blindagem e precisão (prompts)
| ID | Proposta | Impacto | Esforço | Status |
|----|----------|---------|---------|--------|
| P1 | Persona + instruções globais no topo de cada prompt (papel de crítico/professor, registro, "se não souber, diga") | Alto | Baixo | ✅ Fase 1 |
| P2 | Guardrails: sinalizar confiança, separar fato/interpretação, não inventar cenas, citações ou fontes; desambiguar título/ano/diretor | Alto | Baixo | ✅ Fase 1 |
| P3 | Formato de saída: cabeçalhos por dimensão, tabela-resumo na Etapa 1, evidências com minutagem (filme) ou T/E (série), orçamento por seção | Alto | Baixo | ✅ Fase 1 |

### Grupo B — Estrutura do fluxo
| ID | Proposta | Impacto | Esforço | Status |
|----|----------|---------|---------|--------|
| P4 | **Etapa 0 (setup):** tipo de obra, objetivo e nível do usuário + registro das impressões/hipótese iniciais (revisitadas na Etapa 3) | Alto | Médio | ✅ Fase 3 |
| P5 | Etapa 1 em dois tempos (1A: texto — narrativa/imagem/som/montagem; 1B: contexto — produção/sociocultural/recepção) ou módulos de aprofundamento por dimensão | Alto | Médio | ✅ Fase 3 (1A/1B como alternativa à Etapa 1) |
| P6 | 2.1 com diversidade obrigatória (1 pergunta por tipo: forma, tema, ideologia/representação, autoria/comparação, recepção) + espaço oficial para pergunta do usuário | Médio | Baixo | ✅ Fase 1 |
| P7 | 2.2 com contra-argumento ("advogado do diabo") e critério de falsificação da tese | Alto | Baixo | ✅ Fase 1 |
| P8 | Nova etapa opcional **2.3 — Close reading** plano a plano de uma sequência | Médio | Médio | ✅ Fase 3 |
| P9 | Fecho avaliativo na Etapa 3 (julgamento com critérios) + "sua leitura inicial mudou?" | Médio | Baixo | ✅ Fase 1 (balanço crítico) + Fase 3 (revisita à hipótese) |

### Grupo C — Teoria e variantes
| ID | Proposta | Impacto | Esforço | Status |
|----|----------|---------|---------|--------|
| P10 | Explicitar subitens: atuação/performance e gênero (dim. 2/3), autoria (dim. 1/2), espectador/olhar (dim. 6), indústria/streaming (dim. 1/7), focalização (dim. 2) | Alto | Baixo | ✅ Fase 1 |
| P11 | Neutralizar viés clássico: pedir a estrutura real da obra, admitindo modelos não-ocidentais/experimentais; exigir comprovação ao aplicar um rótulo | Médio | Baixo | ✅ Fase 1 |
| P12 | Variante **séries/temporadas**: serialidade, piloto, arcos em 3 níveis, showrunner, modelo de exibição | Alto | Médio | ✅ Fase 4 |
| P13 | Variante **comparativa**: duas obras em diálogo (mesmo diretor, remake, mesmo tema) | Médio | Médio | ✅ Fase 4 |
| P14 | Modos **iniciante × acadêmico** (variável de profundidade/registro nos prompts) | Médio | Médio | ✅ Fase 4 |

### Grupo D — Produto e base técnica
| ID | Proposta | Impacto | Esforço | Status |
|----|----------|---------|---------|--------|
| P15 | **UI web estática** (página única, sem backend): stepper de etapas, formulário, prompt ao vivo, copiar/baixar, lê os templates de `prompts/`, publicável no GitHub Pages | Alto | Médio | ✅ Fase 2 |
| P16 | Modo interativo na CLI (perguntas guiadas no terminal) | Médio | Baixo | ✅ Fase 4 |
| P17 | Empacotar os prompts junto ao pacote Python (CLI funciona instalada de qualquer pasta) | Médio | Baixo | ✅ Fase 4 |

---

## 5. Decisões registradas

| Data | Decisão | Observações |
|------|---------|-------------|
| 2026-10-20 | Interface: **web app estático** (P15), lendo os templates de `prompts/` | Sem backend; publicável no GitHub Pages; CLI permanece como ferramenta complementar |
| 2026-10-20 | Melhorias dos prompts em **plano faseado**, validando cada fase | Ver seção 6 |
| 2026-10-20 | Teoria: **manter as 7 dimensões** e expandir com subitens explícitos (P10/P11) | Sem reformulação do mapa |
| 2026-10-20 | **Fase 1 implementada** (P1, P2, P3, P6, P7, P9 parcial, P10, P11) → prompts v2 | Exemplo regenerado; repo v0.2.0 |
| 2026-10-20 | **Fase 2 implementada**: UI web estática (P15) em `index.html` + `assets/` | Lê `prompts/` via fetch (fonte única); `.nojekyll` p/ GitHub Pages; testes anti-drift (`tests/test_web.py`); repo v0.3.0 |
| 2026-10-20 | **Fase 3 implementada**: Etapa 0, 1A/1B em dois tempos, close reading 2.3 e revisita à hipótese (P4, P5, P8, P9 completo) | 1A/1B como **alternativa** à Etapa 1 (não substituição); UI deriva os campos dos placeholders do template; repo v0.4.0 |
| 2026-10-21 | **Fase 4 implementada**: variantes 1S (séries) e Etapa 4 (comparativa), modos iniciante × acadêmico, CLI interativa e prompts empacotados (P12–P14, P16, P17) | **Plano faseado concluído** (P1–P17); repo v1.0.0 |

## 6. Plano faseado (decidido)

- **Fase 1 — Prompts v2 (só texto, mesma estrutura)** ✅
  Persona e regras de rigor, formato de saída, subitens teóricos,
  diversidade na 2.1, contra-argumento na 2.2, balanço crítico + ficha-resumo
  na Etapa 3.
- **Fase 2 — UI web estática** (P15) ✅
  Antecipada em relação à ordem original (A → B/C → D) para validar a
  experiência de uso mais cedo. A UI é orientada pelos templates de
  `prompts/`, absorvendo as novas etapas das fases seguintes sem retrabalho
  estrutural.
- **Fase 3 — Estrutura do fluxo** (P4, P5, P8, restante de P9) ✅
  Etapa 0 com a hipótese do usuário, Etapa 1 em dois tempos (1A/1B como
  alternativa à Etapa 1 única), close reading 2.3 e a Etapa 3 revisitando a
  hipótese inicial.
- **Fase 4 — Variantes e base técnica** (P12, P13, P14, P16, P17) ✅
  Séries (Etapa 1S), comparativa (Etapa 4), modos de profundidade
  (iniciante × acadêmico), CLI interativa e empacotamento dos prompts no
  pacote Python.

**Plano concluído** 🎬 — todas as propostas P1–P17 foram implementadas e o
projeto alcançou a **v1.0.0**. Ideias futuras registradas no README:
tradução dos prompts (EN/ES) e integração opcional com APIs de LLMs.
