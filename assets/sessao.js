"use strict";

/* ============================================================================
   Fluxo — sessão guiada (Fase 5)

   Este módulo transforma o gerador de prompts em uma jornada: o usuário
   informa a obra uma vez, o Fluxo cria as etapas relevantes já preenchidas,
   acompanha o estado de cada uma, importa respostas e prepara a próxima.
   O modo manual continua sendo o padrão: sem backend e sem chave do projeto.
   ========================================================================== */

(() => {
  const $ = (id) => document.getElementById(id);
  const ids = [
    "trilha", "ia-destino", "incluir-pesquisa", "incluir-close",
    "incluir-contexto", "modo-sessao-guiada", "modo-sessao-maestro",
    "btn-montar-sessao", "painel-comparativa", "sessao-card",
    "sessao-progresso", "sessao-progresso-texto", "proxima-acao",
    "btn-proxima-acao", "sessao-etapas", "painel-maestro",
    "prompt-maestro", "transcricao-maestro", "btn-enviar-maestro",
    "btn-copiar-maestro", "provedor", "provedor-status",
    "config-puter", "config-byok", "config-local", "puter-modelo",
    "byok-endpoint", "byok-modelo", "byok-chave", "byok-lembrar",
    "btn-testar-provedor", "btn-resumir-local",
    "btn-exportar-sessao-md", "btn-exportar-sessao-json",
    "importar-sessao", "btn-resetar-sessao",
  ];
  const el = {};
  ids.forEach((id) => { el[id] = $(id); });
  if (!el["btn-montar-sessao"] || !el["sessao-card"]) return;

  const CHAVE_SESSAO = "fluxo-sessao-v1";
  const CHAVE_BYOK = "fluxo-byok-chave-sessao";
  const DESTINOS_IA = {
    manual: { nome: "sua IA", url: "" },
    chatgpt: { nome: "ChatGPT", url: "https://chatgpt.com/" },
    claude: { nome: "Claude", url: "https://claude.ai/new" },
    gemini: { nome: "Gemini", url: "https://gemini.google.com/app" },
    perplexity: { nome: "Perplexity", url: "https://www.perplexity.ai/" },
    copilot: { nome: "Copilot", url: "https://copilot.microsoft.com/" },
  };
  const MAPAS_360 = new Set(["1", "1a", "1b", "1s"]);

  function novaSessao() {
    return {
      versao: 1,
      criada: false,
      modo: "guiada",
      trilha: "padrao",
      iaDestino: "manual",
      incluirPesquisa: true,
      incluirClose: true,
      incluirContexto: false,
      etapas: [],
      respostas: {},
      enviadas: {},
      concluidas: {},
      resumos: {},
      perguntasDetectadas: [],
      sequenciasDetectadas: [],
      resumoLocal: "",
      transcricaoMaestro: "",
      provedor: "manual",
      provedorConfig: {
        puterModelo: "",
        byokEndpoint: "https://openrouter.ai/api/v1/chat/completions",
        byokModelo: "",
      },
    };
  }

  let sessao = novaSessao();
  try {
    const salvo = JSON.parse(localStorage.getItem(CHAVE_SESSAO) || "null");
    if (salvo && typeof salvo === "object") {
      sessao = {
        ...novaSessao(),
        ...salvo,
        provedorConfig: {
          ...novaSessao().provedorConfig,
          ...(salvo.provedorConfig || {}),
        },
      };
    }
  } catch (_e) {
    sessao = novaSessao();
  }

  let temporizadorRender = null;

  function salvarSessao() {
    try {
      localStorage.setItem(CHAVE_SESSAO, JSON.stringify(sessao));
    } catch (_e) { /* a sessão continua somente em memória */ }
  }

  function disparar(elemento) {
    if (!elemento) return;
    elemento.dispatchEvent(new Event("input", { bubbles: true }));
    elemento.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function definirValor(id, valor) {
    const campo = $(id);
    if (!campo || campo.value === valor) return;
    campo.value = valor;
    disparar(campo);
  }

  function valorDe(id) {
    return ($(id)?.value || "").trim();
  }

  function etapaPorId(id) {
    return ETAPAS.find((etapa) => etapa.id === id);
  }

  function lerConfiguracao() {
    return {
      modo: el["modo-sessao-maestro"]?.checked ? "maestro" : "guiada",
      trilha: el.trilha?.value || "padrao",
      iaDestino: el["ia-destino"]?.value || "manual",
      incluirPesquisa: !!el["incluir-pesquisa"]?.checked,
      incluirClose: !!el["incluir-close"]?.checked,
      incluirContexto: !!el["incluir-contexto"]?.checked,
      provedor: el.provedor?.value || "manual",
      provedorConfig: {
        puterModelo: valorDe("puter-modelo"),
        byokEndpoint: valorDe("byok-endpoint"),
        byokModelo: valorDe("byok-modelo"),
      },
    };
  }

  function sincronizarControles() {
    if (el.trilha) el.trilha.value = sessao.trilha || "padrao";
    if (el["ia-destino"]) el["ia-destino"].value = sessao.iaDestino || "manual";
    if (el["incluir-pesquisa"]) el["incluir-pesquisa"].checked = !!sessao.incluirPesquisa;
    if (el["incluir-close"]) el["incluir-close"].checked = !!sessao.incluirClose;
    if (el["incluir-contexto"]) el["incluir-contexto"].checked = !!sessao.incluirContexto;
    if (el["modo-sessao-guiada"]) el["modo-sessao-guiada"].checked = sessao.modo !== "maestro";
    if (el["modo-sessao-maestro"]) el["modo-sessao-maestro"].checked = sessao.modo === "maestro";
    if (el.provedor) el.provedor.value = sessao.provedor || "manual";
    if (el["puter-modelo"]) el["puter-modelo"].value = sessao.provedorConfig.puterModelo || "";
    if (el["byok-endpoint"]) el["byok-endpoint"].value = sessao.provedorConfig.byokEndpoint || "";
    if (el["byok-modelo"]) el["byok-modelo"].value = sessao.provedorConfig.byokModelo || "";
    if (el["transcricao-maestro"]) {
      el["transcricao-maestro"].value = sessao.transcricaoMaestro || "";
    }
    try {
      const chave = sessionStorage.getItem(CHAVE_BYOK);
      if (chave && el["byok-chave"]) {
        el["byok-chave"].value = chave;
        el["byok-lembrar"].checked = true;
      }
    } catch (_e) { /* sem sessionStorage */ }
    atualizarComparativa();
    atualizarConfigProvedor();
  }

  function atualizarComparativa() {
    if (!el["painel-comparativa"]) return;
    const mostrar = el.trilha?.value === "comparativa" || estado.etapaAtual === "4";
    el["painel-comparativa"].hidden = !mostrar;
  }

  function aplicarPadroes() {
    const trilha = el.trilha?.value || "padrao";
    if (!valorDe("tipo")) {
      const tipos = {
        padrao: "Filme (longa-metragem de ficção)",
        "dois-tempos": "Filme (longa-metragem de ficção)",
        serie: "Série — temporada",
        comparativa: "Comparação entre duas obras audiovisuais",
      };
      definirValor("tipo", tipos[trilha] || tipos.padrao);
    }
    if (!valorDe("objetivo")) {
      definirValor("objetivo", "Compreender a obra em profundidade, conectando forma, temas e contexto");
    }
    if (!valorDe("nivel")) {
      const modos = {
        iniciante: "Iniciante — prefiro termos explicados e exemplos concretos",
        academico: "Avançado — busco rigor teórico e debates da área",
        padrao: "Intermediário — familiarizado com crítica e linguagem audiovisual",
      };
      definirValor("nivel", modos[$("modo")?.value] || modos.padrao);
    }
    if (!valorDe("impressoes")) {
      definirValor(
        "impressoes",
        "Ainda não tenho uma hipótese fechada; começo sem uma leitura definitiva e quero registrar esse ponto de partida."
      );
    }
    if (trilha === "comparativa" && !valorDe("obra-a") && valorDe("titulo")) {
      definirValor("obra-a", valorDe("titulo"));
      definirValor("diretor-a", valorDe("diretor"));
    }
  }

  function calcularOrdem(config = sessao) {
    const trilhas = {
      padrao: ["0", "1", "2.1", "2.2", "2.3", "3"],
      serie: ["0", "1s", "2.1", "2.2", "2.3", "3"],
      "dois-tempos": ["0", "1a", "1b", "2.1", "2.2", "2.3", "3"],
      comparativa: ["4"],
    };
    const ordem = [...(trilhas[config.trilha] || trilhas.padrao)];
    if (config.incluirPesquisa) {
      ordem.splice(ordem[0] === "0" ? 1 : 0, 0, "r");
    }
    if (!config.incluirClose) {
      return ordem.filter((id) => id !== "2.3");
    }
    return ordem;
  }

  function valoresAtuais(sobrepor = {}) {
    const valores = {};
    Object.entries(CAMPOS).forEach(([chave, campo]) => {
      if (chave === "MODO_DE_ANALISE") {
        valores[chave] = MODOS_DE_ANALISE[$("modo")?.value] || "";
      } else {
        valores[chave] = valorDe(campo.id);
      }
    });
    return { ...valores, ...sobrepor };
  }

  function valoresParaEtapa(etapaId, sobrepor = {}) {
    const valores = valoresAtuais(sobrepor);
    if (etapaId === "r" && sessao.trilha === "comparativa") {
      const obraA = valores.OBRA_A;
      const obraB = valores.OBRA_B;
      valores.TITULO_DA_OBRA = [obraA, obraB].filter(Boolean).join(" × ");
      valores.DIRETOR_OU_CRIADOR = [
        obraA && valores.DIRETOR_A ? `${obraA}: ${valores.DIRETOR_A}` : "",
        obraB && valores.DIRETOR_B ? `${obraB}: ${valores.DIRETOR_B}` : "",
      ].filter(Boolean).join("; ");
      valores.TIPO_DE_OBRA = "Análise comparativa entre duas obras audiovisuais"
        + (valores.EIXO_DE_COMPARACAO ? `; eixo: ${valores.EIXO_DE_COMPARACAO}` : "");
    }
    return valores;
  }

  function substituirTemplate(template, valores) {
    const pendentes = [];
    const texto = template.replace(RE_PLACEHOLDER, (_trecho, chave) => {
      const valor = (valores[chave] || "").trim();
      if (valor) return valor;
      if (OPCIONAIS.has(chave)) return "";
      const info = CAMPOS[chave];
      if (info && !pendentes.includes(info.rotulo)) pendentes.push(info.rotulo);
      return info ? info.pendente : `[${chave}]`;
    });
    return { texto: texto.replace(/\n{3,}/g, "\n\n"), pendentes };
  }

  function limparMarkdown(texto) {
    return String(texto || "")
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      .replace(/\*\*/g, "")
      .replace(/__/g, "")
      .replace(/`/g, "")
      .replace(/^\s*(?:>\s*|#{1,6}\s*)/, "")
      .replace(/^\s*(?:\d+[.)]|[-*•])\s+/, "")
      .replace(/\s+/g, " ")
      .trim();
  }

  function unicos(lista, limite = 8) {
    const vistos = new Set();
    return lista.filter((item) => {
      const chave = item.toLocaleLowerCase("pt-BR");
      if (!item || vistos.has(chave)) return false;
      vistos.add(chave);
      return true;
    }).slice(0, limite);
  }

  function extrairResumo(texto) {
    const explicito = texto.match(/^\s*(?:[-*•]\s*)?RESUMO\s*:\s*(.+)$/im);
    if (explicito) return limparMarkdown(explicito[1]).slice(0, 700);
    for (const paragrafo of texto.split(/\n\s*\n/)) {
      const limpo = limparMarkdown(paragrafo);
      if (limpo.length >= 50 && !limpo.toLocaleLowerCase().startsWith("dados para o fluxo")) {
        return limpo.slice(0, 700);
      }
    }
    return "";
  }

  function extrairPerguntas(texto) {
    const explicitas = [...texto.matchAll(/^\s*(?:[-*•]\s*)?PERGUNTA\s*:\s*(.+)$/gim)]
      .map((match) => limparMarkdown(match[1]))
      .filter((item) => item.length >= 10);
    if (explicitas.length) return unicos(explicitas);

    const itens = [];
    let atual = [];
    texto.split(/\r?\n/).forEach((linha) => {
      if (/^\s*(?:\d+[.)]|[-*•])\s+/.test(linha)) {
        if (atual.length) itens.push(atual.join(" "));
        atual = [linha.trim()];
      } else if (atual.length && linha.trim()) {
        atual.push(linha.trim());
      }
    });
    if (atual.length) itens.push(atual.join(" "));
    const candidatos = itens.length ? itens : texto.split(/\n\s*\n/);
    const perguntas = [];
    candidatos.forEach((item) => {
      const limpo = limparMarkdown(item);
      if (!limpo.includes("?")) return;
      let pergunta = `${limpo.split("?")[0].trim()}?`;
      const separador = pergunta.indexOf(":");
      if (separador > 0 && separador <= 70) {
        const resto = pergunta.slice(separador + 1).trim();
        if (resto.length >= 12) pergunta = resto;
      }
      if (pergunta.length >= 12) perguntas.push(pergunta);
    });
    return unicos(perguntas);
  }

  function extrairSequencias(texto) {
    const explicitas = [
      ...texto.matchAll(/^\s*(?:[-*•]\s*)?SEQU[ÊE]NCIA(?:_SUGERIDA)?\s*:\s*(.+)$/gim),
    ].map((match) => limparMarkdown(match[1])).filter((item) => item.length >= 8);
    if (explicitas.length) return unicos(explicitas, 5);

    const sugestoes = [];
    texto.split(/\r?\n/).forEach((linha) => {
      const limpa = limparMarkdown(linha);
      if ((/\b\d{1,2}:\d{2}(?::\d{2})?\b/i.test(limpa) || /\bT\d+\s*:\s*E\d+\b/i.test(limpa))
        && /sequ[êe]ncia|cena|abertura|cl[ií]max|desfecho/i.test(limpa)) {
        sugestoes.push(limpa.slice(0, 260));
      }
    });
    return unicos(sugestoes, 5);
  }

  function extrairDados(texto) {
    return {
      resumo: extrairResumo(texto),
      perguntas: extrairPerguntas(texto),
      sequencias: extrairSequencias(texto),
    };
  }

  function instrucaoDadosFluxo(etapaId) {
    const linhas = [
      "",
      "---",
      "Instrução de continuidade do Fluxo: ao final da resposta principal, acrescente uma seção curta intitulada `## Dados para o Fluxo`, com:",
      "- RESUMO: até 3 frases com os achados que precisam ser lembrados nas próximas etapas.",
    ];
    if (etapaId === "2.1") {
      linhas.push("- Uma linha `PERGUNTA:` para cada pergunta proposta, apenas com a pergunta.");
    }
    if (MAPAS_360.has(etapaId)) {
      linhas.push("- Até 3 linhas `SEQUENCIA_SUGERIDA:` com sequências férteis para close reading, incluindo minutagem ou episódio quando tiver confiança.");
    }
    if (etapaId === "r" || etapaId === "3") {
      linhas.push("- Uma linha `FONTE:` para cada fonte essencial realmente consultada ou recomendada, sem inventar URLs.");
    }
    linhas.push("Não deixe essa seção substituir nem resumir a análise pedida acima.");
    return linhas.join("\n");
  }

  function montarPromptSessao(etapaId, opcoes = {}) {
    const template = estado.templates[etapaId];
    if (!template) {
      return { texto: "Carregando o template desta etapa…", pendentes: [] };
    }
    const valores = valoresParaEtapa(etapaId, opcoes.sobrepor || {});
    const montado = substituirTemplate(template, valores);
    let texto = montado.texto;

    if (!opcoes.simples) {
      const dossie = valorDe("dossie-fontes");
      if (dossie && ["1", "1a", "1b", "1s", "2.2", "3", "4"].includes(etapaId)) {
        texto += "\n\n---\nContexto factual e fontes reunidos na sessão (use para fatos externos; não substitui as evidências formais da própria obra):\n\n"
          + dossie.slice(0, 10000);
      }
      if (sessao.incluirContexto) {
        const trechos = [];
        if (sessao.resumoLocal) trechos.push(`### Resumo consolidado\n${sessao.resumoLocal}`);
        sessao.etapas.forEach((anterior) => {
          if (anterior === etapaId) return;
          const resumo = sessao.resumos[anterior] || extrairResumo(sessao.respostas[anterior] || "");
          if (resumo) trechos.push(`### Etapa ${anterior}\n${resumo}`);
        });
        if (trechos.length) {
          texto += "\n\n---\nPacote de continuidade da sessão (use como contexto, sem repetir tudo):\n\n"
            + trechos.join("\n\n").slice(0, 12000);
        }
      }
      texto += `\n${instrucaoDadosFluxo(etapaId)}`;
    }
    return { texto, pendentes: montado.pendentes };
  }

  function montarPromptMaestro() {
    const ordem = sessao.etapas.length ? sessao.etapas : calcularOrdem(lerConfiguracao());
    const valores = valoresAtuais();
    const foco = sessao.trilha === "comparativa"
      ? [valores.OBRA_A, valores.OBRA_B].filter(Boolean).join(" × ") || "[duas obras a comparar]"
      : valores.TITULO_DA_OBRA || "[obra]";
    const partes = [
      "# Sessão guiada do Fluxo — Prompt Maestro",
      "",
      `Você será o condutor de uma análise completa de **${foco}**, usando os roteiros abaixo **um de cada vez, nesta ordem**. Não execute todas as etapas em uma única resposta.`,
      "",
      "## Como conduzir",
      "",
      "1. Comece somente pela primeira etapa do roteiro e pare ao concluí-la, dizendo qual é a próxima etapa.",
      "2. Quando eu responder “continue”, avance para a etapa seguinte sem pedir que eu cole outro prompt.",
      "3. Na Etapa 2.1, pare obrigatoriamente e espere eu escolher uma pergunta (ou formular a minha). Use exatamente essa escolha na 2.2.",
      "4. Antes da Etapa 2.3, se ela estiver no roteiro, pergunte qual sequência quero dissecar ou ofereça opções concretas.",
      "5. Mantenha as regras de rigor de cada roteiro durante toda a conversa. Diferencie fato de interpretação e marque incertezas.",
      "6. Ao fim de cada etapa, acrescente `## Dados para o Fluxo` com um item `RESUMO:`; na 2.1, repita cada opção em uma linha `PERGUNTA:`; nas análises 360°, sugira até 3 linhas `SEQUENCIA_SUGERIDA:`.",
      "7. Não pule a minha hipótese inicial: ela deve ser registrada antes da sua interpretação e retomada na síntese.",
    ];

    const dossie = valorDe("dossie-fontes");
    if (dossie) {
      partes.push(
        "",
        "## Dossiê factual já reunido",
        "",
        "Use este material para fatos externos, verificando conflitos; ele não substitui evidências da obra:",
        "",
        dossie.slice(0, 10000)
      );
    }

    ordem.forEach((etapaId) => {
      const etapa = etapaPorId(etapaId);
      let prompt = montarPromptSessao(etapaId, {
        simples: true,
        sobrepor: { DOSSE_DE_FONTES: "" },
      }).texto;
      prompt = prompt
        .replaceAll("[pergunta escolhida na Etapa 2.1]", "a pergunta que eu escolher quando você pausar após a Etapa 2.1")
        .replaceAll("[sequência escolhida para o close reading]", "a sequência que combinarmos na pausa anterior à Etapa 2.3");
      partes.push("", "---", "", `## Roteiro — Etapa ${etapaId}: ${etapa?.nome || etapaId}`, "", prompt);
    });
    partes.push("", "---", "", "Comece agora apenas pela primeira etapa do roteiro.");
    return partes.join("\n");
  }

  function etapaConcluida(etapaId) {
    return !!sessao.concluidas[etapaId];
  }

  function dependenciasFaltantes(etapaId) {
    const faltantes = [];
    const indice = sessao.etapas.indexOf(etapaId);
    const anteriores = indice >= 0 ? sessao.etapas.slice(0, indice) : [];
    if (etapaId === "1b" && !etapaConcluida("1a")) {
      faltantes.push("salvar a resposta da Etapa 1A");
    }
    if (etapaId === "2.1") {
      const mapa = [...anteriores].reverse().find((id) => MAPAS_360.has(id));
      if (mapa && !etapaConcluida(mapa)) faltantes.push(`salvar a resposta da Etapa ${mapa.toUpperCase()}`);
    }
    if (etapaId === "2.2" && !valorDe("pergunta")) {
      faltantes.push("escolher uma pergunta na Etapa 2.1 ou escrever a sua");
    }
    if (etapaId === "2.3" && !valorDe("sequencia")) {
      faltantes.push("escolher a sequência do close reading");
    }
    if (etapaId === "3" && sessao.etapas.includes("2.2") && !etapaConcluida("2.2")) {
      faltantes.push("concluir a Etapa 2.2");
    }
    return faltantes;
  }

  function statusEtapa(etapaId) {
    if (etapaConcluida(etapaId)) {
      return { codigo: "concluida", rotulo: "✓ Concluída", detalhe: "Resposta salva na sessão." };
    }
    const pendentes = montarPromptSessao(etapaId, { simples: true }).pendentes;
    if (pendentes.length) {
      return {
        codigo: "bloqueada",
        rotulo: "Faltam dados",
        detalhe: `Preencha: ${pendentes.join(", ")}.`,
      };
    }
    const dependencias = dependenciasFaltantes(etapaId);
    if (dependencias.length) {
      return {
        codigo: "bloqueada",
        rotulo: "Aguardando etapa anterior",
        detalhe: `Antes, é preciso ${dependencias.join("; ")}.`,
      };
    }
    if (sessao.enviadas[etapaId]) {
      return {
        codigo: "aguardando",
        rotulo: "Aguardando resposta",
        detalhe: "Cole a resposta da IA e salve para preparar a próxima etapa.",
      };
    }
    return {
      codigo: "pronta",
      rotulo: "Pronta",
      detalhe: "Prompt preenchido e pronto para enviar.",
    };
  }

  function proximaEtapa() {
    return sessao.etapas.find((id) => !etapaConcluida(id)) || "";
  }

  function mostrarToast(mensagem) {
    if (typeof toast === "function") toast(mensagem);
  }

  async function copiarTexto(texto, areaFallback) {
    try {
      await navigator.clipboard.writeText(texto);
      return true;
    } catch (_e) {
      if (areaFallback) {
        areaFallback.focus();
        areaFallback.select();
        try { return document.execCommand("copy"); } catch (_e2) { return false; }
      }
      return false;
    }
  }

  function abrirDestino() {
    const destino = DESTINOS_IA[sessao.iaDestino] || DESTINOS_IA.manual;
    if (!destino.url) return null;
    return window.open(destino.url, "_blank", "noopener,noreferrer");
  }

  function baixarTexto(nome, conteudo, tipo = "text/markdown;charset=utf-8") {
    const blob = new Blob([conteudo], { type: tipo });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = nome;
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function slug(texto) {
    return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      .toLocaleLowerCase("pt-BR")
      .replace(/[^a-z0-9]+/g, "-")
      .replace(/^-|-$/g, "") || "analise";
  }

  async function enviarPrompt(etapaId, prompt, area) {
    sessao = { ...sessao, ...lerConfiguracao() };
    if (sessao.provedor !== "manual") {
      return executarEtapaNoProvedor(etapaId, prompt);
    }
    const janela = abrirDestino();
    const copiado = await copiarTexto(prompt, area);
    sessao.enviadas[etapaId] = new Date().toISOString();
    salvarSessao();
    renderSessao();
    const destino = DESTINOS_IA[sessao.iaDestino] || DESTINOS_IA.manual;
    mostrarToast(copiado
      ? `Prompt da Etapa ${etapaId.toUpperCase()} copiado${janela ? ` e ${destino.nome} aberto` : ""}. Cole na conversa e depois traga a resposta.`
      : "Não consegui copiar automaticamente. Selecione o prompt e use Ctrl/Cmd+C.");
  }

  async function executarEtapaNoProvedor(etapaId, prompt) {
    atualizarStatusProvedor(`Executando a Etapa ${etapaId.toUpperCase()}…`);
    try {
      const resposta = await executarComProvedor(prompt);
      sessao.respostas[etapaId] = resposta;
      sessao.enviadas[etapaId] = new Date().toISOString();
      salvarResposta(etapaId, false);
      atualizarStatusProvedor("Resposta recebida e salva na sessão.");
      mostrarToast(`Etapa ${etapaId.toUpperCase()} executada e salva.`);
      irParaEtapa(proximaEtapa());
    } catch (erro) {
      console.error(erro);
      atualizarStatusProvedor(`Não foi possível executar: ${erro.message || erro}`);
      mostrarToast("A execução automática falhou. Você ainda pode copiar o prompt e usar o modo manual.");
    }
  }

  async function executarComProvedor(prompt) {
    if (sessao.provedor === "puter") return executarComPuter(prompt);
    if (sessao.provedor === "byok") return executarComByok(prompt);
    if (sessao.provedor === "local") return executarComLocal(prompt);
    throw new Error("O modo manual não executa chamadas; copie o prompt para sua IA.");
  }

  function carregarScript(src) {
    if (document.querySelector(`script[src="${src}"]`)) {
      return Promise.resolve();
    }
    return new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = src;
      script.async = true;
      script.onload = resolve;
      script.onerror = () => reject(new Error("Não foi possível carregar o Puter.js."));
      document.head.appendChild(script);
    });
  }

  function textoDaResposta(resposta) {
    if (typeof resposta === "string") return resposta;
    const conteudo = resposta?.message?.content ?? resposta?.content ?? resposta?.text ?? "";
    if (typeof conteudo === "string") return conteudo;
    if (Array.isArray(conteudo)) {
      return conteudo.map((item) => item.text || item.content || "").join("\n");
    }
    if (resposta?.toString && resposta.toString !== Object.prototype.toString) {
      return resposta.toString();
    }
    return "";
  }

  async function executarComPuter(prompt) {
    await carregarScript("https://js.puter.com/v2/");
    if (!window.puter?.ai?.chat) {
      throw new Error("A API do Puter não ficou disponível neste navegador.");
    }
    const modelo = sessao.provedorConfig.puterModelo;
    const opcoes = modelo ? { model: modelo } : {};
    const resposta = await window.puter.ai.chat(prompt, opcoes);
    const texto = textoDaResposta(resposta).trim();
    if (!texto) throw new Error("O Puter retornou uma resposta vazia.");
    return texto;
  }

  async function executarComByok(prompt) {
    const endpoint = sessao.provedorConfig.byokEndpoint;
    const modelo = sessao.provedorConfig.byokModelo;
    const chave = el["byok-chave"]?.value.trim();
    if (!endpoint || !modelo || !chave) {
      throw new Error("Informe endpoint, modelo e sua chave de API.");
    }
    const resposta = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${chave}`,
      },
      body: JSON.stringify({
        model: modelo,
        messages: [
          {
            role: "system",
            content: "Você é um parceiro rigoroso de análise audiovisual. Siga as instruções do usuário e não invente fatos nem fontes.",
          },
          { role: "user", content: prompt },
        ],
      }),
    });
    const dados = await resposta.json().catch(() => ({}));
    if (!resposta.ok) {
      const detalhe = dados?.error?.message || dados?.message || `HTTP ${resposta.status}`;
      throw new Error(detalhe);
    }
    const texto = textoDaResposta(dados.choices?.[0]).trim();
    if (!texto) throw new Error("O provedor retornou uma resposta vazia.");
    return texto;
  }

  async function disponibilidadeLocal() {
    if (!("LanguageModel" in window)) return "unavailable";
    try {
      return await window.LanguageModel.availability();
    } catch (_e) {
      return "unavailable";
    }
  }

  async function executarComLocal(prompt) {
    const disponibilidade = await disponibilidadeLocal();
    if (disponibilidade === "unavailable") {
      throw new Error("A Prompt API local não está disponível neste navegador/dispositivo.");
    }
    let sessaoLocal;
    try {
      sessaoLocal = await window.LanguageModel.create({
        monitor(monitor) {
          monitor.addEventListener("downloadprogress", (evento) => {
            const pct = Math.round((evento.loaded || 0) * 100);
            atualizarStatusProvedor(`Baixando o modelo local: ${pct}%`);
          });
        },
        initialPrompts: [
          {
            role: "system",
            content: "Responda em português brasileiro, com rigor e sem inventar fatos.",
          },
        ],
      });
    } catch (_e) {
      sessaoLocal = await window.LanguageModel.create();
    }
    try {
      const texto = await sessaoLocal.prompt(prompt);
      if (!String(texto || "").trim()) throw new Error("O modelo local retornou uma resposta vazia.");
      return String(texto).trim();
    } finally {
      try { sessaoLocal.destroy?.(); } catch (_e) { /* ok */ }
    }
  }

  function atualizarStatusProvedor(texto) {
    if (el["provedor-status"]) el["provedor-status"].textContent = texto;
  }

  function atualizarConfigProvedor() {
    const provedor = el.provedor?.value || "manual";
    if (el["config-puter"]) el["config-puter"].hidden = provedor !== "puter";
    if (el["config-byok"]) el["config-byok"].hidden = provedor !== "byok";
    if (el["config-local"]) el["config-local"].hidden = provedor !== "local";
  }

  function sincronizarRespostaComDossie(texto) {
    const campo = $("dossie-fontes");
    if (!campo || !texto.trim()) return;
    const atual = campo.value.trim();
    if (!atual || atual.startsWith("## Metadados de bases abertas")) {
      campo.value = atual ? `${atual}\n\n## Pesquisa externa importada\n\n${texto}` : texto;
    } else if (!atual.includes(texto.slice(0, 160))) {
      campo.value = `${atual}\n\n## Pesquisa externa importada\n\n${texto}`;
    }
    disparar(campo);
  }

  function salvarResposta(etapaId, rolar = true) {
    const area = el["sessao-etapas"].querySelector(`[data-resposta="${etapaId}"]`);
    const texto = (area?.value ?? sessao.respostas[etapaId] ?? "").trim();
    sessao.respostas[etapaId] = texto;
    sessao.concluidas[etapaId] = !!texto;
    if (!texto) {
      salvarSessao();
      renderSessao();
      return;
    }
    const dados = extrairDados(texto);
    sessao.resumos[etapaId] = dados.resumo;
    if (etapaId === "2.1" && dados.perguntas.length) {
      sessao.perguntasDetectadas = dados.perguntas;
    }
    if (MAPAS_360.has(etapaId) && dados.sequencias.length) {
      sessao.sequenciasDetectadas = unicos([
        ...sessao.sequenciasDetectadas,
        ...dados.sequencias,
      ], 6);
    }
    if (etapaId === "r") sincronizarRespostaComDossie(texto);
    salvarSessao();
    renderSessao();
    if (rolar) irParaEtapa(proximaEtapa());
  }

  function botaoSugestao(texto, acao, indice, selecionada) {
    const botao = document.createElement("button");
    botao.type = "button";
    botao.className = `sugestao-opcao${selecionada ? " selecionada" : ""}`;
    botao.dataset.acao = acao;
    botao.dataset.indice = String(indice);
    botao.textContent = texto;
    return botao;
  }

  function criarCardEtapa(etapaId) {
    const etapa = etapaPorId(etapaId);
    const status = statusEtapa(etapaId);
    const montado = montarPromptSessao(etapaId);
    const card = document.createElement("article");
    card.className = `etapa-card status-${status.codigo}`;
    card.id = `sessao-etapa-${etapaId.replace(".", "-")}`;
    card.dataset.etapa = etapaId;

    const topo = document.createElement("div");
    topo.className = "etapa-card-topo";
    const titulo = document.createElement("h3");
    const rotulo = document.createElement("small");
    rotulo.textContent = etapa?.rotulo || `Etapa ${etapaId}`;
    titulo.append(rotulo, document.createTextNode(etapa?.nome || etapaId));
    const pill = document.createElement("span");
    pill.className = `status-etapa status-${status.codigo}`;
    pill.textContent = status.rotulo;
    topo.append(titulo, pill);
    card.appendChild(topo);

    const descricao = document.createElement("p");
    descricao.className = "etapa-card-desc";
    descricao.textContent = status.detalhe;
    card.appendChild(descricao);

    const detalhes = document.createElement("details");
    detalhes.className = "etapa-prompt";
    const resumo = document.createElement("summary");
    resumo.textContent = `Ver prompt já preenchido (${montado.texto.length.toLocaleString("pt-BR")} caracteres)`;
    const promptArea = document.createElement("textarea");
    promptArea.className = "prompt-sessao";
    promptArea.rows = 12;
    promptArea.readOnly = true;
    promptArea.value = montado.texto;
    promptArea.dataset.prompt = etapaId;
    detalhes.append(resumo, promptArea);
    card.appendChild(detalhes);

    const acoes = document.createElement("div");
    acoes.className = "acoes";
    const enviar = document.createElement("button");
    enviar.type = "button";
    enviar.className = "btn btn-primario";
    enviar.dataset.acao = "enviar";
    enviar.dataset.etapa = etapaId;
    enviar.textContent = sessao.provedor === "manual"
      ? "Copiar e abrir minha IA"
      : "Executar esta etapa aqui";
    const copiar = document.createElement("button");
    copiar.type = "button";
    copiar.className = "btn";
    copiar.dataset.acao = "copiar";
    copiar.dataset.etapa = etapaId;
    copiar.textContent = "Copiar prompt";
    acoes.append(enviar, copiar);
    card.appendChild(acoes);

    if (etapaId === "2.1" && sessao.perguntasDetectadas.length) {
      const tituloSugestoes = document.createElement("p");
      tituloSugestoes.innerHTML = "<strong>Escolha uma pergunta:</strong> ela preencherá a Etapa 2.2 automaticamente.";
      const sugestoes = document.createElement("div");
      sugestoes.className = "sugestoes-detectadas";
      sessao.perguntasDetectadas.forEach((pergunta, indice) => {
        sugestoes.appendChild(botaoSugestao(
          pergunta, "pergunta", indice, pergunta === valorDe("pergunta")
        ));
      });
      card.append(tituloSugestoes, sugestoes);
    }

    if (etapaId === "2.3" && sessao.sequenciasDetectadas.length) {
      const tituloSugestoes = document.createElement("p");
      tituloSugestoes.innerHTML = "<strong>Sequências sugeridas nas respostas:</strong>";
      const sugestoes = document.createElement("div");
      sugestoes.className = "sugestoes-detectadas";
      sessao.sequenciasDetectadas.forEach((sequencia, indice) => {
        sugestoes.appendChild(botaoSugestao(
          sequencia, "sequencia", indice, sequencia === valorDe("sequencia")
        ));
      });
      card.append(tituloSugestoes, sugestoes);
    }

    if (etapaId === "2.2" && !valorDe("pergunta")) {
      const tituloManual = document.createElement("p");
      tituloManual.innerHTML = "<strong>Sua pergunta:</strong> selecione uma na Etapa 2.1 ou escreva a sua aqui.";
      const labelManual = document.createElement("label");
      labelManual.className = "campo";
      labelManual.textContent = "Pergunta escolhida";
      const entrada = document.createElement("textarea");
      entrada.rows = 3;
      entrada.dataset.dadoManual = "pergunta";
      entrada.placeholder = "Ex.: Como a montagem transforma em espetáculo aquilo que o filme critica?";
      const usar = document.createElement("button");
      usar.type = "button";
      usar.className = "btn";
      usar.dataset.acao = "definir-manual";
      usar.dataset.campo = "pergunta";
      usar.textContent = "Usar esta pergunta";
      labelManual.appendChild(entrada);
      card.append(tituloManual, labelManual, usar);
    }

    if (etapaId === "2.3" && !valorDe("sequencia")) {
      const tituloManual = document.createElement("p");
      tituloManual.innerHTML = "<strong>Sua sequência:</strong> escolha uma sugestão ou descreva o trecho com minutagem/episódio.";
      const labelManual = document.createElement("label");
      labelManual.className = "campo";
      labelManual.textContent = "Sequência para o close reading";
      const entrada = document.createElement("textarea");
      entrada.rows = 3;
      entrada.dataset.dadoManual = "sequencia";
      entrada.placeholder = "Ex.: Abertura — perseguição ao frango (≈0:00–3:30) ou T1:E3, cena do interrogatório.";
      const usar = document.createElement("button");
      usar.type = "button";
      usar.className = "btn";
      usar.dataset.acao = "definir-manual";
      usar.dataset.campo = "sequencia";
      usar.textContent = "Usar esta sequência";
      labelManual.appendChild(entrada);
      card.append(tituloManual, labelManual, usar);
    }

    const label = document.createElement("label");
    label.className = "campo espacado";
    label.textContent = etapaId === "r"
      ? "Dossiê ou resposta da pesquisa"
      : "Resposta da IA";
    const resposta = document.createElement("textarea");
    resposta.className = "resposta-sessao";
    resposta.rows = 9;
    resposta.dataset.resposta = etapaId;
    resposta.placeholder = "Cole aqui a resposta recebida. Ao salvar, o Fluxo identifica resumos, perguntas e sequências para preparar as próximas etapas.";
    resposta.value = sessao.respostas[etapaId] || "";
    label.appendChild(resposta);
    card.appendChild(label);

    const acoesResposta = document.createElement("div");
    acoesResposta.className = "acoes";
    const salvar = document.createElement("button");
    salvar.type = "button";
    salvar.className = "btn";
    salvar.dataset.acao = "salvar";
    salvar.dataset.etapa = etapaId;
    salvar.textContent = "Salvar resposta e preparar a próxima";
    const concluirSemColar = document.createElement("button");
    concluirSemColar.type = "button";
    concluirSemColar.className = "btn btn-suave";
    concluirSemColar.dataset.acao = "concluir-sem-resposta";
    concluirSemColar.dataset.etapa = etapaId;
    concluirSemColar.textContent = "Já fiz na IA (não colar)";
    const limpar = document.createElement("button");
    limpar.type = "button";
    limpar.className = "btn btn-suave";
    limpar.dataset.acao = "limpar-resposta";
    limpar.dataset.etapa = etapaId;
    limpar.textContent = "Limpar";
    acoesResposta.append(salvar, concluirSemColar, limpar);
    card.appendChild(acoesResposta);
    return card;
  }

  function renderSessao() {
    atualizarComparativa();
    atualizarConfigProvedor();
    el["sessao-card"].hidden = !sessao.criada;
    if (!sessao.criada) return;

    const maestro = sessao.modo === "maestro";
    if (el["painel-maestro"]) el["painel-maestro"].hidden = !maestro;
    if (el["sessao-etapas"]) el["sessao-etapas"].hidden = maestro;

    const concluidas = sessao.etapas.filter(etapaConcluida).length;
    const total = sessao.etapas.length || 1;
    const percentual = maestro
      ? ((el["transcricao-maestro"]?.value || "").trim() ? 100 : 0)
      : Math.round((concluidas / total) * 100);
    if (el["sessao-progresso"]) el["sessao-progresso"].value = percentual;
    if (el["sessao-progresso-texto"]) {
      el["sessao-progresso-texto"].textContent = maestro
        ? "Conversa única"
        : `${concluidas} de ${total} etapas concluídas`;
    }

    if (maestro) {
      el["proxima-acao"].textContent = "Copiar o Prompt Maestro e iniciar a conversa na sua IA. Depois, basta responder às pausas dela.";
      el["btn-proxima-acao"].textContent = "Ir para o Prompt Maestro";
      el["prompt-maestro"].value = montarPromptMaestro();
    } else {
      const proxima = proximaEtapa();
      if (!proxima) {
        el["proxima-acao"].textContent = "Sessão concluída. Exporte o dossiê em Markdown ou a sessão em JSON para guardar e retomar depois.";
        el["btn-proxima-acao"].textContent = "Exportar dossiê";
      } else {
        const etapa = etapaPorId(proxima);
        const status = statusEtapa(proxima);
        el["proxima-acao"].textContent = `${etapa?.rotulo || proxima} — ${etapa?.nome || ""}. ${status.detalhe}`;
        el["btn-proxima-acao"].textContent = "Ir para a próxima etapa";
      }
      el["sessao-etapas"].innerHTML = "";
      sessao.etapas.forEach((etapaId) => {
        el["sessao-etapas"].appendChild(criarCardEtapa(etapaId));
      });
    }
  }

  function agendarRender() {
    clearTimeout(temporizadorRender);
    temporizadorRender = setTimeout(() => {
      if (sessao.criada) renderSessao();
    }, 450);
  }

  function irParaEtapa(etapaId) {
    if (sessao.modo === "maestro") {
      el["painel-maestro"]?.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    if (!etapaId) {
      el["sessao-card"].scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }
    const card = $(`sessao-etapa-${etapaId.replace(".", "-")}`);
    if (card) {
      card.scrollIntoView({ behavior: "smooth", block: "start" });
      setTimeout(() => card.querySelector("[data-acao='enviar']")?.focus(), 450);
    }
  }

  function montarSessao(rolar = true) {
    aplicarPadroes();
    const config = lerConfiguracao();
    sessao = {
      ...sessao,
      ...config,
      criada: true,
      etapas: calcularOrdem(config),
    };
    salvarSessao();
    renderSessao();
    if (rolar) {
      if (sessao.modo === "maestro") irParaEtapa("");
      else irParaEtapa(proximaEtapa());
    }
    mostrarToast("Sessão montada: todas as etapas relevantes já foram preenchidas com os seus dados.");
  }

  function focoDaSessao() {
    if (sessao.trilha === "comparativa") {
      return [valorDe("obra-a"), valorDe("obra-b")].filter(Boolean).join(" × ") || "comparativa";
    }
    return valorDe("titulo") || "analise";
  }

  function exportarMarkdown() {
    const linhas = [
      `# Dossiê do Fluxo — ${focoDaSessao()}`,
      "",
      `- Trilha: ${sessao.trilha}`,
      `- Modo de condução: ${sessao.modo === "maestro" ? "Conversa única (Prompt Maestro)" : "Guiada no Fluxo"}`,
      `- Objetivo: ${valorDe("objetivo") || "—"}`,
      `- Hipótese inicial: ${valorDe("impressoes") || "—"}`,
      "",
    ];
    const dossie = valorDe("dossie-fontes");
    if (dossie) linhas.push("## Dossiê de fontes", "", dossie, "");
    if (sessao.modo === "maestro") {
      linhas.push("## Prompt Maestro", "", el["prompt-maestro"].value || montarPromptMaestro(), "");
      const transcricao = el["transcricao-maestro"]?.value.trim();
      if (transcricao) linhas.push("## Transcrição/síntese da conversa", "", transcricao, "");
    } else {
      sessao.etapas.forEach((etapaId) => {
        const etapa = etapaPorId(etapaId);
        linhas.push(
          `## ${etapa?.rotulo || etapaId} — ${etapa?.nome || etapaId}`,
          "",
          "### Prompt",
          "",
          montarPromptSessao(etapaId).texto,
          "",
          "### Resposta",
          "",
          sessao.respostas[etapaId] || "_(sem resposta registrada)_",
          ""
        );
      });
    }
    baixarTexto(`${slug(focoDaSessao())}-sessao-fluxo.md`, linhas.join("\n"));
  }

  function exportarJson() {
    const campos = {};
    IDS_CAMPOS.forEach((id) => { campos[id] = $(id)?.value || ""; });
    const payload = {
      formato: "fluxo-sessao",
      versao: 1,
      exportadoEm: new Date().toISOString(),
      campos,
      sessao,
    };
    baixarTexto(
      `${slug(focoDaSessao())}-sessao-fluxo.json`,
      `${JSON.stringify(payload, null, 2)}\n`,
      "application/json;charset=utf-8"
    );
  }

  async function importarJson(arquivo) {
    try {
      const dados = JSON.parse(await arquivo.text());
      if (!dados || typeof dados !== "object" || !dados.sessao) {
        throw new Error("Arquivo de sessão inválido.");
      }
      Object.entries(dados.campos || {}).forEach(([id, valor]) => {
        if ($(id) && typeof valor === "string") definirValor(id, valor);
      });
      sessao = {
        ...novaSessao(),
        ...dados.sessao,
        provedorConfig: {
          ...novaSessao().provedorConfig,
          ...(dados.sessao.provedorConfig || {}),
        },
      };
      sincronizarControles();
      salvarSessao();
      renderSessao();
      mostrarToast("Sessão importada com sucesso.");
    } catch (erro) {
      console.error(erro);
      mostrarToast(`Não foi possível importar: ${erro.message || erro}`);
    }
  }

  el["btn-montar-sessao"].addEventListener("click", () => montarSessao(true));
  $("btn-exemplo")?.addEventListener("click", () => {
    setTimeout(() => {
      definirValor("trilha", "padrao");
      montarSessao(true);
    }, 0);
  });
  $("btn-limpar")?.addEventListener("click", () => {
    sessao = novaSessao();
    try { localStorage.removeItem(CHAVE_SESSAO); } catch (_e) { /* ok */ }
    sincronizarControles();
    renderSessao();
  });

  [
    "trilha", "ia-destino", "incluir-pesquisa", "incluir-close",
    "incluir-contexto", "modo-sessao-guiada", "modo-sessao-maestro",
    "provedor", "puter-modelo", "byok-endpoint", "byok-modelo",
  ].forEach((id) => {
    $(id)?.addEventListener("change", () => {
      const config = lerConfiguracao();
      const mudouRota = config.trilha !== sessao.trilha
        || config.incluirPesquisa !== sessao.incluirPesquisa
        || config.incluirClose !== sessao.incluirClose;
      sessao = { ...sessao, ...config };
      if (sessao.criada && mudouRota) sessao.etapas = calcularOrdem(sessao);
      salvarSessao();
      atualizarComparativa();
      atualizarConfigProvedor();
      renderSessao();
    });
  });

  el["byok-chave"]?.addEventListener("input", () => {
    try {
      if (el["byok-lembrar"]?.checked) sessionStorage.setItem(CHAVE_BYOK, el["byok-chave"].value);
      else sessionStorage.removeItem(CHAVE_BYOK);
    } catch (_e) { /* apenas em memória */ }
  });
  el["byok-lembrar"]?.addEventListener("change", () => {
    try {
      if (el["byok-lembrar"].checked) sessionStorage.setItem(CHAVE_BYOK, el["byok-chave"].value);
      else sessionStorage.removeItem(CHAVE_BYOK);
    } catch (_e) { /* ok */ }
  });

  Object.values(CAMPOS).forEach((campo) => {
    $(campo.id)?.addEventListener("input", agendarRender);
  });
  $("stepper")?.addEventListener("click", () => setTimeout(atualizarComparativa, 0));

  el["sessao-etapas"].addEventListener("input", (evento) => {
    const area = evento.target.closest("[data-resposta]");
    if (!area) return;
    sessao.respostas[area.dataset.resposta] = area.value;
    salvarSessao();
  });

  el["sessao-etapas"].addEventListener("click", async (evento) => {
    const botao = evento.target.closest("[data-acao]");
    if (!botao) return;
    const acao = botao.dataset.acao;
    const etapaId = botao.dataset.etapa;

    if (acao === "pergunta") {
      const pergunta = sessao.perguntasDetectadas[Number(botao.dataset.indice)];
      if (pergunta) {
        definirValor("pergunta", pergunta);
        renderSessao();
        irParaEtapa("2.2");
      }
      return;
    }
    if (acao === "sequencia") {
      const sequencia = sessao.sequenciasDetectadas[Number(botao.dataset.indice)];
      if (sequencia) {
        definirValor("sequencia", sequencia);
        renderSessao();
        irParaEtapa("2.3");
      }
      return;
    }
    if (acao === "definir-manual") {
      const campo = botao.dataset.campo;
      const area = el["sessao-etapas"].querySelector(`[data-dado-manual="${campo}"]`);
      const texto = area?.value.trim() || "";
      if (!texto) {
        mostrarToast(campo === "pergunta"
          ? "Escreva ou selecione uma pergunta para continuar."
          : "Descreva uma sequência para continuar.");
        area?.focus();
        return;
      }
      definirValor(campo, texto);
      renderSessao();
      irParaEtapa(campo === "pergunta" ? "2.2" : "2.3");
      return;
    }
    if (!etapaId) return;
    const promptArea = el["sessao-etapas"].querySelector(`[data-prompt="${etapaId}"]`);
    if (acao === "enviar") {
      await enviarPrompt(etapaId, promptArea?.value || montarPromptSessao(etapaId).texto, promptArea);
    } else if (acao === "copiar") {
      const copiado = await copiarTexto(promptArea?.value || "", promptArea);
      mostrarToast(copiado ? "Prompt copiado." : "Selecione o prompt e copie manualmente.");
    } else if (acao === "salvar") {
      salvarResposta(etapaId, true);
      mostrarToast("Resposta salva. A próxima etapa já está preparada.");
    } else if (acao === "concluir-sem-resposta") {
      sessao.concluidas[etapaId] = true;
      salvarSessao();
      renderSessao();
      irParaEtapa(proximaEtapa());
    } else if (acao === "limpar-resposta") {
      sessao.respostas[etapaId] = "";
      sessao.concluidas[etapaId] = false;
      sessao.resumos[etapaId] = "";
      salvarSessao();
      renderSessao();
    }
  });

  el["btn-proxima-acao"]?.addEventListener("click", () => {
    if (sessao.modo !== "maestro" && !proximaEtapa()) {
      exportarMarkdown();
      return;
    }
    irParaEtapa(proximaEtapa());
  });

  el["btn-copiar-maestro"]?.addEventListener("click", async () => {
    const copiado = await copiarTexto(el["prompt-maestro"].value, el["prompt-maestro"]);
    mostrarToast(copiado ? "Prompt Maestro copiado." : "Selecione o texto e copie manualmente.");
  });
  el["btn-enviar-maestro"]?.addEventListener("click", async () => {
    sessao = { ...sessao, ...lerConfiguracao() };
    const janela = abrirDestino();
    const copiado = await copiarTexto(el["prompt-maestro"].value, el["prompt-maestro"]);
    sessao.enviadas.maestro = new Date().toISOString();
    salvarSessao();
    mostrarToast(copiado
      ? `Prompt Maestro copiado${janela ? " e sua IA foi aberta" : ""}. Cole uma única vez e siga as pausas da conversa.`
      : "Não consegui copiar automaticamente. Selecione o Prompt Maestro e copie manualmente.");
  });
  el["transcricao-maestro"]?.addEventListener("input", () => {
    sessao.transcricaoMaestro = el["transcricao-maestro"].value;
    salvarSessao();
    const pct = sessao.transcricaoMaestro.trim() ? 100 : 0;
    if (el["sessao-progresso"]) el["sessao-progresso"].value = pct;
  });

  el["btn-testar-provedor"]?.addEventListener("click", async () => {
    sessao = { ...sessao, ...lerConfiguracao() };
    salvarSessao();
    atualizarConfigProvedor();
    if (sessao.provedor === "manual") {
      atualizarStatusProvedor("Modo manual ativo: nenhum teste é necessário.");
      return;
    }
    if (sessao.provedor === "local") {
      const disponibilidade = await disponibilidadeLocal();
      atualizarStatusProvedor(`IA local: ${disponibilidade}.`);
      return;
    }
    atualizarStatusProvedor("Testando o provedor…");
    try {
      const resposta = await executarComProvedor("Responda somente: conexão ok.");
      atualizarStatusProvedor(`Provedor respondeu: ${resposta.slice(0, 90)}`);
    } catch (erro) {
      atualizarStatusProvedor(`Falha no teste: ${erro.message || erro}`);
    }
  });

  el["btn-resumir-local"]?.addEventListener("click", async () => {
    const respostas = sessao.etapas
      .map((id) => sessao.respostas[id])
      .filter(Boolean);
    if (!respostas.length) {
      atualizarStatusProvedor("Salve ao menos uma resposta antes de resumir.");
      return;
    }
    const base = respostas.map((texto) => extrairResumo(texto) || texto.slice(0, 2500)).join("\n\n");
    atualizarStatusProvedor("Gerando resumo de continuidade…");
    try {
      sessao.resumoLocal = await executarComLocal(
        `Resuma em até 180 palavras os achados essenciais desta sessão de análise audiovisual, preservando incertezas:\n\n${base.slice(0, 9000)}`
      );
      atualizarStatusProvedor("Resumo local salvo e disponível no pacote de contexto.");
    } catch (erro) {
      sessao.resumoLocal = base.slice(0, 1400);
      atualizarStatusProvedor(`IA local indisponível (${erro.message || erro}). Usei um resumo extrativo simples.`);
    }
    salvarSessao();
    renderSessao();
  });

  el["btn-exportar-sessao-md"]?.addEventListener("click", exportarMarkdown);
  el["btn-exportar-sessao-json"]?.addEventListener("click", exportarJson);
  el["importar-sessao"]?.addEventListener("change", () => {
    const arquivo = el["importar-sessao"].files?.[0];
    if (arquivo) importarJson(arquivo);
    el["importar-sessao"].value = "";
  });
  el["btn-resetar-sessao"]?.addEventListener("click", () => {
    const config = lerConfiguracao();
    sessao = { ...novaSessao(), ...config, criada: true, etapas: calcularOrdem(config) };
    salvarSessao();
    sincronizarControles();
    renderSessao();
    mostrarToast("Respostas apagadas. Os dados da obra foram mantidos.");
  });

  sincronizarControles();
  renderSessao();

  if (!estado.carregado) {
    const esperaTemplates = setInterval(() => {
      if (estado.carregado) {
        clearInterval(esperaTemplates);
        renderSessao();
      }
    }, 400);
  }

  window.FluxoSessao = {
    montar: () => montarSessao(false),
    estado: () => JSON.parse(JSON.stringify(sessao)),
    promptMaestro: montarPromptMaestro,
  };
})();
