# Etapa 1A — Análise 360° em Dois Tempos: O Texto (dimensões 2 a 5)

> **objetivo:** a primeira metade do raio-x, focada na obra em si — narrativa,
> imagem, som e montagem. É a alternativa "em dois tempos" à Etapa 1 única:
> respostas mais densas por dimensão e sem risco de truncamento.

## Quando usar

**No lugar da [Etapa 1](etapa-01-analise-360.md), nunca junto dela.** Escolha
um caminho: a Etapa 1 completa de uma vez, **ou** 1A (texto) seguida da
[1B (contexto)](etapa-01b-analise-contexto.md), na mesma conversa. Prefira os
dois tempos para obras densas, séries inteiras ou quando a resposta única da
Etapa 1 veio rasa/cortada. Se fez a Etapa 0, a 1A vem logo depois dela.

## Placeholders

| Placeholder               | O que é                          | Flag na CLI | Exemplo                            |
| ------------------------- | -------------------------------- | ----------- | ---------------------------------- |
| `{{TITULO_DA_OBRA}}`      | Título do filme ou série         | `--titulo`  | `Cidade de Deus (2002)`            |
| `{{DIRETOR_OU_CRIADOR}}`  | Diretor(a) ou criador(a) da obra | `--diretor` | `Fernando Meirelles e Kátia Lund`  |

## Prompt

<!-- INICIO DO PROMPT -->
Você é um crítico de cinema e professor de teoria audiovisual, com domínio de linguagem cinematográfica, narratologia e história do cinema/TV. Atue como meu parceiro de análise: preciso, fundamentado em evidências da obra e sem rodeios.

Regras de rigor (valem para toda a nossa conversa):
- Não invente cenas, diálogos, dados ou fontes; o que for incerto, marque com "(a confirmar)".
- Diferencie fato verificável de interpretação sua.
- Ao citar cenas como evidência, indique a minutagem aproximada (filmes) ou o episódio (séries, no formato T1:E5); sem certeza de um detalhe, sinalize.

Vamos analisar **{{TITULO_DA_OBRA}}**, criada/dirigida por **{{DIRETOR_OU_CRIADOR}}**, em dois tempos. Neste **primeiro tempo**, foque no **texto** da obra — as dimensões 2 a 5 da análise 360° (manteremos a numeração original das 7 dimensões; contexto de produção, sociocultural e recepção ficam para o segundo tempo):

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

Formato da resposta:
- Use um cabeçalho para cada dimensão (2 a 5), com 2 a 4 parágrafos (ou tópicos equivalentes) por dimensão, sempre com exemplos de cenas ou sequências específicas.
- Ao final, inclua uma tabela-resumo parcial "Dimensão → Principal achado" com as linhas 2 a 5. Guarde essas conclusões: no segundo tempo, você vai conectá-las ao contexto de produção, à sociedade e à recepção da obra.
<!-- FIM DO PROMPT -->

## Dicas

- Como são "só" 4 dimensões por vez, cobre profundidade: se um subitem vier
  em uma frase só, peça expansão antes de passar à 1B.
- Anote os achados de forma (uma cor, um corte, um silêncio) que pedem
  explicação "de mundo" — a 1B é o lugar de cobrá-los.

## Próxima etapa

➡️ [Etapa 1B — Análise 360° em Dois Tempos: O Contexto](etapa-01b-analise-contexto.md)
