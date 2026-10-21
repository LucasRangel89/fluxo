# Etapa 0 — Preparação (antes da análise)

> **objetivo:** preparar o terreno. Antes de qualquer raio-x, esta etapa
> identifica a obra sem ambiguidade, calibra a IA ao seu objetivo e nível —
> e, o mais importante, **registra as suas impressões e hipótese iniciais
> antes de a IA opinar**. É o antídoto contra a ancoragem: na Etapa 3, você
> compara o antes/depois da sua própria leitura.

## Quando usar

Como **primeira mensagem** da conversa, antes da Etapa 1 (ou da 1A). É
**opcional, mas recomendada** — sem ela, o fluxo funciona, mas você perde o
registro da sua leitura "pura". Pode rodar antes de assistir (neste caso,
"impressões iniciais" = suas expectativas e o porquê da escolha) ou logo
depois de assistir, com as impressões frescas.

## Placeholders

| Placeholder              | O que é                                             | Flag na CLI  | Exemplo                                              |
| ------------------------ | --------------------------------------------------- | ------------ | ---------------------------------------------------- |
| `{{TITULO_DA_OBRA}}`     | Título do filme ou série                            | `--titulo`   | `Cidade de Deus (2002)`                              |
| `{{DIRETOR_OU_CRIADOR}}` | Diretor(a) ou criador(a) da obra                    | `--diretor`  | `Fernando Meirelles e Kátia Lund`                    |
| `{{TIPO_DE_OBRA}}`       | Filme, série/temporada, episódio, documentário etc. | `--tipo`     | `Filme (longa-metragem de ficção)`                   |
| `{{META_DA_ANALISE}}`| Para que você está analisando                       | `--objetivo` | `Estudar a fundo um clássico brasileiro`             |
| `{{NIVEL_DO_USUARIO}}`   | Sua familiaridade com análise de cinema/TV          | `--nivel`    | `Intermediário — leio críticas, quero mais técnica`  |
| `{{IMPRESSOES_INICIAIS}}`| Suas impressões/hipóteses, com suas palavras        | `--impressoes` | `Achei a violência espetacularizada demais; hoje desconfio que a forma é o tema` |

## Prompt

<!-- INICIO DO PROMPT -->
Olá! Vamos analisar juntos, em etapas, a obra audiovisual **{{TITULO_DA_OBRA}}** ({{TIPO_DE_OBRA}}), de **{{DIRETOR_OU_CRIADOR}}**. Antes da análise completa, quero registrar o ponto de partida — por favor, **ainda não analise a obra**.

Sobre mim e esta análise:
- Meu objetivo: {{META_DA_ANALISE}}
- Meu nível de familiaridade com análise de cinema/TV: {{NIVEL_DO_USUARIO}}
- Minhas impressões e hipóteses iniciais (antes de qualquer análise): {{IMPRESSOES_INICIAIS}}

Nesta etapa de preparação, faça apenas isto:

1. Confirme que identificou a obra certa. Se houver remakes ou obras homônimas, pergunte antes de prosseguirmos.
2. Registre em um parágrafo curto, com as suas palavras, a minha hipótese/impressão inicial — sem julgá-la ou corrigi-la agora. Vamos retomá-la no fim da análise para ver o que mudou.
3. Sugira de 3 a 5 pontos de atenção para eu observar ao assistir (ou reassistir): elementos de forma e temas para ficar de olho (ex.: "repare em como a paleta muda entre os atos"), sem revelar desfechos.
4. Confirme que está pronto para a análise completa, calibrando profundidade e vocabulário ao meu nível e objetivo ao longo de toda a conversa.

Seja breve: isto é só a preparação.
<!-- FIM DO PROMPT -->

## Dicas

- Nas impressões iniciais, **sinceridade vale mais que eloquência**: "achei
  arrastado, mas não sei por quê" é um excelente ponto de partida — é
  justamente o tipo de intuição que a análise vai testar.
- Os "pontos de atenção" viram a sua lente de exibição: anote-os antes de dar
  o play (a CLI os guarda no `registro.md` junto da sua hipótese).
- Se a IA tentar emendar a análise já nesta etapa, corte com educação:
  *"Guarde isso para a Etapa 1, por favor."*

## Próxima etapa

➡️ [Etapa 1 — Análise Audiovisual 360°](etapa-01-analise-360.md) — ou, em dois
tempos: [Etapa 1A — O Texto](etapa-01a-analise-texto.md)
