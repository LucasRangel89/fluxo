# Como contribuir

Obrigado pelo interesse! O coração deste projeto são os **prompts** — então as
contribuições mais valiosas são melhorias, variações e traduções deles.

## Melhorando um prompt

Os templates ficam em [`prompts/`](prompts). Ao editar:

1. **Preserve os marcadores** `<!-- INICIO DO PROMPT -->` e
   `<!-- FIM DO PROMPT -->` — a CLI extrai o prompt entre eles.
2. **Preserve o padrão de placeholders** `{{NOME_DO_PLACEHOLDER}}` (maiúsculas
   e underscores). Se criar um placeholder novo, registre-o em
   `PLACEHOLDERS` no arquivo `src/fluxo/core.py` e adicione a flag
   correspondente em `src/fluxo/cli.py`.
3. Teste o prompt de verdade com uma obra e, se possível, descreva no PR o
   que melhorou na resposta da IA.

## Mexendo no código (CLI)

```bash
# Rodar os testes (sem dependências externas)
PYTHONPATH=src python -m unittest discover -s tests -v

# Experimentar a CLI sem instalar
PYTHONPATH=src python -m fluxo listar
```

Diretrizes rápidas:

- **Zero dependências** em tempo de execução — só biblioteca padrão do Python.
- Mensagens ao usuário em **português**, claras e acionáveis (diga *o que*
  fazer, não só o que deu errado).
- Toda funcionalidade nova merece um teste em [`tests/`](tests).

## Sugerindo uma variação ou tradução

Variações por tipo de obra (documentário, animação, curta-metragem) e
traduções dos prompts (inglês, espanhol...) são muito bem-vindas. Abra uma
issue antes, para alinharmos a estrutura de pastas/arquivos.

## Reportando problemas

Achou um prompt que gera resposta fraca, um erro factual no guia ou um bug na
CLI? Abra uma issue descrevendo: a obra analisada, a etapa, o que você
esperava e o que aconteceu.
