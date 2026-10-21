"""Testes da Fase 5: sessão guiada, Prompt Maestro, pesquisa e importação."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from fluxo.cli import main
from fluxo.core import (
    criar_manifesto_sessao,
    etapas_da_sessao,
    extrair_dados_da_resposta,
    extrair_perguntas,
    extrair_sequencias_sugeridas,
    gerar_prompt,
    gerar_prompt_maestro,
    gerar_prompt_sessao,
    normalizar_etapa,
    normalizar_trilha,
)

RAIZ = Path(__file__).resolve().parents[1]

VALORES = {
    "TITULO_DA_OBRA": "Cidade de Deus (2002)",
    "DIRETOR_OU_CRIADOR": "Fernando Meirelles e Kátia Lund",
    "TIPO_DE_OBRA": "Filme (longa-metragem de ficção)",
    "META_DA_ANALISE": "Estudar um clássico brasileiro",
    "NIVEL_DO_USUARIO": "Intermediário",
    "IMPRESSOES_INICIAIS": "Achei a violência espetacularizada demais.",
    "PERGUNTA_ESCOLHIDA": "Como a montagem constrói o ciclo de violência?",
    "SEQUENCIA_ESCOLHIDA": "A abertura: perseguição ao frango (≈0:00–3:30)",
    "OBRA_A": "Cidade de Deus (2002)",
    "DIRETOR_A": "Fernando Meirelles e Kátia Lund",
    "OBRA_B": "Tropa de Elite (2007)",
    "DIRETOR_B": "José Padilha",
    "EIXO_DE_COMPARACAO": "Duas visões da violência urbana brasileira",
    "DOSSE_DE_FONTES": "Ficha inicial consultada em bases abertas.",
}


def executar(*args: str) -> tuple[int, str, str]:
    saida, erros = io.StringIO(), io.StringIO()
    with redirect_stdout(saida), redirect_stderr(erros):
        codigo = main(list(args))
    return codigo, saida.getvalue(), erros.getvalue()


class TestEtapaPesquisa(unittest.TestCase):
    def test_aliases_e_conteudo(self):
        for entrada in ("r", "R", "00r", "pesquisa", "fontes", "dossie"):
            with self.subTest(entrada=entrada):
                self.assertEqual(normalizar_etapa(entrada), "r")
        prompt = gerar_prompt("r", VALORES)
        self.assertIn("ainda **não faça a análise crítica**", prompt.lower())
        self.assertIn("Fontes consultadas", prompt)
        self.assertIn("(a confirmar)", prompt)
        self.assertIn(VALORES["DOSSE_DE_FONTES"], prompt)
        self.assertNotIn("{{", prompt)

    def test_dossie_e_opcional(self):
        valores = {k: v for k, v in VALORES.items() if k != "DOSSE_DE_FONTES"}
        prompt = gerar_prompt("pesquisa", valores)
        self.assertTrue(prompt.strip())
        self.assertNotIn("{{DOSSE_DE_FONTES}}", prompt)


class TestTrilhas(unittest.TestCase):
    def test_normalizacao(self):
        self.assertEqual(normalizar_trilha("série"), "serie")
        self.assertEqual(normalizar_trilha("filme"), "padrao")
        self.assertEqual(normalizar_trilha("comparação"), "comparativa")

    def test_ordem_das_sessoes(self):
        self.assertEqual(
            etapas_da_sessao("padrao"),
            ["0", "r", "1", "2.1", "2.2", "2.3", "3"],
        )
        self.assertEqual(
            etapas_da_sessao("serie", incluir_pesquisa=False),
            ["0", "1s", "2.1", "2.2", "2.3", "3"],
        )
        self.assertEqual(
            etapas_da_sessao("comparativa"),
            ["r", "4"],
        )
        self.assertNotIn(
            "2.3", etapas_da_sessao("dois-tempos", incluir_close_reading=False)
        )


class TestSessaoEMaestro(unittest.TestCase):
    def test_prompt_da_sessao_inclui_dossie_e_dados_importaveis(self):
        prompt = gerar_prompt_sessao("1", VALORES)
        self.assertIn("Contexto factual e fontes reunidos na sessão", prompt)
        self.assertIn("## Dados para o Fluxo", prompt)
        self.assertIn("SEQUENCIA_SUGERIDA", prompt)

    def test_maestro_conduz_em_pausas_e_nao_vaza_placeholder_dinamico(self):
        valores = {
            k: v
            for k, v in VALORES.items()
            if k not in ("PERGUNTA_ESCOLHIDA", "SEQUENCIA_ESCOLHIDA")
        }
        maestro = gerar_prompt_maestro(valores, trilha="padrao")
        self.assertIn("Prompt Maestro", maestro)
        self.assertIn("Não execute todas as etapas em uma única resposta", maestro)
        self.assertIn("a pergunta que eu escolher quando você pausar", maestro)
        self.assertIn("## Roteiro — Etapa 2.1", maestro)
        self.assertIn("## Roteiro — Etapa 3", maestro)
        self.assertIn(VALORES["DOSSE_DE_FONTES"], maestro)
        self.assertNotIn("[PREENCHER: PERGUNTA_ESCOLHIDA]", maestro)
        self.assertNotIn("[PREENCHER: SEQUENCIA_ESCOLHIDA]", maestro)
        self.assertNotIn("{{", maestro)

    def test_maestro_comparativo_usa_pesquisa_adaptada(self):
        maestro = gerar_prompt_maestro(VALORES, trilha="comparativa")
        self.assertIn("Cidade de Deus (2002) × Tropa de Elite (2007)", maestro)
        self.assertIn("## Roteiro — Etapa r", maestro)
        self.assertIn("## Roteiro — Etapa 4", maestro)
        self.assertNotIn("## Roteiro — Etapa 1:", maestro)

    def test_manifesto_da_sessao(self):
        manifesto = criar_manifesto_sessao(VALORES, trilha="serie")
        self.assertEqual(manifesto["trilha"], "serie")
        self.assertEqual(manifesto["etapas"][2]["id"], "1s")
        self.assertEqual(manifesto["campos"]["TITULO_DA_OBRA"], VALORES["TITULO_DA_OBRA"])


class TestImportacaoDeRespostas(unittest.TestCase):
    def test_extrai_linhas_estruturadas(self):
        resposta = """Análise longa.

## Dados para o Fluxo
- RESUMO: A forma acelerada transforma violência em espetáculo.
- PERGUNTA: Como a montagem constrói o ciclo de violência?
- PERGUNTA: Qual é a posição ética do olhar de Buscapé?
- SEQUENCIA_SUGERIDA: A abertura completa (≈0:00–3:30)
- FONTE: Artigo consultado — https://example.org/artigo
"""
        dados = extrair_dados_da_resposta(resposta)
        self.assertIn("forma acelerada", str(dados["resumo"]))
        self.assertEqual(len(dados["perguntas"]), 2)  # type: ignore[arg-type]
        self.assertIn("A abertura completa", dados["sequencias_sugeridas"][0])  # type: ignore[index]
        self.assertTrue(any("example.org" in fonte for fonte in dados["fontes"]))  # type: ignore[union-attr]

    def test_extrai_perguntas_de_lista_comum(self):
        resposta = """1. **Forma:** Como a montagem transforma a violência em espetáculo? Esta é a justificativa.
2. **Tema:** Até que ponto Buscapé escapa do ciclo que narra? Outra justificativa.
"""
        perguntas = extrair_perguntas(resposta)
        self.assertEqual(
            perguntas,
            [
                "Como a montagem transforma a violência em espetáculo?",
                "Até que ponto Buscapé escapa do ciclo que narra?",
            ],
        )

    def test_extrai_sequencia_por_minutagem(self):
        sugestoes = extrair_sequencias_sugeridas(
            "A sequência da perseguição ao frango (0:00–3:30) condensa o filme."
        )
        self.assertEqual(len(sugestoes), 1)


class TestCliFase5(unittest.TestCase):
    def test_comando_maestro(self):
        codigo, saida, _ = executar(
            "maestro",
            "--titulo", VALORES["TITULO_DA_OBRA"],
            "--diretor", VALORES["DIRETOR_OU_CRIADOR"],
            "--tipo", VALORES["TIPO_DE_OBRA"],
            "--objetivo", VALORES["META_DA_ANALISE"],
            "--nivel", VALORES["NIVEL_DO_USUARIO"],
            "--impressoes", VALORES["IMPRESSOES_INICIAIS"],
        )
        self.assertEqual(codigo, 0)
        self.assertIn("Prompt Maestro", saida)
        self.assertIn("Comece agora apenas pela primeira etapa", saida)

    def test_comando_sessao_gera_somente_a_trilha(self):
        with tempfile.TemporaryDirectory() as tmp:
            codigo, saida, _ = executar(
                "sessao",
                "--titulo", VALORES["TITULO_DA_OBRA"],
                "--diretor", VALORES["DIRETOR_OU_CRIADOR"],
                "--tipo", VALORES["TIPO_DE_OBRA"],
                "--objetivo", VALORES["META_DA_ANALISE"],
                "--nivel", VALORES["NIVEL_DO_USUARIO"],
                "--impressoes", VALORES["IMPRESSOES_INICIAIS"],
                "--trilha", "padrao",
                "--destino", tmp,
            )
            self.assertEqual(codigo, 0)
            pasta = Path(tmp) / "cidade-de-deus-2002"
            for nome in (
                "00-prompt-preparacao.md",
                "00r-prompt-pesquisa-fontes.md",
                "01-prompt-analise-360.md",
                "00-prompt-maestro.md",
                "dossie-de-fontes.md",
                "registro.md",
            ):
                self.assertTrue((pasta / nome).is_file(), nome)
            self.assertFalse((pasta / "01s-prompt-analise-360-serie.md").exists())
            manifesto = json.loads((pasta / "sessao.json").read_text(encoding="utf-8"))
            self.assertEqual(manifesto["trilha"], "padrao")
            self.assertIn("Sessão guiada criada", saida)

    def test_novo_tambem_inclui_maestro_e_manifesto(self):
        with tempfile.TemporaryDirectory() as tmp:
            codigo, _, _ = executar(
                "novo",
                "--titulo", VALORES["TITULO_DA_OBRA"],
                "--diretor", VALORES["DIRETOR_OU_CRIADOR"],
                "--destino", tmp,
            )
            self.assertEqual(codigo, 0)
            pasta = Path(tmp) / "cidade-de-deus-2002"
            self.assertTrue((pasta / "00-prompt-maestro.md").is_file())
            self.assertTrue((pasta / "sessao.json").is_file())


class TestWebFase5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = (RAIZ / "index.html").read_text(encoding="utf-8")
        cls.sessao = (RAIZ / "assets" / "sessao.js").read_text(encoding="utf-8")
        cls.pesquisa = (RAIZ / "assets" / "pesquisa.js").read_text(encoding="utf-8")

    def test_jornada_guiada_esta_no_html(self):
        for trecho in (
            'id="btn-montar-sessao"',
            'id="sessao-etapas"',
            'id="prompt-maestro"',
            'id="dossie-fontes"',
            'id="busca-obra"',
            'id="provedor"',
            "assets/pesquisa.js",
            "assets/sessao.js",
        ):
            with self.subTest(trecho=trecho):
                self.assertIn(trecho, self.index)

    def test_sessao_importa_respostas_e_tem_provedores_opcionais(self):
        for trecho in (
            "extrairPerguntas",
            "extrairSequencias",
            "definir-manual",
            "dadoManual",
            "montarPromptMaestro",
            "executarComPuter",
            "executarComByok",
            "executarComLocal",
            "exportarMarkdown",
            "importarJson",
        ):
            with self.subTest(trecho=trecho):
                self.assertIn(trecho, self.sessao)

    def test_pesquisa_usa_bases_abertas(self):
        for trecho in (
            "pt.wikipedia.org/w/api.php",
            "wikidata.org/w/api.php",
            "api.tvmaze.com/search/shows",
            "wbsearchentities",
        ):
            with self.subTest(trecho=trecho):
                self.assertIn(trecho, self.pesquisa)


if __name__ == "__main__":
    unittest.main()
