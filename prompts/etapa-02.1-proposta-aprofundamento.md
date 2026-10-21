# Etapa 2.1 — Proposta de Aprofundamento Crítico

> **objetivo:** transformar o mapa da Etapa 1 em um debate crítico. Aqui a IA
> deixa de ser uma "enciclopédia" e passa a atuar como parceira de análise,
> propondo as perguntas mais férteis para dissecar a obra.

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
Excelente análise 360°. Com base no que foi levantado, identifique de 3 a 5 pontos que oferecem o maior potencial para uma discussão aprofundada. Podem ser uma escolha de direção controversa, o uso simbólico de um elemento visual, a performance de um ator, a complexidade de um tema social ou uma ambiguidade na narrativa.

Formule cada ponto como uma pergunta analítica e justifique brevemente por que ele é crucial para desvendar as camadas mais profundas de **{{TITULO_DA_OBRA}}**. Apresente-os em formato de lista para que eu possa escolher.
<!-- FIM DO PROMPT -->

## Dicas

- Você receberá de 3 a 5 perguntas. **Não precisa escolher só uma para sempre**:
  depois de concluir a Etapa 2.2, você pode voltar e aprofundar outra.
- Se nenhuma pergunta te fisgar, peça novas opções com um viés específico:
  *"Proponha outras 3 perguntas, agora focadas apenas na linguagem visual."*
- Copie a pergunta escolhida **exatamente como formulada** — ela entra no
  placeholder da próxima etapa.

## Próxima etapa

➡️ [Etapa 2.2 — Execução da Análise Focada](etapa-02.2-analise-focada.md)
