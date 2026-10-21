"""Interface de linha de comando do Fluxo.

Comandos:
    fluxo listar   -> mostra as etapas e o que cada uma requer
    fluxo gerar N  -> gera o prompt da etapa N, pronto para colar na IA
    fluxo novo     -> cria uma pasta de análise com os 4 prompts + registro
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

from . import __version__
from .core import (
    ETAPAS,
    PLACEHOLDERS,
    FluxoError,
    gerar_prompt,
    gerar_registro,
    normalizar_etapa,
    slugificar,
)


def _valores(args: argparse.Namespace) -> dict[str, str]:
    """Mapeia as flags da CLI para os placeholders dos templates."""
    return {
        "TITULO_DA_OBRA": getattr(args, "titulo", "") or "",
        "DIRETOR_OU_CRIADOR": getattr(args, "diretor", "") or "",
        "PERGUNTA_ESCOLHIDA": getattr(args, "pergunta", "") or "",
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
    print(
        'Exemplo: fluxo gerar 1 --titulo "Cidade de Deus (2002)" '
        '--diretor "Fernando Meirelles e Kátia Lund"'
    )
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

    criados: list[str] = []
    for etapa in ETAPAS.values():
        # Modo não-estrito: o que ainda não se sabe (ex.: a pergunta da
        # Etapa 2.2) vira [PREENCHER: ...] dentro do arquivo gerado.
        conteudo = gerar_prompt(etapa.id, valores, estrito=False)
        (pasta / etapa.arquivo_saida).write_text(conteudo + "\n", encoding="utf-8")
        criados.append(etapa.arquivo_saida)

    valores_registro = {**valores, "DATA_DA_ANALISE": date.today().isoformat()}
    (pasta / "registro.md").write_text(gerar_registro(valores_registro), encoding="utf-8")
    criados.append("registro.md")

    print(f"Análise criada em {pasta}/")
    for nome in criados:
        print(f"  - {nome}")
    pendentes = [
        chave
        for chave in ("DIRETOR_OU_CRIADOR", "PERGUNTA_ESCOLHIDA")
        if not valores.get(chave)
    ]
    if pendentes:
        nomes = ", ".join(PLACEHOLDERS[chave][0] for chave in pendentes)
        print(
            f"\nObservação: ficaram pendentes ({nomes}). Complete os trechos "
            "[PREENCHER: ...] nos arquivos gerados quando chegar a hora."
        )
    return 0


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

    p_gerar = sub.add_parser(
        "gerar", help="Gera o prompt de uma etapa com os placeholders preenchidos."
    )
    p_gerar.add_argument("etapa", help="Etapa desejada: 1, 2.1, 2.2 ou 3.")
    p_gerar.add_argument("--titulo", help="Título do filme/série (etapas 1, 2.1 e 3).")
    p_gerar.add_argument("--diretor", help="Diretor(a)/criador(a) da obra (etapa 1).")
    p_gerar.add_argument("--pergunta", help="Pergunta escolhida na Etapa 2.1 (etapa 2.2).")
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

    p_novo = sub.add_parser(
        "novo", help="Cria uma pasta de análise com os 4 prompts e um registro."
    )
    p_novo.add_argument("--titulo", required=True, help="Título do filme/série.")
    p_novo.add_argument("--diretor", help="Diretor(a)/criador(a) da obra.")
    p_novo.add_argument(
        "--pergunta",
        help="Pergunta escolhida (se omitida, fica pendente no arquivo da Etapa 2.2).",
    )
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
