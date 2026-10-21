# Etapa 2.2 — Execução da Análise Focada

> **objetivo:** mergulhar fundo em **uma** questão. Em vez de um panorama, aqui
> a IA constrói um argumento: tese clara, evidências concretas da obra e
> análise de como essas evidências produzem significado.

## Quando usar

**Na mesma conversa**, imediatamente após escolher uma das perguntas propostas
na Etapa 2.1. Pode ser repetida várias vezes — uma para cada pergunta que você
quiser explorar.

## Placeholders

| Placeholder              | O que é                                        | Flag na CLI  | Exemplo                                                                 |
| ------------------------ | ---------------------------------------------- | ------------ | ----------------------------------------------------------------------- |
| `{{PERGUNTA_ESCOLHIDA}}` | Pergunta selecionada da lista da Etapa 2.1     | `--pergunta` | `Como a montagem acelerada transforma a violência em espetáculo...?`    |

## Prompt

<!-- INICIO DO PROMPT -->
Ótima proposta. Vamos aprofundar a seguinte questão: **{{PERGUNTA_ESCOLHIDA}}**

Ao construir sua análise, siga esta estrutura:

1. **Argumento Central:** Formule uma tese clara que responda à pergunta.
2. **Evidências da Obra:** Sustente seu argumento descrevendo cenas, sequências, diálogos ou escolhas técnicas específicas (ex.: "na cena X, o uso do close-up extremo combinado com a iluminação de baixo para cima...").
3. **Análise da Evidência:** Explique *como* esses elementos técnicos e narrativos constroem o significado que você está defendendo.
4. **Contexto e Comparações:** Se relevante, compare essa abordagem com a de outras obras do mesmo diretor, gênero ou período para enriquecer a análise.
<!-- FIM DO PROMPT -->

## Dicas

- Esta é a etapa mais "argumentativa" do fluxo: provoque a IA. Se discordar da
  tese, responda com seu contraponto e peça que ela defenda ou revise o
  argumento — o debate costuma gerar os melhores insights.
- Peça referências temporais quando útil: *"Indique em que ponto do filme
  (minutagem aproximada) cada cena citada acontece"* — e confira depois,
  pois IAs podem errar detalhes de cenas.
- Quer mais profundidade ainda? Peça uma segunda rodada:
  *"Agora critique sua própria tese: qual é o contra-argumento mais forte?"*

## Próxima etapa

➡️ [Etapa 3 — Consolidação, Diálogos e Expansão](etapa-03-sintese-conexoes.md)
