"""Testes do núcleo (core): templates, placeholders e geração de prompts."""

import unittest

from fluxo.core import (
    ETAPAS,
    FluxoError,
    extrair_prompt,
    gerar_prompt,
    normalizar_etapa,
    preencher,
    slugificar,
)

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


class TestNormalizarEtapa(unittest.TestCase):
    def test_aliases(self):
        Casos = {
            "1": "1",
            "01": "1",
            "etapa-1": "1",
            "2.1": "2.1",
            "etapa-2.1": "2.1",
            "22": "2.2",
            "2-2": "2.2",
            "ETAPA 3": "3",
            "03": "3",
        }
        for entrada, esperado in Casos.items():
            with self.subTest(entrada=entrada):
                self.assertEqual(normalizar_etapa(entrada), esperado)

    def test_etapa_invalida(self):
        with self.assertRaises(FluxoError):
            normalizar_etapa("9")


class TestExtrairPrompt(unittest.TestCase):
    def test_extrai_entre_marcadores(self):
        texto = (
            "# Título\n\n<!-- INICIO DO PROMPT -->\n"
            "TEXTO DO PROMPT\n<!-- FIM DO PROMPT -->\n\nrodapé"
        )
        self.assertEqual(extrair_prompt(texto), "TEXTO DO PROMPT")

    def test_sem_marcadores_gera_erro(self):
        with self.assertRaises(FluxoError):
            extrair_prompt("arquivo sem marcadores")


class TestPreencher(unittest.TestCase):
    def test_substitui_placeholder(self):
        resultado = preencher("Obra: {{TITULO_DA_OBRA}}", VALORES)
        self.assertEqual(resultado, "Obra: Cidade de Deus (2002)")

    def test_modo_estrito_exige_todos_os_valores(self):
        with self.assertRaises(FluxoError) as ctx:
            preencher("{{TITULO_DA_OBRA}} / {{DIRETOR_OU_CRIADOR}}", {})
        self.assertIn("--titulo", str(ctx.exception))
        self.assertIn("--diretor", str(ctx.exception))

    def test_modo_nao_estrito_marca_pendencias(self):
        resultado = preencher("{{PERGUNTA_ESCOLHIDA}}", {}, estrito=False)
        self.assertEqual(resultado, "[PREENCHER: PERGUNTA_ESCOLHIDA]")

    def test_valor_vazio_conta_como_ausente(self):
        with self.assertRaises(FluxoError):
            preencher("{{TITULO_DA_OBRA}}", {"TITULO_DA_OBRA": "   "})


class TestGerarPrompt(unittest.TestCase):
    def test_etapa1_preenchida(self):
        prompt = gerar_prompt("1", VALORES)
        self.assertIn("Cidade de Deus (2002)", prompt)
        self.assertIn("Fernando Meirelles e Kátia Lund", prompt)
        self.assertIn("7 dimensões", prompt)
        self.assertNotIn("{{", prompt)

    def test_todas_as_etapas_geram_sem_placeholder_restante(self):
        for etapa_id in ETAPAS:
            with self.subTest(etapa=etapa_id):
                prompt = gerar_prompt(etapa_id, VALORES)
                self.assertTrue(prompt.strip())
                self.assertNotIn("{{", prompt)
                self.assertNotIn("INICIO DO PROMPT", prompt)

    def test_etapa22_exige_pergunta(self):
        with self.assertRaises(FluxoError):
            gerar_prompt("2.2", {"TITULO_DA_OBRA": "X", "DIRETOR_OU_CRIADOR": "Y"})

    def test_etapa22_nao_exige_titulo(self):
        prompt = gerar_prompt("2.2", {"PERGUNTA_ESCOLHIDA": "Por quê?"})
        self.assertIn("Por quê?", prompt)


class TestPromptsV2(unittest.TestCase):
    """Características da Fase 1: blindagem, formato e subitens teóricos."""

    def test_etapa1_tem_persona_guardrails_formato_e_subitens(self):
        prompt = gerar_prompt("1", VALORES)
        self.assertIn("crítico de cinema", prompt)          # persona (P1)
        self.assertIn("(a confirmar)", prompt)              # guardrail (P2)
        self.assertIn("tabela-resumo", prompt)              # formato (P3)
        self.assertIn("minutagem aproximada", prompt)       # evidências (P3)
        self.assertIn("Atuação e Elenco", prompt)           # subitem (P10)
        self.assertIn("Gênero e Convenções", prompt)        # subitem (P10)
        self.assertIn("Posição do Espectador", prompt)      # subitem (P10)
        self.assertIn("focalização", prompt)                # subitem (P10)
        self.assertIn("kishōtenketsu", prompt)              # viés clássico (P11)
        self.assertIn("7 dimensões", prompt)                # mantém as 7 dimensões

    def test_etapa21_pede_diversidade_de_perguntas(self):
        prompt = gerar_prompt("2.1", VALORES)
        self.assertIn("diversidade", prompt)                # P6

    def test_etapa22_tem_contra_argumento(self):
        prompt = gerar_prompt("2.2", VALORES)
        self.assertIn("Contra-argumento", prompt)           # P7

    def test_etapa3_tem_balanco_critico_e_ficha_resumo(self):
        prompt = gerar_prompt("3", VALORES)
        self.assertIn("Balanço Crítico", prompt)            # P9
        self.assertIn("Ficha-Resumo", prompt)               # P3


class TestSlugificar(unittest.TestCase):
    def test_acentos_pontuacao_e_espacos(self):
        self.assertEqual(slugificar("Cidade de Deus (2002)"), "cidade-de-deus-2002")
        self.assertEqual(slugificar("O Fabuloso Destino de Amélie!"), "o-fabuloso-destino-de-amelie")
        self.assertEqual(slugificar("   É o Amô   "), "e-o-amo")

    def test_texto_vazio(self):
        self.assertEqual(slugificar("!!!"), "obra-sem-titulo")


if __name__ == "__main__":
    unittest.main()
