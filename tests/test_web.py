"""Testes de integração da interface web (Fase 2).

A UI (index.html + assets/app.js) lê os mesmos templates que a CLI. Estes
testes garantem que os dois lados continuam consistentes — nada de drift
silencioso entre a lista de etapas do JavaScript e a do Python.
"""

import unittest
from pathlib import Path

from fluxo import __version__
from fluxo.core import ETAPAS, MARCADOR_FIM, MARCADOR_INICIO, PLACEHOLDERS

RAIZ = Path(__file__).resolve().parents[1]


class TestInterfaceWeb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = (RAIZ / "index.html").read_text(encoding="utf-8")
        cls.js = (RAIZ / "assets" / "app.js").read_text(encoding="utf-8")
        cls.css = (RAIZ / "assets" / "app.css").read_text(encoding="utf-8")

    def test_index_referencia_assets_e_campos(self):
        self.assertIn("assets/app.css", self.index)
        self.assertIn("assets/app.js", self.index)
        for campo in (
            'id="titulo"', 'id="diretor"', 'id="tipo"', 'id="objetivo"',
            'id="nivel"', 'id="impressoes"', 'id="pergunta"',
            'id="sequencia"', 'id="obra-a"', 'id="diretor-a"',
            'id="obra-b"', 'id="diretor-b"', 'id="eixo"', 'id="modo"',
            'id="saida"', 'id="stepper"',
        ):
            with self.subTest(campo=campo):
                self.assertIn(campo, self.index)

    def test_js_usa_os_mesmos_templates_da_cli(self):
        for etapa in ETAPAS.values():
            with self.subTest(etapa=etapa.id):
                self.assertIn(f"prompts/{etapa.arquivo_template}", self.js)
                self.assertIn(etapa.arquivo_saida, self.js)
                caminho = RAIZ / "prompts" / etapa.arquivo_template
                self.assertTrue(caminho.is_file(), f"template ausente: {caminho}")

    def test_js_usa_os_mesmos_marcadores_e_placeholders(self):
        self.assertIn(MARCADOR_INICIO, self.js)
        self.assertIn(MARCADOR_FIM, self.js)
        for chave in PLACEHOLDERS:
            if chave == "DATA_DA_ANALISE":
                continue  # só existe no template de registro, fora da UI
            with self.subTest(placeholder=chave):
                self.assertIn(chave, self.js)

    def test_versao_exibida_confere_com_o_pacote(self):
        self.assertIn(__version__, self.index)

    def test_nojekyll_para_github_pages(self):
        self.assertTrue((RAIZ / ".nojekyll").is_file())

    def test_css_presente(self):
        self.assertGreater(len(self.css), 500)


if __name__ == "__main__":
    unittest.main()
