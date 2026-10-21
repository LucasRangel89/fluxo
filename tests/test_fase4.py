"""Testes da Fase 4: variante de séries (1S), comparativa (Etapa 4), modos
de análise, CLI interativa e templates empacotados (P12–P14, P16, P17).

Executa sem dependências externas: `python -m unittest discover -s tests -v`
"""

from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from fluxo.cli import main as cli_main  # noqa: E402
from fluxo.core import (  # noqa: E402
    MODOS_DE_ANALISE,
    FluxoError,
    gerar_prompt,
    normalizar_etapa,
    preencher,
)

VALORES = {
    "TITULO_DA_OBRA": "Dark — Temporada 1 (2017)",
    "DIRETOR_OU_CRIADOR": "Baran bo Odar e Jantje Friese (criadores/showrunners)",
    "TIPO_DE_OBRA": "Série — temporada 1",
    "META_DA_ANALISE": "Entender como a série sustenta o mistério",
    "NIVEL_DO_USUARIO": "intermediário",
    "IMPRESSOES_INICIAIS": "Achei o piloto lento, mas o final me pegou",
    "PERGUNTA_ESCOLHIDA": "Como a montagem constrói o tempo circular?",
    "SEQUENCIA_ESCOLHIDA": "O final do episódio T1:E10",
    "OBRA_A": "Cidade de Deus (2002)",
    "DIRETOR_A": "Fernando Meirelles e Kátia Lund",
    "OBRA_B": "Tropa de Elite (2007)",
    "DIRETOR_B": "José Padilha",
    "EIXO_DE_COMPARACAO": "Duas visões da violência urbana brasileira",
}


class TestEtapaSerie(unittest.TestCase):
    def test_360_seriado_tem_vocabulario_proprio(self) -> None:
        prompt = gerar_prompt("1s", VALORES)
        self.assertIn("Dark — Temporada 1 (2017)", prompt)
        self.assertIn("bo Odar", prompt)
        self.assertIn("showrunner", prompt)
        self.assertIn("cliffhangers", prompt)
        self.assertIn("episódio-síntese", prompt)
        self.assertNotIn("{{", prompt)

    def test_aliases_da_variante_serie(self) -> None:
        for entrada in ("1s", "01s", "serie", "séries", "temporada"):
            if entrada == "séries":
                continue  # com acento não é alias; só formas sem acento
            self.assertEqual(normalizar_etapa(entrada), "1s")


class TestComparativa(unittest.TestCase):
    def test_comparativa_completa(self) -> None:
        prompt = gerar_prompt("4", VALORES)
        self.assertIn("Cidade de Deus (2002)", prompt)
        self.assertIn("Tropa de Elite (2007)", prompt)
        self.assertIn("Duas visões da violência urbana brasileira", prompt)
        self.assertIn("Comparação dimensão a dimensão", prompt)
        self.assertNotIn("{{", prompt)

    def test_comparativa_exige_as_duas_obras_e_o_eixo(self) -> None:
        so_obra_a = {k: v for k, v in VALORES.items() if k.startswith("OBRA_A")}
        with self.assertRaises(FluxoError) as ctx:
            gerar_prompt("4", so_obra_a)
        mensagem = str(ctx.exception)
        self.assertIn("--obra-b", mensagem)
        self.assertIn("--eixo", mensagem)

    def test_aliases_da_comparativa(self) -> None:
        for entrada in ("4", "04", "comparativa", "comparacao"):
            self.assertEqual(normalizar_etapa(entrada), "4")


class TestModosDeAnalise(unittest.TestCase):
    def test_modo_eh_opcional_no_modo_estrito(self) -> None:
        prompt = gerar_prompt("1", VALORES)  # sem MODO_DE_ANALISE
        self.assertNotIn("Calibragem", prompt)
        self.assertNotIn("\n\n\n", prompt)  # sem buraco no texto

    def test_modos_injetam_calibragem(self) -> None:
        for modo, trecho in (
            ("iniciante", "Calibragem (modo iniciante)"),
            ("academico", "Calibragem (modo acadêmico)"),
        ):
            prompt = gerar_prompt(
                "1", {**VALORES, "MODO_DE_ANALISE": MODOS_DE_ANALISE[modo]}
            )
            self.assertIn(trecho, prompt)

    def test_preencher_colapsa_o_opcional_vazio(self) -> None:
        resultado = preencher("A\n\n{{MODO_DE_ANALISE}}\n\nB", {})
        self.assertEqual(resultado, "A\n\nB")

    def test_modo_via_cli(self) -> None:
        saida = io.StringIO()
        with redirect_stdout(saida):
            codigo = cli_main(
                [
                    "gerar", "1s",
                    "--titulo", "Dark — Temporada 1 (2017)",
                    "--diretor", "Baran bo Odar e Jantje Friese",
                    "--modo", "iniciante",
                ]
            )
        self.assertEqual(codigo, 0)
        self.assertIn("Calibragem (modo iniciante)", saida.getvalue())


class TestInterativo(unittest.TestCase):
    def _rodar(self, respostas: list[str]) -> tuple[int, str]:
        saida = io.StringIO()
        with mock.patch("builtins.input", side_effect=respostas):
            with redirect_stdout(saida):
                codigo = cli_main(["interativo"])
        return codigo, saida.getvalue()

    def test_gera_prompt_guiado(self) -> None:
        codigo, saida = self._rodar(
            ["Interestelar (2014)", "Christopher Nolan", "0", "2.1", "n", "n", "sair"]
        )
        self.assertEqual(codigo, 0)
        self.assertIn("Interestelar (2014)", saida)
        self.assertIn("3 a 5 pontos", saida)
        self.assertIn("Até logo", saida)

    def test_pergunta_o_que_falta_na_etapa_2_2(self) -> None:
        pergunta = "O que a escada diz sobre classe social no filme?"
        codigo, saida = self._rodar(
            ["Parasita (2019)", "Bong Joon-ho", "1", "2.2", pergunta, "n", "n", "sair"]
        )
        self.assertEqual(codigo, 0)
        self.assertIn(pergunta, saida)

    def test_eof_encerra_sem_erro(self) -> None:
        saida = io.StringIO()
        with mock.patch("builtins.input", side_effect=EOFError):
            with redirect_stdout(saida):
                codigo = cli_main(["interativo"])
        self.assertEqual(codigo, 0)


class TestTemplatesEmpacotados(unittest.TestCase):
    def test_copias_sincronizadas_com_os_originais(self) -> None:
        empacotado = RAIZ / "src" / "fluxo" / "_templates"
        originais = list((RAIZ / "prompts").glob("*.md")) + [
            RAIZ / "templates" / "registro-de-analise.md"
        ]
        for original in originais:
            copia = empacotado / original.name
            self.assertTrue(
                copia.is_file(),
                f"Falta a cópia empacotada de {original.name}: "
                "rode scripts/sincronizar_templates.py",
            )
            self.assertEqual(
                original.read_bytes(),
                copia.read_bytes(),
                f"Cópia empacotada dessincronizada: {original.name}. "
                "Rode scripts/sincronizar_templates.py",
            )

    def test_diretorio_empacotado_gera_o_mesmo_prompt(self) -> None:
        empacotado = RAIZ / "src" / "fluxo" / "_templates"
        self.assertEqual(
            gerar_prompt("1", VALORES, diretorio=empacotado),
            gerar_prompt("1", VALORES),
        )


if __name__ == "__main__":
    unittest.main()
