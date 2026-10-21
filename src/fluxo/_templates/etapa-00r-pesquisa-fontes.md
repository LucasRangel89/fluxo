# Etapa R — Pesquisa e Dossiê de Fontes

> **objetivo:** separar fatos verificáveis de interpretação antes da análise.
> Esta etapa produz um dossiê curto, com fontes e incertezas explicitadas,
> para reduzir invenções sobre produção, créditos, recepção e contexto.

## Quando usar

Opcionalmente, depois da Etapa 0 e antes da Análise 360°. Ela funciona
especialmente bem em uma ferramenta com pesquisa na web, mas também pode ser
usada em uma IA comum — nesse caso, trate cada afirmação sem fonte como uma
pista a confirmar, não como fato estabelecido.

## Placeholders

| Placeholder              | O que é                                             | Flag na CLI  | Exemplo                              |
| ------------------------ | --------------------------------------------------- | ------------ | ------------------------------------ |
| `{{TITULO_DA_OBRA}}`     | Obra, temporada ou comparação a pesquisar          | `--titulo`   | `Cidade de Deus (2002)`              |
| `{{DIRETOR_OU_CRIADOR}}` | Diretor(a), criador(a) ou showrunner               | `--diretor`  | `Fernando Meirelles e Kátia Lund`    |
| `{{TIPO_DE_OBRA}}`       | Filme, série/temporada, episódio, comparação etc.  | `--tipo`     | `Filme (longa-metragem de ficção)`   |
| `{{DOSSE_DE_FONTES}}`    | Metadados, links ou pistas que você já reuniu      | `--dossie`   | Links, ficha inicial, trechos        |

## Prompt

<!-- INICIO DO PROMPT -->
Atue agora apenas como pesquisador(a) audiovisual. Ainda **não faça a análise crítica** de **{{TITULO_DA_OBRA}}** ({{TIPO_DE_OBRA}}), de **{{DIRETOR_OU_CRIADOR}}**. Sua tarefa é construir um dossiê factual confiável para usarmos nas próximas etapas.

Informações e pistas que eu já tenho (podem estar incompletas ou incorretas — verifique):

{{DOSSE_DE_FONTES}}

Se você tiver acesso à web, pesquise. Priorize fontes primárias e institucionais — produtoras, festivais, arquivos, universidades, entrevistas e publicações especializadas — e use bases abertas apenas como ponto de partida. Para cada fato importante, forneça o link direto da fonte. Não invente links, datas, créditos, números ou citações.

Organize o dossiê assim:

1. **Identificação sem ambiguidade:** título original e em português, ano, país(es), formato, duração ou temporada/episódios e como distinguir a obra de remakes e homônimos.
2. **Ficha essencial:** direção/criação/showrunner, roteiro, fotografia, montagem, música/som, direção de arte, elenco principal e produção, somente quando houver fonte ou confiança alta.
3. **Produção e circulação:** contexto de produção, financiamento/modelo industrial quando relevante, lançamento, festivais, televisão/streaming e eventuais controvérsias documentadas.
4. **Recepção e legado:** recepção contemporânea, prêmios relevantes, reavaliações e influência — separando consenso, opinião de um crítico e dado mensurável.
5. **Pistas para a análise:** no máximo 5 fatos ou fontes que possam iluminar narrativa, imagem, som, montagem ou representação. Não transforme essas pistas em conclusão crítica.
6. **Incertezas e conflitos:** liste explicitamente o que não foi encontrado, o que diverge entre fontes e o que está "(a confirmar)".
7. **Fontes consultadas:** lista numerada com título, veículo/autor quando disponível e URL completa. Se você não tiver navegação na web, diga isso claramente e marque as referências lembradas como "(a confirmar)".

Regras: diferencie fato, interpretação e rumor; não use sinopses como prova de escolhas formais; não presuma minutagens ou detalhes de cena sem evidência; quando duas obras estiverem em comparação, pesquise as duas com o mesmo nível de cuidado.
<!-- FIM DO PROMPT -->

## Dicas

- Salve a resposta como dossiê da sessão. Na interface web, cole-a no campo
  **Dossiê de fontes** para que ela acompanhe as etapas seguintes.
- Um dossiê não transforma a IA em testemunha da obra: cenas e minutagens
  continuam precisando de cautela.
- Se a ferramenta não navegar na web, use esta etapa para obter uma lista de
  verificações e complete as fontes manualmente.

## Próxima etapa

➡️ [Etapa 1 — Análise Audiovisual 360°](etapa-01-analise-360.md) — ou a
variante adequada: [1A/1B](etapa-01a-analise-texto.md),
[1S para séries](etapa-01s-analise-serie.md) ou
[Etapa 4 comparativa](etapa-04-comparativa.md)
