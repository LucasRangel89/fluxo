# Etapa 4 — Análise Comparativa: Duas Obras em Diálogo (variante)

> **objetivo:** colocar **duas obras frente a frente** sob um eixo claro de
> comparação — mesmo diretor, remake, mesmo tema, mesma época, gêneros
> irmãos. Comparar é o atalho mais rápido para enxergar o que, sozinha,
> nenhuma das duas revela.

## Quando usar

Como **extensão** do fluxo: depois de analisar uma obra (Etapas 0–3), para
confrontá-la com outra; ou numa **conversa nova**, comparando duas obras que
você já conhece. Casos clássicos: original × remake, dois filmes do mesmo
autor em fases distintas, duas respostas opostas ao mesmo tema, obra × sua
influência declarada.

## Placeholders

| Placeholder              | O que é                                          | Flag na CLI    | Exemplo                                        |
| ------------------------ | ------------------------------------------------ | -------------- | ---------------------------------------------- |
| `{{OBRA_A}}`             | Primeira obra (com ano)                          | `--obra-a`     | `Cidade de Deus (2002)`                        |
| `{{DIRETOR_A}}`          | Diretor(a)/criador(a) da obra A                  | `--diretor-a`  | `Fernando Meirelles e Kátia Lund`              |
| `{{OBRA_B}}`             | Segunda obra (com ano)                           | `--obra-b`     | `Tropa de Elite (2007)`                        |
| `{{DIRETOR_B}}`          | Diretor(a)/criador(a) da obra B                  | `--diretor-b`  | `José Padilha`                                 |
| `{{EIXO_DE_COMPARACAO}}` | O critério/eixo do confronto                     | `--eixo`       | `Duas visões da violência urbana brasileira: de dentro da favela × pelo Estado` |
| `{{MODO_DE_ANALISE}}`    | Calibragem opcional (via `--modo`)               | `--modo`       | `iniciante` / `academico`                      |

## Prompt

<!-- INICIO DO PROMPT -->
Você é um crítico de cinema e professor de teoria audiovisual. Atue como meu parceiro de análise: preciso, fundamentado em evidências das obras e sem rodeios. Regras: não invente cenas, dados ou fontes (o incerto, marque com "(a confirmar)"); diferencie fato de interpretação; cite evidências com minutagem (filmes) ou episódio T1:E5 (séries).

{{MODO_DE_ANALISE}}

Vamos fazer uma **análise comparativa** entre duas obras audiovisuais:

- **Obra A:** {{OBRA_A}}, de {{DIRETOR_A}}
- **Obra B:** {{OBRA_B}}, de {{DIRETOR_B}}
- **Eixo da comparação:** {{EIXO_DE_COMPARACAO}}

Estruture a análise assim:

1. **Cartões de apresentação:** uma mini-ficha de cada obra — contexto de produção, lugar na carreira do(a) autor(a), recepção — apenas o essencial para situar o confronto.
2. **Terreno comum e a pergunta do eixo:** o que torna essas duas obras comparáveis (gênero, tema, influência direta, remake, mesma época)? Formule a pergunta que esta comparação, de fato, responde.
3. **Comparação dimensão a dimensão** — sempre em pares ("em A...; em B...; o contraste revela..."), com evidências concretas dos dois lados:
   - Narrativa, estrutura e temas;
   - Imagem: fotografia, direção de arte/mise-en-scène e atuação;
   - Som e montagem/ritmo;
   - Representação e comentário social; posição do espectador em cada uma.
4. **O diálogo entre elas:** há influência direta, resposta deliberada ou apenas ar de época (zeitgeist) compartilhado? O que cada uma enxerga que a outra não alcança?
5. **Síntese e juízo:** o que cada obra ilumina na outra quando vistas juntas? **Nos critérios do eixo escolhido** (não em gosto pessoal), qual realiza melhor a sua proposta — e a que custo?
6. **Tabela comparativa final:** linhas = os critérios do eixo; colunas = Obra A × Obra B; e uma última coluna com o veredito de cada contraste em uma frase.
<!-- FIM DO PROMPT -->

## Dicas

- O **eixo** é tudo: "compare X e Y" rende lista de semelhanças; "como X e Y
  filmam a violência — espetáculo ou denúncia?" rende análise. Se não tiver
  um eixo, peça antes: *"Que eixos de comparação entre A e B seriam mais
  férteis? Proponha 3."*
- Sequência poderosa: rode o fluxo completo (0→3) em cada obra, em conversas
  separadas, e use esta etapa como "relatório de convergência" depois.
- Desconfie de simetrias perfeitas demais: boas comparações têm assimetrias —
  cobre-as ("onde a comparação quebra?").

## Fim (ou novo começo)

🎬 Comparação concluída! Para dissecar uma das obras a fundo, volte à
[Etapa 1 — Análise Audiovisual 360°](etapa-01-analise-360.md).
