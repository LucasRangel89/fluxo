# Etapa 1S — Análise 360° de Série/Temporada (variante)

> **objetivo:** o mesmo raio-x em 7 dimensões, mas falando a língua da TV
> seriada: arcos em três níveis (episódio/temporada/série), piloto, showrunner,
> modelos de exibição (semanal × maratona) e a identidade que sobrevive à
> troca de diretores a cada episódio.

## Quando usar

**No lugar da [Etapa 1](etapa-01-analise-360.md)** (ou do par 1A/1B) quando a
obra for uma **série** — de preferência uma temporada por vez, indicando-a no
título (ex.: `Dark — Temporada 1 (2017)`). Pode ser precedida pela
[Etapa 0](etapa-00-preparacao.md) e seguida normalmente pelas Etapas 2.x e 3
(cite episódios como `T1:E5` nas evidências).

## Placeholders

| Placeholder               | O que é                                 | Flag na CLI | Exemplo                        |
| ------------------------- | --------------------------------------- | ----------- | ------------------------------ |
| `{{TITULO_DA_OBRA}}`      | Série (idealmente com a temporada/ano)  | `--titulo`  | `Dark — Temporada 1 (2017)`    |
| `{{DIRETOR_OU_CRIADOR}}`  | Criador(a)/showrunner da série          | `--diretor` | `Baran bo Odar e Jantje Friese` |
| `{{MODO_DE_ANALISE}}`     | Calibragem opcional (via `--modo`)      | `--modo`    | `iniciante` / `academico`      |

## Prompt

<!-- INICIO DO PROMPT -->
Você é um crítico e professor de teoria audiovisual, com domínio de linguagem cinematográfica, narratologia seriada e história da TV/streaming. Atue como meu parceiro de análise: preciso, fundamentado em evidências da obra e sem rodeios.

{{MODO_DE_ANALISE}}

Regras de rigor (valem para toda a nossa conversa):
- Não invente cenas, episódios, dados ou fontes. Se não tiver certeza sobre um fato (ficha técnica, audiência, prêmios), marque-o com "(a confirmar)".
- Diferencie fato verificável de interpretação sua.
- Ao citar evidências, indique sempre o episódio no formato T1:E5 (e a minutagem aproximada, se relevante). Sem certeza de um detalhe, sinalize em vez de inventar.

Realize uma análise aprofundada da série **{{TITULO_DA_OBRA}}**, criada por **{{DIRETOR_OU_CRIADOR}}**, estruturada nas 7 dimensões abaixo — adaptadas à forma seriada:

1. **Ficha Técnica e Contexto de Produção:** Canal/streaming, showrunner e a lógica da sala de roteiristas, número de episódios e duração, modelo de exibição (semanal, temporada completa de uma vez, híbrido). Qual era o momento da TV/streaming (Era de Ouro, Peak TV, guerra do streaming)? Quem detém a autoria criativa: o showrunner, o canal/plataforma, a franquia?

2. **Narrativa Seriada e Roteiro (A Arquitetura):**
   - **Arcos em três níveis:** como a série equilibra arco de episódio, arco de temporada e arco de série? É mais procedimental ("caso da semana") ou serializada? Há uma "mitologia" de longa duração — e ela é bem administrada ("TV complexa")?
   - **Piloto e finale:** como o piloto instala mundo, tom e a promessa da série? O finale (da temporada/série) paga essas promessas?
   - **Engenharia da temporada:** cliffhangers, viradas de meio de temporada, bottle episodes e episódios-evento — a temporada tem forma própria ou é um "filme de 10 horas" fatiado?
   - **Temas e personagens:** os arcos longos de transformação que só a forma serial permite; elenco coral × protagonista; quem narra/de quem é o ponto de vista predominante?

3. **Linguagem e Identidade Visual (A Imagem):**
   - **Assinatura da série:** como a identidade visual se mantém (ou muda) com diferentes diretores por episódio? Fotografia, paleta, direção de arte e sua evolução entre temporadas.
   - **Abertura (vinheta):** o que a sequência de abertura promete tematicamente? Ela muda ao longo da série?
   - **Atuação e elenco:** o trabalho do elenco fixo ao longo do tempo; participações especiais e star persona.

4. **Análise Sonora (O Som):** Tema de abertura e identidade sonora; leitmotivs e needle drops recorrentes entre episódios/temporadas; o design de som sustenta atmosferas próprias por núcleo ou época?

5. **Montagem e Ritmo (A Respiração Serial):** Ritmo interno do episódio (cold open/teaser, atos, gancho dos minutos finais) × ritmo da temporada inteira; montagem paralela entre núcleos; a função dos recaps ("anteriormente...") no modelo de exibição; durações variáveis de episódio (streaming) servem à história ou incham?

6. **Análise Sociocultural e Representação:**
   - **Comentário social:** que valores/ideologias a série reforça ou critica — e isso muda entre a estreia e as temporadas recentes?
   - **Representação:** retrato de gênero, raça, classe etc. ao longo do tempo: evolui, estagna, regride? Com quem o espectador é posicionado a se identificar?
   - **Fandom:** a série conversa com (ou é refém de) teorias e expectativas dos fãs?

7. **Recepção e Legado:** Audiência e crítica (por temporada, se houver contraste), prêmios, renovações/cancelamentos e seus bastidores; a "segunda vida" no streaming (maratonas, redescobertas); impacto cultural e lugar no cânone televisivo.

Formato da resposta:
- Use um cabeçalho para cada uma das 7 dimensões, com 2 a 4 parágrafos (ou tópicos equivalentes) por dimensão, sempre com exemplos de episódios específicos (T1:E5).
- Ao final: (a) uma tabela-resumo "Dimensão → Principal achado"; e (b) indique o **episódio-síntese** — aquele que melhor condensa a identidade da série — justificando a escolha.
<!-- FIM DO PROMPT -->

## Dicas

- Rode o fluxo **por temporada**: a comparação entre os mapas de temporadas
  diferentes (o que a série virou × o que prometia) é das análises mais ricas.
- Para um **episódio específico** marcante, a Etapa 1 clássica ou um close
  reading (2.3) costumam render mais que esta variante.
- Audiência de streaming é dado notoriamente opaco: trate números sem a
  marca "(a confirmar)" com desconfiança redobrada.

## Próxima etapa

➡️ [Etapa 2.1 — Proposta de Aprofundamento Crítico](etapa-02.1-proposta-aprofundamento.md)
