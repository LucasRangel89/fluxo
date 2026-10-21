"""Testes da Fase 3: Etapa 0, Etapas 1A/1B, Close Reading 2.3 e hipótese."""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from fluxo.cli import main
from fluxo.core import ETAPAS, FluxoError, gerar_prompt, normalizar_etapa

VALORES = {
    "TITULO_DA_OBRA": "Cidade de Deus (2002)",
    "DIRETOR_OU_CRIADOR": "Fernando Meirelles e Kátia Lund",
    "TIPO_DE_OBRA": "Filme (longa-metragem de ficção)",
    "META_DA_ANALISE": "Estudar um clássico brasileiro",
    "NIVEL_DO_USUARIO": "Intermediário",
    "IMPRESSOES_INICIAIS": "Achei a violência espetacularizada demais.",
    "PERGUNTA_ESCOLHIDA": "Como a montagem constrói o ciclo de violência?",
    "SEQUENCIA_ESCOLHIDA": "A abertura: perseguição ao frango (≈0:00–3:30)",
}


def executar(*args: str) -> tuple[int, str, str]:
    saida, erros = io.StringIO(), io.StringIO()
    with redirect_stdout(saida), redirect_stderr(erros):
        codigo = main(list(args))
    return codigo, saida.getvalue(), erros.getvalue()


class TestAliasesNovos(unittest.TestCase):
    def test_etapa0(self):
        for entrada in ("0", "00", "etapa-0", "setup", "preparacao"):
            with self.subTest(entrada=entrada):
                self.assertEqual(normalizar_etapa(entrada), "0")

    def test_dois_tempos(self):
        self.assertEqual(normalizar_etapa("1a"), "1a")
        self.assertEqual(normalizar_etapa("01B"), "1b")
        self.assertEqual(normalizar_etapa("texto"), "1a")
        self.assertEqual(normalizar_etapa("contexto"), "1b")

    def test_close_reading(self):
        self.assertEqual(normalizar_etapa("2.3"), "2.3")
        self.assertEqual(normalizar_etapa("close"), "2.3")
        self.assertEqual(normalizar_etapa("close reading"), "2.3")


class TestEtapa0(unittest.TestCase):
    def test_registra_hipotese_sem_analisar(self):
        prompt = gerar_prompt("0", VALORES)
        self.assertIn("ainda não analise a obra", prompt)
        self.assertIn(VALORES["IMPRESSOES_INICIAIS"], prompt)
        self.assertIn("pontos de atenção", prompt)
        self.assertNotIn("{{", prompt)

    def test_exige_impressoes(self):
        incompleto = {k: v for k, v in VALORES.items() if k != "IMPRESSOES_INICIAIS"}
        with self.assertRaises(FluxoError) as ctx:
            gerar_prompt("0", incompleto)
        self.assertIn("--impressoes", str(ctx.exception))


class TestDoisTempos(unittest.TestCase):
    def test_1a_cobre_so_o_texto(self):
        prompt = gerar_prompt("1a", VALORES)
        self.assertIn("dimensões 2 a 5", prompt)
        self.assertIn("Atuação e Elenco", prompt)
        self.assertNotIn("7. **Recepção", prompt)

    def test_1b_fecha_com_tabela_completa(self):
        prompt = gerar_prompt("1b", VALORES)
        self.assertIn("tabela-resumo completa das 7 dimensões", prompt)
        self.assertIn("Posição do Espectador", prompt)

    def test_uniao_cobre_as_7_dimensoes(self):
        uniao = gerar_prompt("1a", VALORES) + gerar_prompt("1b", VALORES)
        for trecho in (
            "Ficha Técnica", "Trama e Enredo", "Fotografia e Iluminação",
            "Trilha Sonora", "Montagem e Ritmo", "Comentário Social",
            "Recepção e Impacto Cultural",
        ):
            with self.subTest(trecho=trecho):
                self.assertIn(trecho, uniao)


class TestCloseReading(unittest.TestCase):
    def test_pede_decoupagem(self):
        prompt = gerar_prompt("2.3", VALORES)
        self.assertIn("Decupagem", prompt)
        self.assertIn(VALORES["SEQUENCIA_ESCOLHIDA"], prompt)

    def test_exige_sequencia(self):
        with self.assertRaises(FluxoError):
            gerar_prompt("2.3", {"TITULO_DA_OBRA": "X"})


class TestEtapa3RevisitaHipotese(unittest.TestCase):
    def test_menciona_etapa0_e_hipotese(self):
        prompt = gerar_prompt("3", VALORES)
        self.assertIn("Etapa 0", prompt)
        self.assertIn("hipótese", prompt)


class TestCliFase3(unittest.TestCase):
    def test_gerar_etapa0(self):
        codigo, saida, _ = executar(
            "gerar", "0",
            "--titulo", VALORES["TITULO_DA_OBRA"],
            "--diretor", VALORES["DIRETOR_OU_CRIADOR"],
            "--tipo", VALORES["TIPO_DE_OBRA"],
            "--objetivo", VALORES["META_DA_ANALISE"],
            "--nivel", VALORES["NIVEL_DO_USUARIO"],
            "--impressoes", VALORES["IMPRESSOES_INICIAIS"],
        )
        self.assertEqual(codigo, 0)
        self.assertIn("preparação", saida)
        self.assertNotIn("{{", saida)

    def test_gerar_2_3(self):
        codigo, saida, _ = executar(
            "gerar", "2.3",
            "--titulo", VALORES["TITULO_DA_OBRA"],
            "--sequencia", VALORES["SEQUENCIA_ESCOLHIDA"],
        )
        self.assertEqual(codigo, 0)
        self.assertIn("close reading", saida.lower())

    def test_novo_gera_todas_as_etapas(self):
        with tempfile.TemporaryDirectory() as tmp:
            codigo, _, _ = executar(
                "novo",
                "--titulo", VALORES["TITULO_DA_OBRA"],
                "--diretor", VALORES["DIRETOR_OU_CRIADOR"],
                "--destino", tmp,
            )
            self.assertEqual(codigo, 0)
            pasta = Path(tmp) / "cidade-de-deus-2002"
            for etapa in ETAPAS.values():
                self.assertTrue(
                    (pasta / etapa.arquivo_saida).is_file(), etapa.arquivo_saida
                )
            registro = (pasta / "registro.md").read_text(encoding="utf-8")
            self.assertIn("Etapa 0 — Preparação", registro)
            self.assertIn("Minha leitura inicial mudou?", registro)

    def test_listar_inclui_novas_etapas(self):
        codigo, saida, _ = executar("listar")
        self.assertEqual(codigo, 0)
        for trecho in ("Etapa 0", "Etapa 1a", "Etapa 1b", "Etapa 2.3"):
            self.assertIn(trecho, saida)


if __name__ == "__main__":
    unittest.main()
