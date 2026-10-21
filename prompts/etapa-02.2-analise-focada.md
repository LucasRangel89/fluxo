# Etapa 2.2 — Execução da Análise Focada

> **objetivo:** mergulhar fundo em **uma** questão. Em vez de um panorama, aqui
> a IA constrói um argumento completo: tese clara, evidências concretas da
> obra, análise de como elas produzem significado — e um **contra-argumento**
> obrigatório, para a tese não passar sem ser testada.

## Quando usar

**Na mesma conversa**, imediatamente após escolher uma das perguntas propostas
na Etapa 2.1 (ou formular a sua própria). Pode ser repetida várias vezes —
uma para cada pergunta que você quiser explorar.

## Placeholders

| Placeholder              | O que é                                        | Flag na CLI  | Exemplo                                                                 |
| ------------------------ | ---------------------------------------------- | ------------ | ----------------------------------------------------------------------- |
| `{{PERGUNTA_ESCOLHIDA}}` | Pergunta selecionada da lista da Etapa 2.1     | `--pergunta` | `Como a montagem acelerada transforma a violência em espetáculo...?`    |

## Prompt

<!-- INICIO DO PROMPT -->
Ótima proposta. Vamos aprofundar a seguinte questão: **{{PERGUNTA_ESCOLHIDA}}**

Ao construir sua análise, siga esta estrutura:

1. **Argumento Central:** Formule uma tese clara que responda à pergunta.
2. **Evidências da Obra:** Sustente seu argumento descrevendo cenas, sequências, diálogos ou escolhas técnicas específicas (ex.: "na cena X, o uso do close-up extremo combinado com a iluminação de baixo para cima..."), com minutagem ou episódio (T1:E5) aproximados. Se não tiver certeza de algum detalhe de cena, sinalize em vez de inventar.
3. **Análise da Evidência:** Explique *como* esses elementos técnicos e narrativos constroem o significado que você está defendendo.
4. **Contra-argumento:** Apresente a objeção mais forte à sua própria tese — uma leitura alternativa plausível — e diga que tipo de evidência derrubaria o seu argumento. Em seguida, responda à objeção ou ajuste a tese.
5. **Contexto e Comparações:** Se relevante, compare essa abordagem com a de outras obras do mesmo diretor, gênero ou período para enriquecer a análise.
<!-- FIM DO PROMPT -->

## Dicas

- Esta é a etapa mais "argumentativa" do fluxo: **provoque a IA**. O prompt já
  a obriga a apresentar um contra-argumento; se você tiver um contraexemplo
  seu (uma cena que parece desmentir a tese), jogue na mesa e veja a tese se
  refinar — ou ruir, o que também é um ótimo resultado.
- Confira as cenas citadas (a minutagem/episódio ajuda nisso): é aqui que IAs
  mais "preenchem lacunas" com detalhes plausíveis, porém inventados.
- Terminou uma pergunta e sobrou fôlego? Volte à lista da Etapa 2.1 e rode a
  2.2 de novo com outra questão.

## Próxima etapa

➡️ Opcional, para ir ainda mais fundo:
[Etapa 2.3 — Close Reading de uma Sequência](etapa-02.3-close-reading.md)

➡️ Fechamento: [Etapa 3 — Consolidação, Diálogos e Expansão](etapa-03-sintese-conexoes.md)
