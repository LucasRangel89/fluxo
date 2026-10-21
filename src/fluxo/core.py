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
    "TIPO_DE_OBRA": ("tipo da obra (filme, série/temporada, episódio...)", "--tipo"),
    "META_DA_ANALISE": ("seu objetivo com a análise", "--objetivo"),
    "NIVEL_DO_USUARIO": ("seu nível de familiaridade com análise", "--nivel"),
    "IMPRESSOES_INICIAIS": ("suas impressões/hipóteses iniciais", "--impressoes"),
    "PERGUNTA_ESCOLHIDA": ("pergunta escolhida na Etapa 2.1", "--pergunta"),
    "SEQUENCIA_ESCOLHIDA": ("sequência escolhida para o close reading", "--sequencia"),
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
            id="0",
            nome="Preparação",
            arquivo_template="etapa-00-preparacao.md",
            arquivo_saida="00-prompt-preparacao.md",
            descricao=(
                "Setup opcional: identifica a obra, registra a sua hipótese "
                "antes da IA opinar e calibra objetivo/nível."
            ),
            obrigatorios=(
                "TITULO_DA_OBRA", "DIRETOR_OU_CRIADOR", "TIPO_DE_OBRA",
                "META_DA_ANALISE", "NIVEL_DO_USUARIO", "IMPRESSOES_INICIAIS",
            ),
        ),
        Etapa(
            id="1",
            nome="Análise Audiovisual 360°",
            arquivo_template="etapa-01-analise-360.md",
            arquivo_saida="01-prompt-analise-360.md",
            descricao="Raio-x completo da obra em 7 dimensões críticas, de uma vez.",
            obrigatorios=("TITULO_DA_OBRA", "DIRETOR_OU_CRIADOR"),
        ),
        Etapa(
            id="1a",
            nome="Análise 360° — O Texto (1º tempo)",
            arquivo_template="etapa-01a-analise-texto.md",
            arquivo_saida="01a-prompt-analise-360-texto.md",
            descricao=(
                "Alternativa à Etapa 1 em dois tempos: dimensões 2 a 5 "
                "(narrativa, imagem, som e montagem)."
            ),
            obrigatorios=("TITULO_DA_OBRA", "DIRETOR_OU_CRIADOR"),
        ),
        Etapa(
            id="1b",
            nome="Análise 360° — O Contexto (2º tempo)",
            arquivo_template="etapa-01b-analise-contexto.md",
            arquivo_saida="01b-prompt-analise-360-contexto.md",
            descricao=(
                "Segundo tempo: dimensões 1, 6 e 7 (produção, sociocultural e "
                "recepção) + tabela-resumo completa das 7."
            ),
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
            descricao=(
                "Análise densa da pergunta escolhida: tese, evidências, "
                "contra-argumento e contexto."
            ),
            obrigatorios=("PERGUNTA_ESCOLHIDA",),
        ),
        Etapa(
            id="2.3",
            nome="Close Reading de uma Sequência",
            arquivo_template="etapa-02.3-close-reading.md",
            arquivo_saida="02.3-prompt-close-reading.md",
            descricao=(
                "Opcional: disseca uma sequência plano a plano — decupagem, "
                "mise-en-scène, montagem e sentido."
            ),
            obrigatorios=("TITULO_DA_OBRA", "SEQUENCIA_ESCOLHIDA"),
        ),
        Etapa(
            id="3",
            nome="Consolidação, Diálogos e Expansão",
            arquivo_template="etapa-03-sintese-conexoes.md",
            arquivo_saida="03-prompt-sintese-conexoes.md",
            descricao=(
                "Síntese final, balanço crítico, obras em diálogo, reflexões "
                "(incl. sua hipótese inicial) e fontes."
            ),
            obrigatorios=("TITULO_DA_OBRA",),
        ),
    )
}

_ALIASES: dict[str, str] = {
    "0": "0", "00": "0", "e0": "0", "etapa0": "0", "etapa-0": "0",
    "etapa00": "0", "etapa-00": "0", "setup": "0", "preparacao": "0",
    "1": "1", "01": "1", "e1": "1", "etapa1": "1", "etapa-1": "1",
    "etapa01": "1", "etapa-01": "1",
    "1a": "1a", "01a": "1a", "1-a": "1a", "e1a": "1a", "etapa1a": "1a",
    "etapa-1a": "1a", "texto": "1a",
    "1b": "1b", "01b": "1b", "1-b": "1b", "e1b": "1b", "etapa1b": "1b",
    "etapa-1b": "1b", "contexto": "1b",
    "2.1": "2.1", "21": "2.1", "2-1": "2.1", "etapa2.1": "2.1", "etapa-2.1": "2.1",
    "2.2": "2.2", "22": "2.2", "2-2": "2.2", "etapa2.2": "2.2", "etapa-2.2": "2.2",
    "2.3": "2.3", "23": "2.3", "2-3": "2.3", "etapa2.3": "2.3", "etapa-2.3": "2.3",
    "close-reading": "2.3", "closereading": "2.3", "close": "2.3",
    "3": "3", "03": "3", "e3": "3", "etapa3": "3", "etapa-3": "3",
    "etapa03": "3", "etapa-03": "3",
}


def normalizar_etapa(entrada: str) -> str:
    """Aceita variações como ``00``, ``etapa-1a`` ou ``close`` e devolve o id canônico."""
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
