"""Testes da interface de linha de comando (CLI)."""

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from fluxo.cli import main


def executar(*args: str) -> tuple[int, str, str]:
    saida, erros = io.StringIO(), io.StringIO()
    with redirect_stdout(saida), redirect_stderr(erros):
        codigo = main(list(args))
    return codigo, saida.getvalue(), erros.getvalue()


class TestComandoListar(unittest.TestCase):
    def test_lista_todas_as_etapas(self):
        codigo, saida, _ = executar("listar")
        self.assertEqual(codigo, 0)
        for trecho in ("Etapa 1", "Etapa 2.1", "Etapa 2.2", "Etapa 3"):
            self.assertIn(trecho, saida)


class TestComandoGerar(unittest.TestCase):
    def test_gera_etapa1(self):
        codigo, saida, _ = executar(
            "gerar", "1",
            "--titulo", "Parasita (2019)",
            "--diretor", "Bong Joon-ho",
        )
        self.assertEqual(codigo, 0)
        self.assertIn("Parasita (2019)", saida)
        self.assertIn("Bong Joon-ho", saida)
        self.assertNotIn("{{", saida)

    def test_sem_diretor_falha_com_mensagem_util(self):
        codigo, _, erros = executar("gerar", "1", "--titulo", "Parasita (2019)")
        self.assertEqual(codigo, 1)
        self.assertIn("--diretor", erros)

    def test_etapa_invalida_falha(self):
        codigo, _, erros = executar("gerar", "9", "--titulo", "X")
        self.assertEqual(codigo, 1)
        self.assertIn("Etapas válidas", erros)

    def test_salvar_em_arquivo(self):
        with tempfile.TemporaryDirectory() as tmp:
            destino = Path(tmp) / "prompt.md"
            codigo, _, _ = executar(
                "gerar", "3",
                "--titulo", "Parasita (2019)",
                "--salvar", str(destino),
            )
            self.assertEqual(codigo, 0)
            conteudo = destino.read_text(encoding="utf-8")
            self.assertIn("Parasita (2019)", conteudo)


class TestComandoNovo(unittest.TestCase):
    def test_cria_estrutura_completa(self):
        with tempfile.TemporaryDirectory() as tmp:
            codigo, saida, _ = executar(
                "novo",
                "--titulo", "Cidade de Deus (2002)",
                "--diretor", "Fernando Meirelles e Kátia Lund",
                "--destino", tmp,
            )
            self.assertEqual(codigo, 0)
            pasta = Path(tmp) / "cidade-de-deus-2002"
            esperados = (
                "01-prompt-analise-360.md",
                "02.1-prompt-proposta-aprofundamento.md",
                "02.2-prompt-analise-focada.md",
                "03-prompt-sintese-conexoes.md",
                "registro.md",
            )
            for nome in esperados:
                self.assertTrue((pasta / nome).is_file(), f"faltando: {nome}")
            prompt1 = (pasta / "01-prompt-analise-360.md").read_text(encoding="utf-8")
            self.assertIn("Cidade de Deus (2002)", prompt1)
            # Sem --pergunta, a Etapa 2.2 fica marcada como pendente.
            prompt22 = (pasta / "02.2-prompt-analise-focada.md").read_text(encoding="utf-8")
            self.assertIn("[PREENCHER: PERGUNTA_ESCOLHIDA]", prompt22)
            self.assertIn("Análise criada", saida)

    def test_recusa_sobrescrever_sem_forcar(self):
        with tempfile.TemporaryDirectory() as tmp:
            args = ("novo", "--titulo", "Parasita (2019)", "--destino", tmp)
            self.assertEqual(executar(*args)[0], 0)
            codigo, _, erros = executar(*args)
            self.assertEqual(codigo, 1)
            self.assertIn("--forcar", erros)
            self.assertEqual(executar(*args, "--forcar")[0], 0)

    def test_slug_personalizado(self):
        with tempfile.TemporaryDirectory() as tmp:
            codigo, _, _ = executar(
                "novo", "--titulo", "Cidade de Deus (2002)",
                "--slug", "cdd", "--destino", tmp,
            )
            self.assertEqual(codigo, 0)
            self.assertTrue((Path(tmp) / "cdd" / "registro.md").is_file())


if __name__ == "__main__":
    unittest.main()
