"""Interface de linha de comando do Fluxo.

Comandos:
    fluxo listar      -> mostra as etapas e o que cada uma requer
    fluxo gerar N     -> gera o prompt da etapa N, pronto para colar na IA
    fluxo novo        -> cria uma pasta de análise com todos os prompts
    fluxo sessao      -> cria somente a trilha guiada relevante + maestro
    fluxo maestro     -> gera um roteiro único para a IA conduzir a sessão
    fluxo interativo  -> modo guiado: perguntas no terminal, prompt no fim

Etapas: 0 (preparação), R (pesquisa/fontes), 1 (360° de uma vez) ou
1a+1b (em dois tempos), 1s (variante de séries), 2.1 (proposta),
2.2 (focada), 2.3 (close reading), 3 (síntese) e 4 (comparativa).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from . import __version__
from .core import (
    ETAPAS,
    MODOS_DE_ANALISE,
    OPCIONAIS,
    PLACEHOLDERS,
    TRILHAS,
    FluxoError,
    criar_manifesto_sessao,
    etapas_da_sessao,
    gerar_prompt,
    gerar_prompt_maestro,
    gerar_prompt_sessao,
    gerar_registro,
    normalizar_etapa,
    normalizar_trilha,
    placeholders_do_template,
    slugificar,
)


def _ler_dossie(args: argparse.Namespace) -> str:
    """Lê o dossiê informado por texto ou arquivo, se houver."""
    arquivo = getattr(args, "dossie_arquivo", None)
    if arquivo:
        caminho = Path(arquivo).expanduser()
        if not caminho.is_file():
            raise FluxoError(f"Arquivo de dossiê não encontrado: {arquivo}")
        return caminho.read_text(encoding="utf-8").strip()
    return getattr(args, "dossie", "") or ""


def _valores(args: argparse.Namespace) -> dict[str, str]:
    """Mapeia as flags da CLI para os placeholders dos templates."""
    modo = getattr(args, "modo", "padrao") or "padrao"
    return {
        "TITULO_DA_OBRA": getattr(args, "titulo", "") or "",
        "DIRETOR_OU_CRIADOR": getattr(args, "diretor", "") or "",
        "TIPO_DE_OBRA": getattr(args, "tipo", "") or "",
        "META_DA_ANALISE": getattr(args, "objetivo", "") or "",
        "NIVEL_DO_USUARIO": getattr(args, "nivel", "") or "",
        "IMPRESSOES_INICIAIS": getattr(args, "impressoes", "") or "",
        "PERGUNTA_ESCOLHIDA": getattr(args, "pergunta", "") or "",
        "SEQUENCIA_ESCOLHIDA": getattr(args, "sequencia", "") or "",
        "OBRA_A": getattr(args, "obra_a", "") or "",
        "DIRETOR_A": getattr(args, "diretor_a", "") or "",
        "OBRA_B": getattr(args, "obra_b", "") or "",
        "DIRETOR_B": getattr(args, "diretor_b", "") or "",
        "EIXO_DE_COMPARACAO": getattr(args, "eixo", "") or "",
        "MODO_DE_ANALISE": MODOS_DE_ANALISE[modo],
        "DOSSE_DE_FONTES": _ler_dossie(args),
    }


def _copiar(texto: str) -> bool:
    """Tenta copiar o texto para a área de transferência (melhor esforço)."""
    try:
        import pyperclip  # type: ignore[import-not-found]

        pyperclip.copy(texto)
        return True
    except Exception:
        pass
    for comando in (
        ["pbcopy"],                                # macOS
        ["wl-copy"],                               # Linux/Wayland
        ["xclip", "-selection", "clipboard"],      # Linux/X11
        ["xsel", "--clipboard", "--input"],        # Linux/X11
        ["clip"],                                  # Windows
    ):
        if shutil.which(comando[0]):
            try:
                subprocess.run(comando, input=texto.encode("utf-8"), check=True)
                return True
            except Exception:
                continue
    return False


def cmd_listar(_args: argparse.Namespace) -> int:
    print("Etapas do fluxo:\n")
    for etapa in ETAPAS.values():
        flags = ", ".join(PLACEHOLDERS[p][1] or p for p in etapa.obrigatorios)
        print(f"  Etapa {etapa.id:<4} {etapa.nome}")
        print(f"           {etapa.descricao}")
        print(f"           Requer: {flags}\n")
    print("Modos (--modo): padrao | iniciante (explica os termos) | academico.")
    print(
        'Exemplo: fluxo gerar 1 --titulo "Cidade de Deus (2002)" '
        '--diretor "Fernando Meirelles e Kátia Lund"'
    )
    print("Para uma jornada única, use 'fluxo maestro' ou 'fluxo sessao'.")
    print("Ou rode 'fluxo interativo' e responda às perguntas.")
    return 0


def cmd_gerar(args: argparse.Namespace) -> int:
    etapa_id = normalizar_etapa(args.etapa)
    prompt = gerar_prompt(etapa_id, _valores(args))
    if args.salvar:
        destino = Path(args.salvar)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(prompt + "\n", encoding="utf-8")
        print(f"Prompt da Etapa {etapa_id} salvo em {destino}", file=sys.stderr)
    else:
        print(prompt)
    if args.copiar:
        if _copiar(prompt):
            print("Prompt copiado para a área de transferência.", file=sys.stderr)
        else:
            print(
                "Aviso: não consegui copiar automaticamente. "
                "Instale o pacote 'pyperclip' ou copie o texto manualmente.",
                file=sys.stderr,
            )
    return 0


def _entregar_prompt(prompt: str, args: argparse.Namespace, rotulo: str) -> int:
    """Imprime ou salva um prompt e, se pedido, copia o texto."""
    salvar = getattr(args, "salvar", None)
    if salvar:
        destino = Path(salvar)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_text(prompt + "\n", encoding="utf-8")
        print(f"{rotulo} salvo em {destino}", file=sys.stderr)
    else:
        print(prompt)
    if getattr(args, "copiar", False):
        if _copiar(prompt):
            print("Prompt copiado para a área de transferência.", file=sys.stderr)
        else:
            print(
                "Aviso: não consegui copiar automaticamente. "
                "Instale o pacote 'pyperclip' ou copie o texto manualmente.",
                file=sys.stderr,
            )
    return 0


def _inferir_trilha(
    args: argparse.Namespace, valores: dict[str, str]
) -> str:
    """Infere a trilha quando o usuário não a informou explicitamente."""
    informada = getattr(args, "trilha", None)
    if informada:
        return normalizar_trilha(informada)
    # Se há uma obra principal, A/B podem ser apenas dados extras do kit
    # completo. A trilha comparativa automática exige ausência de título ou
    # uma escolha explícita com --trilha comparativa.
    if (valores.get("OBRA_A") or valores.get("OBRA_B")) and not valores.get(
        "TITULO_DA_OBRA"
    ):
        return "comparativa"
    texto = " ".join(
        valores.get(chave, "")
        for chave in ("TITULO_DA_OBRA", "TIPO_DE_OBRA")
    ).casefold()
    if any(termo in texto for termo in ("série", "serie", "temporada", "episódio", "episodio")):
        return "serie"
    return "padrao"


def cmd_maestro(args: argparse.Namespace) -> int:
    valores = _valores(args)
    trilha = _inferir_trilha(args, valores)
    if trilha == "comparativa":
        if not valores.get("OBRA_A") and not valores.get("OBRA_B"):
            raise FluxoError(
                "Para o Prompt Maestro comparativo, informe ao menos --obra-a e --obra-b."
            )
    elif not valores.get("TITULO_DA_OBRA"):
        raise FluxoError("Informe o título da obra com --titulo.")
    prompt = gerar_prompt_maestro(
        valores,
        trilha=trilha,
        incluir_pesquisa=not getattr(args, "sem_pesquisa", False),
        incluir_close_reading=not getattr(args, "sem_close_reading", False),
    )
    return _entregar_prompt(prompt, args, "Prompt Maestro")


def _texto_dossie(valores: dict[str, str]) -> str:
    dossie = (valores.get("DOSSE_DE_FONTES") or "").strip()
    if dossie:
        return "# Dossiê de fontes\n\n" + dossie + "\n"
    return """# Dossiê de fontes

> Reúna aqui metadados, links e trechos verificados. Este material serve
> para fatos externos; as interpretações devem continuar ancoradas na obra.

## Identificação

-

## Fatos verificados

-

## Fontes

-

## Incertezas e conflitos

-
"""


def _escrever_extras_da_sessao(
    pasta: Path,
    valores: dict[str, str],
    trilha: str,
    args: argparse.Namespace,
) -> list[str]:
    """Escreve maestro, manifesto e dossiê de uma pasta de sessão."""
    criados: list[str] = []
    maestro = gerar_prompt_maestro(
        valores,
        trilha=trilha,
        incluir_pesquisa=not getattr(args, "sem_pesquisa", False),
        incluir_close_reading=not getattr(args, "sem_close_reading", False),
    )
    (pasta / "00-prompt-maestro.md").write_text(
        maestro + "\n", encoding="utf-8"
    )
    criados.append("00-prompt-maestro.md")

    manifesto = criar_manifesto_sessao(
        valores,
        trilha=trilha,
        incluir_pesquisa=not getattr(args, "sem_pesquisa", False),
        incluir_close_reading=not getattr(args, "sem_close_reading", False),
    )
    (pasta / "sessao.json").write_text(
        json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    criados.append("sessao.json")

    (pasta / "dossie-de-fontes.md").write_text(
        _texto_dossie(valores), encoding="utf-8"
    )
    criados.append("dossie-de-fontes.md")
    return criados

# Placeholders que podem ficar pendentes ao montar a estrutura com `novo`
# (são preenchidos ao longo da conversa: pergunta da 2.1, sequência da 2.3...).
_PENDENTES_ACEITAVEIS = (
    "DIRETOR_OU_CRIADOR", "TIPO_DE_OBRA", "META_DA_ANALISE",
    "NIVEL_DO_USUARIO", "IMPRESSOES_INICIAIS", "PERGUNTA_ESCOLHIDA",
    "SEQUENCIA_ESCOLHIDA", "OBRA_A", "DIRETOR_A", "OBRA_B", "DIRETOR_B",
    "EIXO_DE_COMPARACAO",
)


def cmd_novo(args: argparse.Namespace) -> int:
    valores = _valores(args)
    if not valores["TITULO_DA_OBRA"]:
        raise FluxoError("Informe o título da obra com --titulo.")
    slug = args.slug or slugificar(valores["TITULO_DA_OBRA"])
    pasta = Path(args.destino) / slug
    if pasta.exists() and any(pasta.iterdir()) and not args.forcar:
        raise FluxoError(
            f"A pasta {pasta} já existe e não está vazia. "
            "Use --forcar para sobrescrever os arquivos."
        )
    pasta.mkdir(parents=True, exist_ok=True)

    trilha = _inferir_trilha(args, valores)
    criados: list[str] = []
    for etapa in ETAPAS.values():
        # Modo não-estrito: o que ainda não se sabe (ex.: a pergunta da
        # Etapa 2.2) vira [PREENCHER: ...] dentro do arquivo gerado. Na
        # Fase 5, os arquivos já nascem como peças de uma sessão importável.
        conteudo = gerar_prompt_sessao(
            etapa.id, valores, trilha=trilha, incluir_contexto=False
        )
        (pasta / etapa.arquivo_saida).write_text(conteudo + "\n", encoding="utf-8")
        criados.append(etapa.arquivo_saida)

    criados.extend(_escrever_extras_da_sessao(pasta, valores, trilha, args))

    valores_registro = {**valores, "DATA_DA_ANALISE": date.today().isoformat()}
    (pasta / "registro.md").write_text(gerar_registro(valores_registro), encoding="utf-8")
    criados.append("registro.md")

    print(f"Análise criada em {pasta}/")
    for nome in criados:
        print(f"  - {nome}")
    pendentes = [
        chave for chave in _PENDENTES_ACEITAVEIS if not valores.get(chave)
    ]
    if pendentes:
        nomes = ", ".join(PLACEHOLDERS[chave][0] for chave in pendentes)
        print(
            f"\nObservação: ficaram pendentes ({nomes}). Complete os trechos "
            "[PREENCHER: ...] nos arquivos gerados quando chegar a hora."
        )
    return 0


def cmd_sessao(args: argparse.Namespace) -> int:
    """Cria somente os artefatos relevantes para uma trilha guiada."""
    valores = _valores(args)
    trilha = _inferir_trilha(args, valores)

    if trilha == "comparativa":
        foco = " × ".join(
            trecho
            for trecho in (
                valores.get("OBRA_A", "").strip(),
                valores.get("OBRA_B", "").strip(),
            )
            if trecho
        )
        if not foco:
            raise FluxoError(
                "Para uma sessão comparativa, informe --obra-a e --obra-b."
            )
        valores_registro_base = {
            **valores,
            "TITULO_DA_OBRA": foco,
            "DIRETOR_OU_CRIADOR": "; ".join(
                trecho
                for trecho in (
                    valores.get("DIRETOR_A", "").strip(),
                    valores.get("DIRETOR_B", "").strip(),
                )
                if trecho
            ),
        }
    else:
        foco = valores.get("TITULO_DA_OBRA", "").strip()
        if not foco:
            raise FluxoError("Informe o título da obra com --titulo.")
        valores_registro_base = valores

    slug = args.slug or slugificar(foco)
    pasta = Path(args.destino) / slug
    if pasta.exists() and any(pasta.iterdir()) and not args.forcar:
        raise FluxoError(
            f"A pasta {pasta} já existe e não está vazia. "
            "Use --forcar para sobrescrever os arquivos."
        )
    pasta.mkdir(parents=True, exist_ok=True)

    ordem = etapas_da_sessao(
        trilha,
        incluir_pesquisa=not args.sem_pesquisa,
        incluir_close_reading=not args.sem_close_reading,
    )
    criados: list[str] = []
    for etapa_id in ordem:
        etapa = ETAPAS[etapa_id]
        conteudo = gerar_prompt_sessao(
            etapa_id, valores, trilha=trilha, incluir_contexto=False
        )
        (pasta / etapa.arquivo_saida).write_text(
            conteudo + "\n", encoding="utf-8"
        )
        criados.append(etapa.arquivo_saida)

    criados.extend(_escrever_extras_da_sessao(pasta, valores, trilha, args))

    valores_registro = {
        **valores_registro_base,
        "DATA_DA_ANALISE": date.today().isoformat(),
    }
    (pasta / "registro.md").write_text(
        gerar_registro(valores_registro), encoding="utf-8"
    )
    criados.append("registro.md")

    print(f"Sessão guiada criada em {pasta}/")
    print(f"Trilha: {trilha} · etapas: {', '.join(ordem)}")
    for nome in criados:
        print(f"  - {nome}")
    print(
        "\nComece por 00-prompt-maestro.md para uma conversa única ou siga "
        "os arquivos na ordem acima para conduzir etapa por etapa."
    )
    return 0


def _perguntar(texto: str) -> str:
    return input(texto)


def _sim(texto: str) -> bool:
    return _perguntar(texto).strip().lower() in ("s", "sim", "y", "yes")


def cmd_interativo(_args: argparse.Namespace) -> int:
    """Modo guiado: perguntas no terminal e prompt pronto no fim de cada etapa."""
    print("🎬 Fluxo — modo interativo")
    print("Responda às perguntas e eu monto os prompts para você.")
    print("Dica: rode as etapas na ordem, colando cada prompt na MESMA conversa com a IA.\n")
    valores: dict[str, str] = {chave: "" for chave in PLACEHOLDERS}
    try:
        valores["TITULO_DA_OBRA"] = _perguntar("Título do filme/série: ").strip()
        if not valores["TITULO_DA_OBRA"]:
            print("Sem título, sem análise. Até logo! 🎬")
            return 0
        valores["DIRETOR_OU_CRIADOR"] = _perguntar(
            "Diretor(a)/criador(a) / showrunner (Enter = preencher depois): "
        ).strip()
        print("Modo de análise: [0] padrão  [1] iniciante (explica os termos)  "
              "[2] acadêmico")
        escolha = _perguntar("Modo [0]: ").strip()
        modo = {"1": "iniciante", "2": "academico"}.get(escolha, "padrao")
        valores["MODO_DE_ANALISE"] = MODOS_DE_ANALISE[modo]
        slug = slugificar(valores["TITULO_DA_OBRA"])

        while True:
            print("\nEtapas disponíveis:")
            for etapa in ETAPAS.values():
                print(f"  [{etapa.id:>4}] {etapa.nome}")
            entrada = _perguntar(
                "\nQual etapa você quer gerar? (id da etapa, ou 'sair'): "
            ).strip().lower()
            if entrada in ("sair", "q", "quit"):
                break
            if not entrada:
                continue
            try:
                etapa = ETAPAS[normalizar_etapa(entrada)]
            except FluxoError as erro:
                print(f"⚠️  {erro}")
                continue

            for chave in placeholders_do_template(etapa.id):
                if chave in OPCIONAIS or valores.get(chave):
                    continue
                nome, _flag = PLACEHOLDERS.get(chave, (chave, None))
                valores[chave] = _perguntar(f"{nome}: ").strip()

            try:
                prompt = gerar_prompt(etapa.id, valores)
            except FluxoError as erro:
                print(f"⚠️  {erro} Tente de novo.")
                # Limpa só o que a etapa exigia, para perguntar outra vez.
                for chave in etapa.obrigatorios:
                    if chave not in ("TITULO_DA_OBRA", "DIRETOR_OU_CRIADOR"):
                        valores[chave] = ""
                continue

            print("\n" + "─" * 64)
            print(prompt)
            print("─" * 64)
            if _sim("Copiar para a área de transferência? [s/N] "):
                print(
                    "Copiado! 🎬 Cole na conversa com a IA."
                    if _copiar(prompt)
                    else "Não consegui copiar automaticamente — copie o texto acima."
                )
            if _sim(f"Salvar em analises/{slug}/{etapa.arquivo_saida}? [s/N] "):
                destino = Path("analises") / slug / etapa.arquivo_saida
                destino.parent.mkdir(parents=True, exist_ok=True)
                destino.write_text(prompt + "\n", encoding="utf-8")
                print(f"Salvo em {destino}")
    except (EOFError, KeyboardInterrupt):
        print("\n")
    print("Até logo! 🎬 Bons filmes (e séries).")
    return 0


def _flags_da_obra(parser: argparse.ArgumentParser) -> None:
    """Flags de preenchimento compartilhadas por `gerar` e `novo`."""
    parser.add_argument("--titulo", help="Título do filme/série.")
    parser.add_argument("--diretor", help="Diretor(a)/criador(a) da obra.")
    parser.add_argument(
        "--tipo",
        help="Tipo da obra: filme, série/temporada, episódio, documentário... (etapa 0).",
    )
    parser.add_argument("--objetivo", help="Seu objetivo com a análise (etapa 0).")
    parser.add_argument(
        "--nivel", help="Seu nível de familiaridade com análise (etapa 0)."
    )
    parser.add_argument(
        "--impressoes",
        help="Suas impressões/hipóteses iniciais, antes da análise (etapa 0).",
    )
    parser.add_argument(
        "--pergunta", help="Pergunta escolhida na Etapa 2.1 (etapa 2.2)."
    )
    parser.add_argument(
        "--sequencia",
        help="Sequência a dissecar, com minutagem/episódio (etapa 2.3).",
    )
    parser.add_argument("--obra-a", help="Primeira obra da comparação (etapa 4).")
    parser.add_argument("--diretor-a", help="Diretor(a)/criador(a) da obra A (etapa 4).")
    parser.add_argument("--obra-b", help="Segunda obra da comparação (etapa 4).")
    parser.add_argument("--diretor-b", help="Diretor(a)/criador(a) da obra B (etapa 4).")
    parser.add_argument(
        "--eixo",
        help="Eixo da comparação: tema, remake, mesmo diretor... (etapa 4).",
    )
    parser.add_argument(
        "--modo",
        choices=sorted(MODOS_DE_ANALISE),
        default="padrao",
        help="Calibragem do prompt: padrao, iniciante (explica termos) ou academico.",
    )
    parser.add_argument(
        "--dossie",
        help="Metadados, links ou dossiê factual já reunido (etapa R/sessão).",
    )
    parser.add_argument(
        "--dossie-arquivo",
        metavar="arquivo",
        help="Lê o dossiê de fontes de um arquivo Markdown/texto.",
    )


def _flags_da_sessao(parser: argparse.ArgumentParser) -> None:
    """Opções de trilha compartilhadas por `maestro` e `sessao`."""
    parser.add_argument(
        "--trilha",
        choices=sorted(TRILHAS),
        help="Trilha da sessão: padrao, serie, dois-tempos ou comparativa.",
    )
    parser.add_argument(
        "--sem-pesquisa",
        action="store_true",
        help="Não inclui a Etapa R (pesquisa e dossiê de fontes).",
    )
    parser.add_argument(
        "--sem-close-reading",
        action="store_true",
        help="Não inclui a Etapa 2.3 (close reading).",
    )


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="fluxo",
        description=(
            "Fluxo de Prompts Especializado para Análise de Obras "
            "Audiovisuais (filmes e séries) com IA."
        ),
    )
    parser.add_argument("--versao", action="version", version=f"fluxo {__version__}")
    sub = parser.add_subparsers(dest="comando", metavar="comando")

    p_listar = sub.add_parser(
        "listar", help="Lista as etapas do fluxo e o que cada uma requer."
    )
    p_listar.set_defaults(func=cmd_listar)

    p_interativo = sub.add_parser(
        "interativo",
        help="Modo guiado: responde perguntas no terminal e monta os prompts.",
    )
    p_interativo.set_defaults(func=cmd_interativo)

    p_gerar = sub.add_parser(
        "gerar", help="Gera o prompt de uma etapa com os placeholders preenchidos."
    )
    p_gerar.add_argument(
        "etapa",
        help="Etapa desejada: 0, R, 1, 1a, 1b, 1s, 2.1, 2.2, 2.3, 3 ou 4 (veja 'fluxo listar').",
    )
    _flags_da_obra(p_gerar)
    p_gerar.add_argument(
        "--salvar",
        metavar="arquivo",
        help="Salva o prompt no arquivo indicado em vez de imprimir na tela.",
    )
    p_gerar.add_argument(
        "--copiar",
        action="store_true",
        help="Copia o prompt para a área de transferência.",
    )
    p_gerar.set_defaults(func=cmd_gerar)

    p_maestro = sub.add_parser(
        "maestro",
        help="Gera um roteiro único para a IA conduzir todas as etapas na mesma conversa.",
    )
    _flags_da_obra(p_maestro)
    _flags_da_sessao(p_maestro)
    p_maestro.add_argument(
        "--salvar",
        metavar="arquivo",
        help="Salva o Prompt Maestro no arquivo indicado em vez de imprimir.",
    )
    p_maestro.add_argument(
        "--copiar",
        action="store_true",
        help="Copia o Prompt Maestro para a área de transferência.",
    )
    p_maestro.set_defaults(func=cmd_maestro)

    p_sessao = sub.add_parser(
        "sessao",
        help="Cria uma pasta guiada somente com as etapas relevantes da trilha escolhida.",
    )
    _flags_da_obra(p_sessao)
    _flags_da_sessao(p_sessao)
    p_sessao.add_argument("--slug", help="Nome da pasta (padrão: derivado do título).")
    p_sessao.add_argument(
        "--destino", default="analises", help="Pasta base das sessões (padrão: analises)."
    )
    p_sessao.add_argument(
        "--forcar", action="store_true", help="Sobrescreve os arquivos se a pasta já existir."
    )
    p_sessao.set_defaults(func=cmd_sessao)

    p_novo = sub.add_parser(
        "novo",
        help="Cria uma pasta de análise com os prompts de todas as etapas e um registro.",
    )
    _flags_da_obra(p_novo)
    _flags_da_sessao(p_novo)
    # Em `novo`, o título é obrigatório (define a pasta e os arquivos).
    for acao in p_novo._actions:
        if acao.dest == "titulo":
            acao.required = True
    p_novo.add_argument("--slug", help="Nome da pasta (padrão: derivado do título).")
    p_novo.add_argument(
        "--destino", default="analises", help="Pasta base das análises (padrão: analises)."
    )
    p_novo.add_argument(
        "--forcar", action="store_true", help="Sobrescreve os arquivos se a pasta já existir."
    )
    p_novo.set_defaults(func=cmd_novo)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = construir_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except FluxoError as erro:
        print(f"Erro: {erro}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
