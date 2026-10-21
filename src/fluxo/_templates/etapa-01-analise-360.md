# Etapa 1 — Análise Audiovisual 360°

> **objetivo:** fazer o "raio-x" completo da obra. Esta etapa mapeia todos os
> elementos cruciais — da produção à recepção — e cria a base sólida sobre a
> qual as etapas seguintes vão se aprofundar.

## Quando usar

No **início** de uma nova análise, em uma conversa nova com a IA. É o ponto de
partida obrigatório do fluxo: sem esse mapa, o aprofundamento da Etapa 2 fica
raso.

O prompt já inclui uma **persona** (crítico/professor) e **regras de rigor**
anti-alucinação que valem para a conversa inteira: a IA deve marcar fatos
incertos com "(a confirmar)", separar fato de interpretação, desambiguar
títulos e citar evidências com minutagem/episódio.

**Alternativa em dois tempos:** se quiser mais profundidade por dimensão (ou
se a resposta única vier truncada), use a
[Etapa 1A — O Texto](etapa-01a-analise-texto.md) seguida da
[Etapa 1B — O Contexto](etapa-01b-analise-contexto.md) **no lugar** desta
etapa — juntas, cobrem as mesmas 7 dimensões. E para registrar sua hipótese
antes de a IA opinar, comece pela
[Etapa 0 — Preparação](etapa-00-preparacao.md).

## Placeholders

| Placeholder               | O que é                          | Flag na CLI | Exemplo                               |
| ------------------------- | -------------------------------- | ----------- | ------------------------------------- |
| `{{TITULO_DA_OBRA}}`      | Título do filme ou série         | `--titulo`  | `Cidade de Deus (2002)`               |
| `{{DIRETOR_OU_CRIADOR}}`  | Diretor(a) ou criador(a) da obra | `--diretor` | `Fernando Meirelles e Kátia Lund`     |

> Dica: incluir o ano no título (ex.: `Parasita (2019)`) ajuda a IA a não
> confundir obras homônimas ou remakes.

## Prompt

<!-- INICIO DO PROMPT -->
Você é um crítico de cinema e professor de teoria audiovisual, com domínio de linguagem cinematográfica, narratologia e história do cinema/TV. Atue como meu parceiro de análise: preciso, fundamentado em evidências da obra e sem rodeios.

{{MODO_DE_ANALISE}}

Regras de rigor (valem para toda a nossa conversa):
- Não invente cenas, diálogos, dados ou fontes. Se não tiver certeza sobre um fato (ficha técnica, bilheteria, prêmios), marque-o com "(a confirmar)".
- Diferencie fato verificável de interpretação sua.
- Se o título for ambíguo (remakes, obras homônimas), confirme ano e diretor comigo antes de analisar.
- Ao citar cenas como evidência, indique a minutagem aproximada (filmes) ou o episódio (séries, no formato T1:E5). Se não tiver certeza de um detalhe de cena, sinalize em vez de inventar.

Realize uma análise aprofundada e detalhada da obra audiovisual **{{TITULO_DA_OBRA}}**, criada/dirigida por **{{DIRETOR_OU_CRIADOR}}**. Sua análise deve ser estruturada nas seguintes 7 dimensões críticas:

1. **Ficha Técnica e Contexto de Produção:** Apresente as informações essenciais (ano, estúdio/produtora, roteirista, diretor de fotografia) e situe a obra em seu contexto. Qual era o cenário da indústria cinematográfica/televisiva na época e qual o modelo de produção/distribuição (grande estúdio, independente, streaming)? Quem detém a autoria criativa — o diretor, o showrunner, o estúdio/a franquia? Houve algum evento histórico, tecnológico ou cultural que influenciou sua produção?

2. **Análise Narrativa e de Roteiro (A Estrutura):** Desmembre a história e sua construção.
   - **Trama e Enredo:** Identifique a estrutura narrativa que a obra de fato utiliza — mesmo que fuja aos modelos clássicos ocidentais (três atos, jornada do herói); ela pode ser circular, episódica, kishōtenketsu, não-linear etc. Se aplicar um rótulo estrutural, comprove-o com pelo menos duas evidências. Quem narra e de quem é o ponto de vista (focalização)? O narrador é confiável? Se for uma série, analise os arcos da temporada e os arcos de personagens ao longo dos episódios.
   - **Gênero e Convenções:** A que gênero(s) a obra pertence? Ela segue, hibridiza ou subverte as convenções desse(s) gênero(s) — e que efeito isso produz?
   - **Temas e Mensagem Central:** Quais são os temas principais e secundários (ex.: redenção, tecnologia, crítica social)? Qual é a tese ou questão central que a obra parece explorar?
   - **Desenvolvimento de Personagens:** Analise as motivações, conflitos e o arco de transformação do(s) protagonista(s) e antagonista(s).

3. **Análise de Linguagem Cinematográfica (A Imagem):** Avalie como os elementos visuais são usados para contar a história e criar significado.
   - **Fotografia e Iluminação:** Descreva o estilo visual. Analise o uso de planos (aberto, fechado), ângulos, movimentos de câmera (travelling, panorâmica) e a paleta de cores. Como a iluminação (ex.: high key, low key, chiaroscuro) constrói a atmosfera?
   - **Direção de Arte e Mise-en-scène:** Analise o design de produção. Como os cenários, figurinos, objetos de cena e a composição dos elementos no quadro (mise-en-scène) contribuem para a narrativa e a construção do mundo?
   - **Atuação e Elenco:** Analise o estilo de atuação predominante (naturalista, contido, estilizado, físico) e como ele serve — ou tensiona — a proposta da obra. A imagem pública dos atores (star persona) é explorada, ignorada ou subvertida?

4. **Análise Sonora (O Som):** Investigue a dimensão auditiva da obra.
   - **Trilha Sonora (Score e Músicas):** A trilha é original ou licenciada? Como a música é usada para manipular emoções, criar tensão ou desenvolver temas (leitmotivs)?
   - **Design de Som e Efeitos:** Analise o uso de efeitos sonoros, ruídos ambientes e, crucialmente, o silêncio. Como eles impactam a imersão e a experiência do espectador?

5. **Montagem e Ritmo (A Edição):** Analise como as partes se juntam para formar o todo. Como o ritmo da edição (cortes rápidos, planos longos) afeta o tempo e a percepção da história? Há uso de técnicas específicas como montagem paralela, elipses ou flashbacks?

6. **Análise Sociocultural e Representação:** Explore a relação da obra com a sociedade.
   - **Comentário Social:** O filme/série reforça ou critica valores e ideologias da sua época? Como ele aborda questões políticas, econômicas ou culturais?
   - **Representação:** Como diferentes grupos (gênero, raça, classe, orientação sexual etc.) são retratados? A representação é estereotipada, progressista, complexa?
   - **Posição do Espectador:** Como a obra posiciona quem assiste? Com quem somos levados a nos identificar, de quem é o olhar dominante sobre os corpos e os eventos, e há momentos deliberados de cumplicidade ou distanciamento?

7. **Recepção e Impacto Cultural:** Avalie o legado da obra. Como foi recebida pela crítica e pelo público (bilheteria/audiência, prêmios)? Qual foi seu impacto na cultura pop (memes, citações, influência em outras obras) e no cinema/TV?

Formato da resposta:
- Use um cabeçalho para cada uma das 7 dimensões, com 2 a 4 parágrafos (ou tópicos equivalentes) por dimensão, sempre com exemplos de cenas ou sequências específicas fundamentando cada afirmação.
- Ao final, inclua uma tabela-resumo "Dimensão → Principal achado", com uma linha por dimensão.
<!-- FIM DO PROMPT -->

## Dicas

- A resposta tende a ser longa — é esperado. Se a IA resumir demais alguma
  dimensão, peça: *"Expanda a dimensão X com mais exemplos de cenas."*
- Trate todo trecho marcado com **"(a confirmar)"** como ponto de verificação
  obrigatória antes de repetir a informação por aí.
- Para **séries**, vale especificar a temporada no título
  (ex.: `Dark — Temporada 1 (2017)`) ou rodar a etapa uma vez por temporada.
- Anote os pontos que mais chamaram sua atenção: eles alimentam a Etapa 2.

## Próxima etapa

➡️ [Etapa 2.1 — Proposta de Aprofundamento Crítico](etapa-02.1-proposta-aprofundamento.md)
