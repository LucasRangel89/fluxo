# Exemplo completo — Cidade de Deus (2002)

Este diretório mostra o **fluxo ponta a ponta já preenchido** para uma obra
real. Serve como referência de como os prompts ficam prontos para colar na IA
e de como a conversa evolui entre as etapas.

**A obra:** *Cidade de Deus* (2002), drama brasileiro dirigido por
**Fernando Meirelles** (codireção de **Kátia Lund**), baseado no romance
homônimo de Paulo Lins. O filme acompanha duas décadas da favela Cidade de
Deus, no Rio de Janeiro, pelos olhos de Buscapé — e foi indicado a **quatro
Oscars**, incluindo Melhor Direção e Melhor Fotografia. É uma obra ideal para
o fluxo: rica em **todas** as 7 dimensões da Etapa 1, da montagem frenética ao
comentário social.

---

## Arquivos deste exemplo

| Arquivo | Etapa | Conteúdo |
| ------- | ----- | -------- |
| [`00-prompt-preparacao.md`](00-prompt-preparacao.md) | 0 | Preparação: a hipótese inicial, registrada antes da análise |
| [`01-prompt-analise-360.md`](01-prompt-analise-360.md) | 1 | Prompt da Análise 360°, pronto para colar |
| [`01a-prompt-analise-360-texto.md`](01a-prompt-analise-360-texto.md) | 1A | Alternativa à Etapa 1 — 1º tempo: o texto (dimensões 2–5) |
| [`01b-prompt-analise-360-contexto.md`](01b-prompt-analise-360-contexto.md) | 1B | Alternativa à Etapa 1 — 2º tempo: o contexto (dimensões 1, 6 e 7) |
| [`01s-prompt-analise-360-serie.md`](01s-prompt-analise-360-serie.md) | 1S | Variante seriada da Etapa 1 (incluída como referência — pense nela para séries, não para este filme) |
| [`02.1-prompt-proposta-aprofundamento.md`](02.1-prompt-proposta-aprofundamento.md) | 2.1 | Prompt pedindo as perguntas de aprofundamento |
| [`02.2-prompt-analise-focada.md`](02.2-prompt-analise-focada.md) | 2.2 | Prompt da análise focada, com a pergunta escolhida (abaixo) |
| [`02.3-prompt-close-reading.md`](02.3-prompt-close-reading.md) | 2.3 | Close reading da sequência de abertura (opcional) |
| [`03-prompt-sintese-conexoes.md`](03-prompt-sintese-conexoes.md) | 3 | Prompt de síntese e conexões |
| [`04-prompt-comparativa.md`](04-prompt-comparativa.md) | 4 | Comparativa Cidade de Deus × Tropa de Elite: duas visões da violência urbana brasileira |
| [`registro.md`](registro.md) | — | Modelo para registrar os achados da análise |

> ⚠️ Cole os prompts **na ordem, na mesma conversa** com a IA.

---

## A Etapa 2.1 na prática

Depois da Análise 360°, a IA propõe as perguntas de aprofundamento. Para
*Cidade de Deus*, uma lista típica seria algo como *(ilustrativo)*:

1. ⭐ **De que forma a montagem acelerada e fragmentada, combinada à narração
   em off de Buscapé, transforma a violência em espetáculo — e como o filme
   lida com a tensão ética entre estetizar essa violência e, ao mesmo tempo,
   criticá-la?**
   *É o debate central sobre o filme desde o lançamento: a forma virtuosística
   reforça ou enfraquece a denúncia?*
2. Como a evolução da paleta de cores e da fotografia — do dourado nostálgico
   dos anos 1960/70 ao tom cru e saturado dos anos 1980 — visualiza a
   degradação da favela e a perda da infância de seus moradores?
3. Em que medida a estrutura em capítulos e os flashbacks circulares (a
   história do apartamento, o retorno à cena do frango no desfecho) constroem
   a sensação de um ciclo de violência sem saída?
4. Como o filme representa o Estado e a polícia — quase sempre ausentes ou
   corruptos — e o que essa ausência revela da sua crítica social?
5. Qual é o papel da fotografia, o ofício de Buscapé, como metáfora: a câmera
   como única "arma" capaz de romper o ciclo — mas também como instrumento
   ambíguo de denúncia e de exploração midiática da violência?

**Neste exemplo, escolhemos a pergunta nº 1** — é ela que está preenchida em
[`02.2-prompt-analise-focada.md`](02.2-prompt-analise-focada.md). Nada impede
voltar depois e aprofundar as outras, uma de cada vez.

---

## Como este exemplo foi gerado

Todos os arquivos foram criados com um único comando da [CLI](../../README.md):

```bash
fluxo novo \
  --titulo "Cidade de Deus (2002)" \
  --diretor "Fernando Meirelles e Kátia Lund" \
  --tipo "Filme (longa-metragem de ficção)" \
  --objetivo "Estudar a fundo um clássico do cinema brasileiro" \
  --nivel "Intermediário — leio críticas e quero aprofundar a técnica" \
  --impressoes "Na primeira vez que vi, achei a violência espetacularizada demais, quase um videoclipe. Hoje desconfio que a forma acelerada é justamente o tema — mas ainda não sei dizer se o filme critica ou celebra esse mundo." \
  --pergunta "De que forma a montagem acelerada e fragmentada, combinada à narração em off de Buscapé, transforma a violência em espetáculo — e como o filme lida com a tensão ética entre estetizar essa violência e, ao mesmo tempo, criticá-la?" \
  --sequencia "A abertura completa: a faca sendo amolada, a fuga e a perseguição ao frango, até o plano em que Buscapé fica preso entre o bando de Zé Pequeno e a polícia (≈0:00–3:30)" \
  --obra-a "Cidade de Deus (2002)" \
  --diretor-a "Fernando Meirelles e Kátia Lund" \
  --obra-b "Tropa de Elite (2007)" \
  --diretor-b "José Padilha" \
  --eixo "Duas visões da violência urbana brasileira: a favela pelos olhos de quem mora nela (Buscapé, o fotógrafo) × pelos olhos do Estado (Cap. Nascimento, o BOPE) — forma e ética do olhar" \
  --slug cidade-de-deus \
  --destino exemplos
```

## Replique com a sua obra

```bash
fluxo novo --titulo "Sua Obra (Ano)" --diretor "Nome do Diretor(a)"
# → cria analises/sua-obra-ano/ com os prompts de todas as etapas e o registro.md
```

Depois é só: **assistir → colar o prompt da Etapa 1 → seguir o fluxo →
anotar os achados no `registro.md`**. Bom filme! 🎬
