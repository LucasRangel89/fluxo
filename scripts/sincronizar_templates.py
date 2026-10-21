#!/usr/bin/env python3
"""Sincroniza os templates canônicos para dentro do pacote (P17).

A fonte da verdade são os arquivos em ``prompts/`` (e
``templates/registro-de-analise.md``). Este script copia todos eles para
``src/fluxo/_templates/``, que é o fallback usado quando a CLI está
instalada via pip, fora do repositório.

Uso (a partir da raiz do repo):

    python scripts/sincronizar_templates.py

Os testes em ``tests/test_fase4.py`` falham se alguma cópia estiver
diferente do original — editou um template? Rode o script.
"""

from __future__ import annotations

import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "src" / "fluxo" / "_templates"


def main() -> int:
    DESTINO.mkdir(parents=True, exist_ok=True)
    copiados: list[str] = []
    for origem in sorted((RAIZ / "prompts").glob("*.md")):
        shutil.copyfile(origem, DESTINO / origem.name)
        copiados.append(origem.name)
    registro = RAIZ / "templates" / "registro-de-analise.md"
    shutil.copyfile(registro, DESTINO / registro.name)
    copiados.append(registro.name)

    print(f"{len(copiados)} templates sincronizados em {DESTINO.relative_to(RAIZ)}/:")
    for nome in copiados:
        print(f"  - {nome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
