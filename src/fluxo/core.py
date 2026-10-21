"""Núcleo do Fluxo: carregamento de templates e geração de prompts.

Os templates vivem na pasta ``prompts/`` do repositório, como arquivos
Markdown legíveis por humanos. O texto do prompt em si fica delimitado pelos
marcadores ``<!-- INICIO DO PROMPT -->`` e ``<!-- FIM DO PROMPT -->`` — é esse
trecho que a CLI extrai, preenche e entrega pronto para colar na IA.

Quando a CLI está instalada fora do repositório, ela usa as cópias
empacotadas em ``fluxo/_templates/`` (mantidas em dia por
``scripts/sincronizar_templates.py`` e verificadas por testes).
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

_DIR_EMPACOTADO = Path(__file__).parent / "_templates"

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
    "OBRA_A": ("primeira obra da comparação (com ano)", "--obra-a"),
    "DIRETOR_A": ("diretor(a)/criador(a) da primeira obra", "--diretor-a"),
    "OBRA_B": ("segunda obra da comparação (com ano)", "--obra-b"),
    "DIRETOR_B": ("diretor(a)/criador(a) da segunda obra", "--diretor-b"),
    "EIXO_DE_COMPARACAO": ("eixo da comparação (tema, remake, mesmo diretor...)", "--eixo"),
    "MODO_DE_ANALISE": ("modo de análise (opcional)", "--modo"),
    "DOSSE_DE_FONTES": ("dossiê, metadados e pistas de fontes (opcional)", "--dossie"),
    "DATA_DA_ANALISE": ("data da análise", None),
}

# Placeholders que podem faltar sem erro: viram "" na substituição.
OPCIONAIS: frozenset[str] = frozenset({"MODO_DE_ANALISE", "DOSSE_DE_FONTES"})

# Instrução injetada nos prompts de abertura conforme o modo (--modo).
MODOS_DE_ANALISE: dict[str, str] = {
    "padrao": "",
    "iniciante": (
        "Calibragem (modo iniciante): explique cada termo técnico na primeira "
        "vez que ele aparecer, entre parênteses e em linguagem simples; "
        "prefira exemplos concretos a conceitos abstratos e não pressuponha "
        "repertório de teoria do cinema."
    ),
    "academico": (
        "Calibragem (modo acadêmico): use registro acadêmico e o vocabulário "
        "técnico sem simplificações; ao mobilizar teoria do cinema, nomeie "
        "autores e conceitos (sem inventar referências); problematize "
        "consensos e aponte os debates em aberto."
    ),
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
            id="r",
            nome="Pesquisa e Dossiê de Fontes",
            arquivo_template="etapa-00r-pesquisa-fontes.md",
            arquivo_saida="00r-prompt-pesquisa-fontes.md",
            descricao=(
                "Etapa opcional de pesquisa: reúne fatos verificáveis, fontes "
                "e incertezas antes da interpretação."
            ),
            obrigatorios=(
                "TITULO_DA_OBRA", "DIRETOR_OU_CRIADOR", "TIPO_DE_OBRA",
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
            id="1s",
            nome="Análise 360° de Série/Temporada",
            arquivo_template="etapa-01s-analise-serie.md",
            arquivo_saida="01s-prompt-analise-360-serie.md",
            descricao=(
                "Variante da Etapa 1 para séries: arcos em 3 níveis, piloto, "
                "showrunner, modelo de exibição e episódio-síntese."
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
        Etapa(
            id="4",
            nome="Análise Comparativa (duas obras)",
            arquivo_template="etapa-04-comparativa.md",
            arquivo_saida="04-prompt-comparativa.md",
            descricao=(
                "Variante: duas obras frente a frente sob um eixo (remake, "
                "mesmo diretor, mesmo tema) + tabela comparativa."
            ),
            obrigatorios=(
                "OBRA_A", "DIRETOR_A", "OBRA_B", "DIRETOR_B", "EIXO_DE_COMPARACAO",
            ),
        ),
    )
}

_ALIASES: dict[str, str] = {
    "0": "0", "00": "0", "e0": "0", "etapa0": "0", "etapa-0": "0",
    "etapa00": "0", "etapa-00": "0", "setup": "0", "preparacao": "0",
    "r": "r", "0r": "r", "00r": "r", "er": "r", "etapar": "r",
    "etapa-r": "r", "pesquisa": "r", "fontes": "r", "dossie": "r",
    "dossiê": "r", "research": "r",
    "1": "1", "01": "1", "e1": "1", "etapa1": "1", "etapa-1": "1",
    "etapa01": "1", "etapa-01": "1",
    "1a": "1a", "01a": "1a", "1-a": "1a", "e1a": "1a", "etapa1a": "1a",
    "etapa-1a": "1a", "texto": "1a",
    "1b": "1b", "01b": "1b", "1-b": "1b", "e1b": "1b", "etapa1b": "1b",
    "etapa-1b": "1b", "contexto": "1b",
    "1s": "1s", "01s": "1s", "1-s": "1s", "e1s": "1s", "etapa1s": "1s",
    "etapa-1s": "1s", "serie": "1s", "series": "1s", "temporada": "1s",
    "2.1": "2.1", "21": "2.1", "2-1": "2.1", "etapa2.1": "2.1", "etapa-2.1": "2.1",
    "2.2": "2.2", "22": "2.2", "2-2": "2.2", "etapa2.2": "2.2", "etapa-2.2": "2.2",
    "2.3": "2.3", "23": "2.3", "2-3": "2.3", "etapa2.3": "2.3", "etapa-2.3": "2.3",
    "close-reading": "2.3", "closereading": "2.3", "close": "2.3",
    "3": "3", "03": "3", "e3": "3", "etapa3": "3", "etapa-3": "3",
    "etapa03": "3", "etapa-03": "3",
    "4": "4", "04": "4", "e4": "4", "etapa4": "4", "etapa-4": "4",
    "etapa04": "4", "etapa-04": "4", "comparativa": "4", "comparacao": "4",
}


def normalizar_etapa(entrada: str) -> str:
    """Aceita variações como ``00``, ``serie`` ou ``close`` e devolve o id canônico."""
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
    """Localiza os templates: env, repositório ou cópias empacotadas no pacote."""
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
    # Instalação via pip, fora do repositório: templates empacotados.
    if (_DIR_EMPACOTADO / "etapa-01-analise-360.md").is_file():
        return _DIR_EMPACOTADO
    raise FluxoError(
        "Não encontrei os templates de prompt. Execute a partir da raiz do "
        "repositório ou defina a variável FLUXO_PROMPTS_DIR."
    )


def encontrar_template_registro() -> Path:
    """Localiza ``registro-de-analise.md`` (repositório ou pacote)."""
    for inicio in (Path(__file__).parent, Path.cwd()):
        achado = _procurar_para_cima(inicio, "templates/registro-de-analise.md")
        if achado is not None:
            return achado
    empacotado = _DIR_EMPACOTADO / "registro-de-analise.md"
    if empacotado.is_file():
        return empacotado
    raise FluxoError("Não encontrei o template de registro de análise.")


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


def placeholders_do_template(
    etapa_id: str, diretorio: Path | None = None
) -> list[str]:
    """Lista, em ordem de aparição, os placeholders usados pelo template da etapa."""
    template = carregar_template(etapa_id, diretorio)
    return list(dict.fromkeys(_RE_PLACEHOLDER.findall(template)))


def preencher(template: str, valores: dict[str, str], *, estrito: bool = True) -> str:
    """Substitui os placeholders ``{{CHAVE}}`` pelos valores informados.

    No modo estrito (padrão), qualquer placeholder obrigatório sem valor gera
    um :class:`FluxoError` indicando o que falta; os opcionais (ver
    ``OPCIONAIS``) viram texto vazio. Fora do modo estrito, os obrigatórios
    pendentes viram ``[PREENCHER: CHAVE]`` — útil ao montar a estrutura de uma
    análise antes de conhecer, por exemplo, a pergunta da Etapa 2.2.
    """
    faltando: list[str] = []

    def _substituir(match: re.Match[str]) -> str:
        chave = match.group(1)
        valor = (valores.get(chave) or "").strip()
        if valor:
            return valor
        if chave in OPCIONAIS:
            return ""
        faltando.append(chave)
        return match.group(0) if estrito else f"[PREENCHER: {chave}]"

    resultado = _RE_PLACEHOLDER.sub(_substituir, template)
    if estrito and faltando:
        detalhes = []
        for chave in dict.fromkeys(faltando):
            nome, flag = PLACEHOLDERS.get(chave, (chave, None))
            detalhes.append(f"{nome} ({flag})" if flag else nome)
        raise FluxoError("Faltam informações obrigatórias: " + "; ".join(detalhes) + ".")
    # Placeholders opcionais vazios não devem deixar buracos no texto.
    return re.sub(r"\n{3,}", "\n\n", resultado)


def gerar_prompt(
    etapa_id: str,
    valores: dict[str, str],
    *,
    estrito: bool = True,
    diretorio: Path | None = None,
) -> str:
    """Gera o prompt final de uma etapa, já com os placeholders preenchidos."""
    return preencher(carregar_template(etapa_id, diretorio), valores, estrito=estrito)


TRILHAS: dict[str, tuple[str, ...]] = {
    "padrao": ("0", "1", "2.1", "2.2", "2.3", "3"),
    "serie": ("0", "1s", "2.1", "2.2", "2.3", "3"),
    "dois-tempos": ("0", "1a", "1b", "2.1", "2.2", "2.3", "3"),
    "comparativa": ("4",),
}

_ALIASES_TRILHA: dict[str, str] = {
    "padrao": "padrao",
    "filme": "padrao",
    "padrao-filme": "padrao",
    "serie": "serie",
    "series": "serie",
    "temporada": "serie",
    "doistempos": "dois-tempos",
    "dois-tempos": "dois-tempos",
    "dois": "dois-tempos",
    "comparativa": "comparativa",
    "comparacao": "comparativa",
}


def normalizar_trilha(entrada: str | None) -> str:
    """Normaliza o nome de uma trilha de sessão (ex.: ``série`` -> ``serie``)."""
    bruto = (entrada or "padrao").strip().lower().replace(" ", "-")
    sem_acento = unicodedata.normalize("NFKD", bruto).encode(
        "ascii", "ignore"
    ).decode("ascii")
    try:
        return _ALIASES_TRILHA[sem_acento]
    except KeyError:
        validas = ", ".join(TRILHAS)
        raise FluxoError(
            f"Trilha desconhecida: {entrada!r}. Trilhas válidas: {validas}."
        ) from None


def etapas_da_sessao(
    trilha: str = "padrao",
    *,
    incluir_pesquisa: bool = True,
    incluir_close_reading: bool = True,
) -> list[str]:
    """Retorna, em ordem, as etapas relevantes para uma sessão guiada."""
    canonica = normalizar_trilha(trilha)
    etapas = list(TRILHAS[canonica])
    if incluir_pesquisa:
        posicao = 1 if etapas and etapas[0] == "0" else 0
        etapas.insert(posicao, "r")
    if not incluir_close_reading and "2.3" in etapas:
        etapas.remove("2.3")
    return etapas


def _valores_para_etapa_da_sessao(
    etapa_id: str, valores: dict[str, str], trilha: str
) -> dict[str, str]:
    """Adapta os valores da sessão a etapas com outro enquadramento.

    A pesquisa comparativa usa o template genérico da Etapa R; por isso, as
    duas obras viram temporariamente o ``TITULO_DA_OBRA`` daquela geração.
    """
    resultado = dict(valores)
    if etapa_id == "r" and normalizar_trilha(trilha) == "comparativa":
        obra_a = (valores.get("OBRA_A") or "").strip()
        obra_b = (valores.get("OBRA_B") or "").strip()
        if obra_a or obra_b:
            resultado["TITULO_DA_OBRA"] = " × ".join(
                trecho for trecho in (obra_a, obra_b) if trecho
            )
        diretor_a = (valores.get("DIRETOR_A") or "").strip()
        diretor_b = (valores.get("DIRETOR_B") or "").strip()
        criadores = []
        if diretor_a:
            criadores.append(f"{obra_a or 'Obra A'}: {diretor_a}")
        if diretor_b:
            criadores.append(f"{obra_b or 'Obra B'}: {diretor_b}")
        if criadores:
            resultado["DIRETOR_OU_CRIADOR"] = "; ".join(criadores)
        eixo = (valores.get("EIXO_DE_COMPARACAO") or "").strip()
        resultado["TIPO_DE_OBRA"] = (
            "Análise comparativa entre duas obras audiovisuais"
            + (f"; eixo: {eixo}" if eixo else "")
        )
    return resultado


def _limpar_markdown(texto: str) -> str:
    limpo = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", texto)
    limpo = limpo.replace("**", "").replace("__", "").replace("`", "")
    limpo = re.sub(r"^\s*(?:>\s*|#{1,6}\s*)", "", limpo)
    limpo = re.sub(r"^\s*(?:\d+[.)]|[-*•])\s+", "", limpo)
    return re.sub(r"\s+", " ", limpo).strip()


def _unicos(textos: list[str], *, limite: int = 8) -> list[str]:
    vistos: set[str] = set()
    resultado: list[str] = []
    for texto in textos:
        chave = texto.casefold()
        if texto and chave not in vistos:
            vistos.add(chave)
            resultado.append(texto)
        if len(resultado) >= limite:
            break
    return resultado


def extrair_perguntas(resposta: str) -> list[str]:
    """Extrai perguntas selecionáveis de uma resposta da Etapa 2.1.

    Prioriza linhas ``PERGUNTA:`` geradas para importação pelo Fluxo e cai
    para listas numeradas/com marcadores quando a resposta veio de outro
    prompt ou foi editada pela IA.
    """
    explicitas = [
        _limpar_markdown(match.group(1))
        for match in re.finditer(
            r"(?im)^\s*(?:[-*•]\s*)?PERGUNTA\s*:\s*(.+)$", resposta
        )
    ]
    if explicitas:
        return _unicos([item for item in explicitas if len(item) >= 10])

    itens: list[str] = []
    atual: list[str] = []
    for linha in resposta.splitlines():
        if re.match(r"^\s*(?:\d+[.)]|[-*•])\s+", linha):
            if atual:
                itens.append(" ".join(atual))
            atual = [linha.strip()]
        elif atual and linha.strip():
            atual.append(linha.strip())
    if atual:
        itens.append(" ".join(atual))
    if not itens:
        itens = [trecho.strip() for trecho in re.split(r"\n\s*\n", resposta)]

    perguntas: list[str] = []
    for item in itens:
        limpo = _limpar_markdown(item)
        if "?" not in limpo:
            continue
        pergunta = limpo.split("?", 1)[0].strip() + "?"
        # Formatos como "Forma: Como a câmera...?" guardam a pergunta após ":".
        if ":" in pergunta:
            prefixo, _, resto = pergunta.partition(":")
            if 0 < len(prefixo) <= 70 and len(resto.strip()) >= 12:
                pergunta = resto.strip()
        if len(pergunta) >= 12:
            perguntas.append(pergunta)
    return _unicos(perguntas)


def extrair_sequencias_sugeridas(resposta: str) -> list[str]:
    """Extrai sugestões de sequência para alimentar a Etapa 2.3."""
    explicitas = [
        _limpar_markdown(match.group(1))
        for match in re.finditer(
            r"(?im)^\s*(?:[-*•]\s*)?SEQU[ÊE]NCIA(?:_SUGERIDA)?\s*:\s*(.+)$",
            resposta,
        )
    ]
    if explicitas:
        return _unicos([item for item in explicitas if len(item) >= 8], limite=5)

    sugestoes: list[str] = []
    padrao_tempo = re.compile(r"(?:\b\d{1,2}:\d{2}(?::\d{2})?\b|\bT\d+\s*:\s*E\d+\b)", re.I)
    palavras = ("sequência", "sequencia", "cena", "abertura", "clímax", "climax", "desfecho")
    for linha in resposta.splitlines():
        limpa = _limpar_markdown(linha)
        if padrao_tempo.search(limpa) and any(
            palavra in limpa.casefold() for palavra in palavras
        ):
            sugestoes.append(limpa[:260])
    return _unicos(sugestoes, limite=5)


def extrair_resumo_da_resposta(resposta: str) -> str:
    """Extrai um resumo curto de continuidade de uma resposta salva."""
    match = re.search(r"(?im)^\s*(?:[-*•]\s*)?RESUMO\s*:\s*(.+)$", resposta)
    if match:
        return _limpar_markdown(match.group(1))[:700]
    for paragrafo in re.split(r"\n\s*\n", resposta):
        limpo = _limpar_markdown(paragrafo)
        if len(limpo) >= 50 and not limpo.casefold().startswith("dados para o fluxo"):
            return limpo[:700]
    return ""


def extrair_fontes(resposta: str) -> list[str]:
    """Extrai linhas de fontes e URLs citadas em uma resposta."""
    fontes = [
        _limpar_markdown(match.group(1))
        for match in re.finditer(r"(?im)^\s*(?:[-*•]\s*)?FONTE\s*:\s*(.+)$", resposta)
    ]
    fontes.extend(re.findall(r"https?://[^\s)\]]+", resposta))
    return _unicos(fontes, limite=20)


def extrair_dados_da_resposta(resposta: str) -> dict[str, object]:
    """Estrutura os dados importáveis de uma resposta de qualquer etapa."""
    return {
        "resumo": extrair_resumo_da_resposta(resposta),
        "perguntas": extrair_perguntas(resposta),
        "sequencias_sugeridas": extrair_sequencias_sugeridas(resposta),
        "fontes": extrair_fontes(resposta),
    }


def _instrucao_dados_fluxo(etapa_id: str) -> str:
    linhas = [
        "",
        "---",
        "Instrução de continuidade do Fluxo: ao final da resposta principal, "
        "acrescente uma seção curta intitulada `## Dados para o Fluxo`, com:",
        "- RESUMO: até 3 frases com os achados que precisam ser lembrados nas próximas etapas.",
    ]
    if etapa_id == "2.1":
        linhas.append(
            "- Uma linha `PERGUNTA:` para cada pergunta proposta, apenas com a pergunta."
        )
    if etapa_id in ("1", "1a", "1b", "1s"):
        linhas.append(
            "- Até 3 linhas `SEQUENCIA_SUGERIDA:` com sequências férteis para close reading, incluindo minutagem ou episódio quando tiver confiança."
        )
    if etapa_id in ("r", "3"):
        linhas.append(
            "- Uma linha `FONTE:` para cada fonte essencial realmente consultada ou recomendada, sem inventar URLs."
        )
    linhas.append(
        "Não deixe essa seção substituir nem resumir a análise pedida acima."
    )
    return "\n".join(linhas)


def gerar_prompt_sessao(
    etapa_id: str,
    valores: dict[str, str],
    *,
    trilha: str = "padrao",
    respostas: dict[str, str] | None = None,
    incluir_contexto: bool = False,
    incluir_dados_fluxo: bool = True,
    incluir_dossie: bool = True,
    diretorio: Path | None = None,
) -> str:
    """Gera um prompt contextualizado para uso dentro de uma sessão guiada."""
    canonica = normalizar_etapa(etapa_id)
    valores_etapa = _valores_para_etapa_da_sessao(canonica, valores, trilha)
    prompt = gerar_prompt(
        canonica, valores_etapa, estrito=False, diretorio=diretorio
    )

    dossie = (valores.get("DOSSE_DE_FONTES") or "").strip()
    if incluir_dossie and dossie and canonica in ("1", "1a", "1b", "1s", "2.2", "3", "4"):
        prompt += (
            "\n\n---\n"
            "Contexto factual e fontes reunidos na sessão (use para fatos "
            "externos; não substitui as evidências formais da própria obra):\n\n"
            + dossie[:10000]
        )

    if incluir_contexto and respostas:
        trechos: list[str] = []
        for anterior in etapas_da_sessao(
            trilha, incluir_pesquisa=True, incluir_close_reading=True
        ):
            if anterior == canonica:
                break
            resposta = (respostas.get(anterior) or "").strip()
            if not resposta:
                continue
            resumo = extrair_resumo_da_resposta(resposta) or resposta[:1800]
            trechos.append(f"### Etapa {anterior}\n{resumo}")
        if trechos:
            prompt += (
                "\n\n---\n"
                "Pacote de continuidade da sessão (resumo do que já foi "
                "levantado; use como contexto, sem repetir tudo):\n\n"
                + "\n\n".join(trechos)[:12000]
            )

    if incluir_dados_fluxo:
        prompt += "\n" + _instrucao_dados_fluxo(canonica)
    return prompt


def gerar_prompt_maestro(
    valores: dict[str, str],
    *,
    trilha: str = "padrao",
    incluir_pesquisa: bool = True,
    incluir_close_reading: bool = True,
    diretorio: Path | None = None,
) -> str:
    """Monta um único roteiro para a IA conduzir a sessão inteira no chat."""
    canonica = normalizar_trilha(trilha)
    ordem = etapas_da_sessao(
        canonica,
        incluir_pesquisa=incluir_pesquisa,
        incluir_close_reading=incluir_close_reading,
    )
    dossie = (valores.get("DOSSE_DE_FONTES") or "").strip()
    valores_prompts = dict(valores)
    valores_prompts["DOSSE_DE_FONTES"] = ""
    if canonica == "comparativa":
        foco = " × ".join(
            trecho
            for trecho in (
                (valores.get("OBRA_A") or "").strip(),
                (valores.get("OBRA_B") or "").strip(),
            )
            if trecho
        ) or "[duas obras a comparar]"
    else:
        foco = (valores.get("TITULO_DA_OBRA") or "[obra]").strip()

    partes = [
        "# Sessão guiada do Fluxo — Prompt Maestro",
        "",
        f"Você será o condutor de uma análise completa de **{foco}**, usando "
        "os roteiros abaixo **um de cada vez, nesta ordem**. Não execute todas "
        "as etapas em uma única resposta.",
        "",
        "## Como conduzir",
        "",
        "1. Comece somente pela primeira etapa do roteiro e pare ao concluí-la, "
        "dizendo qual é a próxima etapa.",
        "2. Quando eu responder “continue”, avance para a etapa seguinte sem "
        "pedir que eu cole outro prompt.",
        "3. Na Etapa 2.1, pare obrigatoriamente e espere eu escolher uma "
        "pergunta (ou formular a minha). Use exatamente essa escolha na 2.2.",
        "4. Antes da Etapa 2.3, se ela estiver no roteiro, pergunte qual "
        "sequência quero dissecar ou ofereça opções concretas.",
        "5. Mantenha as regras de rigor de cada roteiro durante toda a "
        "conversa. Diferencie fato de interpretação e marque incertezas.",
        "6. Ao fim de cada etapa, acrescente `## Dados para o Fluxo` com um "
        "item `RESUMO:`; na 2.1, repita cada opção em uma linha `PERGUNTA:`; "
        "nas análises 360°, sugira até 3 linhas `SEQUENCIA_SUGERIDA:`.",
        "7. Não pule a minha hipótese inicial: ela deve ser registrada antes "
        "da sua interpretação e retomada na síntese.",
    ]
    if dossie:
        partes.extend(
            [
                "",
                "## Dossiê factual já reunido",
                "",
                "Use este material para fatos externos, verificando conflitos; "
                "ele não substitui evidências da obra:",
                "",
                dossie[:10000],
            ]
        )

    substituicoes = {
        "[PREENCHER: PERGUNTA_ESCOLHIDA]": (
            "a pergunta que eu escolher quando você pausar após a Etapa 2.1"
        ),
        "[PREENCHER: SEQUENCIA_ESCOLHIDA]": (
            "a sequência que combinarmos na pausa anterior à Etapa 2.3"
        ),
    }
    for etapa_id in ordem:
        etapa = ETAPAS[etapa_id]
        prompt = gerar_prompt_sessao(
            etapa_id,
            valores_prompts,
            trilha=canonica,
            incluir_contexto=False,
            incluir_dados_fluxo=False,
            incluir_dossie=False,
            diretorio=diretorio,
        )
        for pendente, texto in substituicoes.items():
            prompt = prompt.replace(pendente, texto)
        partes.extend(
            [
                "",
                "---",
                "",
                f"## Roteiro — Etapa {etapa_id}: {etapa.nome}",
                "",
                prompt,
            ]
        )

    partes.extend(
        [
            "",
            "---",
            "",
            "Comece agora apenas pela primeira etapa do roteiro.",
        ]
    )
    return "\n".join(partes).strip()


def criar_manifesto_sessao(
    valores: dict[str, str],
    *,
    trilha: str = "padrao",
    incluir_pesquisa: bool = True,
    incluir_close_reading: bool = True,
) -> dict[str, object]:
    """Cria o manifesto serializável de uma sessão guiada."""
    ordem = etapas_da_sessao(
        trilha,
        incluir_pesquisa=incluir_pesquisa,
        incluir_close_reading=incluir_close_reading,
    )
    return {
        "versao": 1,
        "trilha": normalizar_trilha(trilha),
        "campos": {
            chave: valores.get(chave, "")
            for chave in PLACEHOLDERS
            if chave != "DATA_DA_ANALISE"
        },
        "etapas": [
            {
                "id": etapa.id,
                "nome": etapa.nome,
                "prompt": etapa.arquivo_saida,
                "status": "pendente",
                "resposta": "",
            }
            for etapa in (ETAPAS[etapa_id] for etapa_id in ordem)
        ],
    }


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
