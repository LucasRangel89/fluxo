"""Núcleo do Fluxo: carregamento de templates e geração de prompts.

Os templates vivem na pasta ``prompts/`` do repositório, como arquivos
Markdown legíveis por humanos. O texto do prompt em si fica delimitado pelos
marcadores ``<!-- INICIO DO PROMPT -->`` e ``<!-- FIM DO PROMPT -->`` — é esse
trecho que a CLI extrai, preenche e entrega pronto para colar na IA.
"""

from __future__ import annotations

import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path

MARCADOR_INICIO = "<!-- INICIO DO PROMPT -->"
MARCADOR_FIM = "<!-- FIM DO PROMPT -->"

_RE_PLACEHOLDER = re.compile(r"\{\{\s*([A-Z0-9_]+)\s*\}\}")

# Para cada placeholder conhecido: (nome amigável, flag equivalente na CLI).
PLACEHOLDERS: dict[str, tuple[str, str | None]] = {
    "TITULO_DA_OBRA": ("título do filme/série", "--titulo"),
    "DIRETOR_OU_CRIADOR": ("nome do diretor(a)/criador(a)", "--diretor"),
    "PERGUNTA_ESCOLHIDA": ("pergunta escolhida na Etapa 2.1", "--pergunta"),
    "DATA_DA_ANALISE": ("data da análise", None),
}


class FluxoError(Exception):
    """Erro esperado de uso — a mensagem já vem pronta para o usuário."""


@dataclass(frozen=True)
class Etapa:
    """Metadados de uma etapa do fluxo."""

    id: str
    nome: str
    arquivo_template: str
    arquivo_saida: str
    descricao: str
    obrigatorios: tuple[str, ...]


ETAPAS: dict[str, Etapa] = {
    etapa.id: etapa
    for etapa in (
        Etapa(
            id="1",
            nome="Análise Audiovisual 360°",
            arquivo_template="etapa-01-analise-360.md",
            arquivo_saida="01-prompt-analise-360.md",
            descricao="Raio-x completo da obra em 7 dimensões críticas.",
            obrigatorios=("TITULO_DA_OBRA", "DIRETOR_OU_CRIADOR"),
        ),
        Etapa(
            id="2.1",
            nome="Proposta de Aprofundamento Crítico",
            arquivo_template="etapa-02.1-proposta-aprofundamento.md",
            arquivo_saida="02.1-prompt-proposta-aprofundamento.md",
            descricao="A IA propõe de 3 a 5 perguntas analíticas para você escolher.",
            obrigatorios=("TITULO_DA_OBRA",),
        ),
        Etapa(
            id="2.2",
            nome="Execução da Análise Focada",
            arquivo_template="etapa-02.2-analise-focada.md",
            arquivo_saida="02.2-prompt-analise-focada.md",
            descricao="Análise densa da pergunta escolhida: tese, evidências e contexto.",
            obrigatorios=("PERGUNTA_ESCOLHIDA",),
        ),
        Etapa(
            id="3",
            nome="Consolidação, Diálogos e Expansão",
            arquivo_template="etapa-03-sintese-conexoes.md",
            arquivo_saida="03-prompt-sintese-conexoes.md",
            descricao="Síntese final, obras em diálogo, reflexões e fontes para expandir.",
            obrigatorios=("TITULO_DA_OBRA",),
        ),
    )
}

_ALIASES: dict[str, str] = {
    "1": "1", "01": "1", "e1": "1", "etapa1": "1", "etapa-1": "1",
    "etapa01": "1", "etapa-01": "1",
    "2.1": "2.1", "21": "2.1", "2-1": "2.1", "etapa2.1": "2.1", "etapa-2.1": "2.1",
    "2.2": "2.2", "22": "2.2", "2-2": "2.2", "etapa2.2": "2.2", "etapa-2.2": "2.2",
    "3": "3", "03": "3", "e3": "3", "etapa3": "3", "etapa-3": "3",
    "etapa03": "3", "etapa-03": "3",
}


def normalizar_etapa(entrada: str) -> str:
    """Aceita variações como ``01``, ``etapa-2.1`` ou ``22`` e devolve o id canônico."""
    chave = entrada.strip().lower().replace(" ", "")
    try:
        return _ALIASES[chave]
    except KeyError:
        validas = ", ".join(ETAPAS)
        raise FluxoError(
            f"Etapa desconhecida: {entrada!r}. Etapas válidas: {validas}."
        ) from None


def _procurar_para_cima(inicio: Path, relativo: str) -> Path | None:
    atual = inicio.resolve()
    for base in (atual, *atual.parents):
        alvo = base / relativo
        if alvo.exists():
            return alvo
    return None


def encontrar_diretorio_prompts() -> Path:
    """Localiza a pasta ``prompts/`` (env ``FLUXO_PROMPTS_DIR`` ou busca no repo)."""
    env = os.environ.get("FLUXO_PROMPTS_DIR")
    if env:
        caminho = Path(env).expanduser()
        if caminho.is_dir():
            return caminho
        raise FluxoError(f"FLUXO_PROMPTS_DIR não é um diretório válido: {env}")
    for inicio in (Path(__file__).parent, Path.cwd()):
        achado = _procurar_para_cima(inicio, "prompts/etapa-01-analise-360.md")
        if achado is not None:
            return achado.parent
    raise FluxoError(
        "Não encontrei o diretório 'prompts/'. Execute a partir da raiz do "
        "repositório ou defina a variável FLUXO_PROMPTS_DIR."
    )


def encontrar_template_registro() -> Path:
    """Localiza ``templates/registro-de-analise.md``."""
    for inicio in (Path(__file__).parent, Path.cwd()):
        achado = _procurar_para_cima(inicio, "templates/registro-de-analise.md")
        if achado is not None:
            return achado
    raise FluxoError("Não encontrei o arquivo 'templates/registro-de-analise.md'.")


def extrair_prompt(conteudo: str) -> str:
    """Extrai o texto do prompt entre os marcadores de um arquivo-template."""
    if MARCADOR_INICIO not in conteudo or MARCADOR_FIM not in conteudo:
        raise FluxoError(
            "Template sem os marcadores de prompt "
            f"({MARCADOR_INICIO} ... {MARCADOR_FIM})."
        )
    _, _, resto = conteudo.partition(MARCADOR_INICIO)
    prompt, _, _ = resto.partition(MARCADOR_FIM)
    return prompt.strip()


def carregar_template(etapa_id: str, diretorio: Path | None = None) -> str:
    """Lê o arquivo da etapa e devolve apenas o texto do prompt (com placeholders)."""
    etapa = ETAPAS[normalizar_etapa(etapa_id)]
    base = diretorio or encontrar_diretorio_prompts()
    caminho = base / etapa.arquivo_template
    if not caminho.is_file():
        raise FluxoError(f"Template não encontrado: {caminho}")
    return extrair_prompt(caminho.read_text(encoding="utf-8"))


def preencher(template: str, valores: dict[str, str], *, estrito: bool = True) -> str:
    """Substitui os placeholders ``{{CHAVE}}`` pelos valores informados.

    No modo estrito (padrão), qualquer placeholder sem valor gera um
    :class:`FluxoError` indicando o que falta. Fora dele, os trechos pendentes
    viram ``[PREENCHER: CHAVE]`` — útil ao montar a estrutura de uma análise
    antes de conhecer, por exemplo, a pergunta da Etapa 2.2.
    """
    faltando: list[str] = []

    def _substituir(match: re.Match[str]) -> str:
        chave = match.group(1)
        valor = (valores.get(chave) or "").strip()
        if valor:
            return valor
        faltando.append(chave)
        return match.group(0) if estrito else f"[PREENCHER: {chave}]"

    resultado = _RE_PLACEHOLDER.sub(_substituir, template)
    if estrito and faltando:
        detalhes = []
        for chave in dict.fromkeys(faltando):
            nome, flag = PLACEHOLDERS.get(chave, (chave, None))
            detalhes.append(f"{nome} ({flag})" if flag else nome)
        raise FluxoError("Faltam informações obrigatórias: " + "; ".join(detalhes) + ".")
    return resultado


def gerar_prompt(
    etapa_id: str,
    valores: dict[str, str],
    *,
    estrito: bool = True,
    diretorio: Path | None = None,
) -> str:
    """Gera o prompt final de uma etapa, já com os placeholders preenchidos."""
    return preencher(carregar_template(etapa_id, diretorio), valores, estrito=estrito)


def gerar_registro(valores: dict[str, str]) -> str:
    """Preenche o template de registro de análise."""
    caminho = encontrar_template_registro()
    return preencher(caminho.read_text(encoding="utf-8"), valores, estrito=False)


def slugificar(texto: str) -> str:
    """Converte um título em slug de pasta (ex.: ``Cidade de Deus`` -> ``cidade-de-deus``)."""
    normalizado = unicodedata.normalize("NFKD", texto)
    ascii_puro = normalizado.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_puro.lower()).strip("-")
    return slug or "obra-sem-titulo"
