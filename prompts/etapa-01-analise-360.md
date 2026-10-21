# Etapa 1 — Análise Audiovisual 360°

> **objetivo:** fazer o "raio-x" completo da obra. Esta etapa mapeia todos os
> elementos cruciais — da produção à recepção — e cria a base sólida sobre a
> qual as etapas seguintes vão se aprofundar.

## Quando usar

No **início** de uma nova análise, em uma conversa nova com a IA. É o ponto de
partida obrigatório do fluxo: sem esse mapa, o aprofundamento da Etapa 2 fica
raso.

## Placeholders

| Placeholder               | O que é                          | Flag na CLI | Exemplo                               |
| ------------------------- | -------------------------------- | ----------- | ------------------------------------- |
| `{{TITULO_DA_OBRA}}`      | Título do filme ou série         | `--titulo`  | `Cidade de Deus (2002)`               |
| `{{DIRETOR_OU_CRIADOR}}`  | Diretor(a) ou criador(a) da obra | `--diretor` | `Fernando Meirelles e Kátia Lund`     |

> Dica: incluir o ano no título (ex.: `Parasita (2019)`) ajuda a IA a não
> confundir obras homônimas ou remakes.

## Prompt

<!-- INICIO DO PROMPT -->
Realize uma análise aprofundada e detalhada da obra audiovisual **{{TITULO_DA_OBRA}}**, criada/dirigida por **{{DIRETOR_OU_CRIADOR}}**. Sua análise deve ser estruturada nas seguintes 7 dimensões críticas:

1. **Ficha Técnica e Contexto de Produção:** Apresente as informações essenciais (ano, estúdio, roteirista, diretor de fotografia) e situe a obra em seu contexto. Qual era o cenário da indústria cinematográfica/televisiva na época? Houve algum evento histórico, tecnológico ou cultural que influenciou sua produção?

2. **Análise Narrativa e de Roteiro (A Estrutura):** Desmembre a história e sua construção.
   - **Trama e Enredo:** Qual é a estrutura narrativa (ex.: jornada do herói, estrutura de três atos, narrativa não-linear)? Se for uma série, analise os arcos da temporada e os arcos de personagens ao longo dos episódios.
   - **Temas e Mensagem Central:** Quais são os temas principais e secundários (ex.: redenção, tecnologia, crítica social)? Qual é a tese ou questão central que a obra parece explorar?
   - **Desenvolvimento de Personagens:** Analise as motivações, conflitos e o arco de transformação do(s) protagonista(s) e antagonista(s).

3. **Análise de Linguagem Cinematográfica (A Imagem):** Avalie como os elementos visuais são usados para contar a história e criar significado.
   - **Fotografia e Iluminação:** Descreva o estilo visual. Analise o uso de planos (aberto, fechado), ângulos, movimentos de câmera (travelling, panorâmica) e a paleta de cores. Como a iluminação (ex.: high key, low key, chiaroscuro) constrói a atmosfera?
   - **Direção de Arte e Mise-en-scène:** Analise o design de produção. Como os cenários, figurinos, objetos de cena e a composição dos elementos no quadro (mise-en-scène) contribuem para a narrativa e a construção do mundo?

4. **Análise Sonora (O Som):** Investigue a dimensão auditiva da obra.
   - **Trilha Sonora (Score e Músicas):** A trilha é original ou licenciada? Como a música é usada para manipular emoções, criar tensão ou desenvolver temas (leitmotivs)?
   - **Design de Som e Efeitos:** Analise o uso de efeitos sonoros, ruídos ambientes e, crucialmente, o silêncio. Como eles impactam a imersão e a experiência do espectador?

5. **Montagem e Ritmo (A Edição):** Analise como as partes se juntam para formar o todo. Como o ritmo da edição (cortes rápidos, planos longos) afeta o tempo e a percepção da história? Há uso de técnicas específicas como montagem paralela, elipses ou flashbacks?

6. **Análise Sociocultural e Representação:** Explore a relação da obra com a sociedade.
   - **Comentário Social:** O filme/série reforça ou critica valores e ideologias da sua época? Como ele aborda questões políticas, econômicas ou culturais?
   - **Representação:** Como diferentes grupos (gênero, raça, classe, orientação sexual etc.) são retratados? A representação é estereotipada, progressista, complexa?

7. **Recepção e Impacto Cultural:** Avalie o legado da obra. Como foi recebida pela crítica e pelo público (bilheteria/audiência, prêmios)? Qual foi seu impacto na cultura pop (memes, citações, influência em outras obras) e no cinema/TV?

*Sua resposta deve ser rica em exemplos de cenas ou sequências específicas da obra para fundamentar cada ponto da análise.*
<!-- FIM DO PROMPT -->

## Dicas

- A resposta tende a ser longa — é esperado. Se a IA resumir demais alguma
  dimensão, peça: *"Expanda a dimensão X com mais exemplos de cenas."*
- Para **séries**, vale especificar a temporada no título
  (ex.: `Dark — Temporada 1 (2017)`) ou rodar a etapa uma vez por temporada.
- Anote os pontos que mais chamaram sua atenção: eles alimentam a Etapa 2.

## Próxima etapa

➡️ [Etapa 2.1 — Proposta de Aprofundamento Crítico](etapa-02.1-proposta-aprofundamento.md)
