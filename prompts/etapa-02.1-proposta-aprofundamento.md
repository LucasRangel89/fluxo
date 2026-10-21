# Etapa 2.1 — Proposta de Aprofundamento Crítico

> **objetivo:** transformar o mapa da Etapa 1 em um debate crítico. Aqui a IA
> deixa de ser uma "enciclopédia" e passa a atuar como parceira de análise,
> propondo as perguntas mais férteis para dissecar a obra — com diversidade
> garantida de tipos de questão (forma, tema, autoria, recepção).

## Quando usar

**Na mesma conversa** da Etapa 1, logo após receber a análise 360°. O prompt
depende do contexto anterior ("Com base no que foi levantado..."), então não
funciona bem isolado.

## Placeholders

| Placeholder          | O que é                  | Flag na CLI | Exemplo                 |
| -------------------- | ------------------------ | ----------- | ----------------------- |
| `{{TITULO_DA_OBRA}}` | Título do filme ou série | `--titulo`  | `Cidade de Deus (2002)` |

## Prompt

<!-- INICIO DO PROMPT -->
Excelente análise 360°. Com base no que foi levantado, identifique de 3 a 5 pontos que oferecem o maior potencial para uma discussão aprofundada. Podem ser uma escolha de direção controversa, o uso simbólico de um elemento visual, a performance de um ator, a complexidade de um tema social ou uma ambiguidade na narrativa. Evite perguntas puramente factuais ("qual foi o orçamento?") ou retóricas — quero questões interpretativas, que admitam mais de uma resposta defensável.

Para garantir diversidade, cubra tipos diferentes de questão — por exemplo: uma sobre forma (imagem, som ou montagem), uma sobre tema ou ideologia/representação, uma sobre autoria ou comparação com outras obras e, se fizer sentido, uma sobre recepção e legado.

Formule cada ponto como uma pergunta analítica e justifique brevemente por que ele é crucial para desvendar as camadas mais profundas de **{{TITULO_DA_OBRA}}**. Apresente-os em lista numerada para que eu possa escolher — se eu preferir, posso propor uma pergunta minha em vez de usar a lista.
<!-- FIM DO PROMPT -->

## Dicas

- Você receberá de 3 a 5 perguntas. **Não precisa escolher só uma para sempre**:
  depois de concluir a Etapa 2.2, você pode voltar e aprofundar outra.
- A lista é um cardápio, não uma obrigação: se a Análise 360° despertou uma
  dúvida *sua*, leve a sua própria pergunta para a Etapa 2.2.
- Se nenhuma pergunta te fisgar, peça novas opções com um viés específico:
  *"Proponha outras 3 perguntas, agora focadas apenas na linguagem visual."*
- Copie a pergunta escolhida **exatamente como formulada** — ela entra no
  placeholder da próxima etapa.

## Próxima etapa

➡️ [Etapa 2.2 — Execução da Análise Focada](etapa-02.2-analise-focada.md)
