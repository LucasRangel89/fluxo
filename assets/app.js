"use strict";

/* ============================================================================
   Fluxo — interface web (Fases 2 e 3)

   Lê os templates de `prompts/` em tempo real (mesma fonte da CLI), extrai o
   prompt entre os marcadores HTML e preenche os placeholders a partir do
   formulário. Os campos extras exibidos por etapa são derivados dos
   placeholders que o template daquela etapa realmente usa.
   A lista ETAPAS abaixo espelha `src/fluxo/core.py` — se mudar um lado,
   mude o outro (tests/test_web.py verifica a consistência).
   ========================================================================== */

const MARCADOR_INICIO = "<!-- INICIO DO PROMPT -->";
const MARCADOR_FIM = "<!-- FIM DO PROMPT -->";
const RE_PLACEHOLDER = /\{\{\s*([A-Z0-9_]+)\s*\}\}/g;

/* Placeholder do template -> campo do formulário + rótulos amigáveis. */
const CAMPOS = {
  TITULO_DA_OBRA: {
    id: "titulo",
    rotulo: "título da obra",
    pendente: "[título da obra]",
  },
  DIRETOR_OU_CRIADOR: {
    id: "diretor",
    rotulo: "diretor(a)/criador(a)",
    pendente: "[diretor(a)/criador(a)]",
  },
  TIPO_DE_OBRA: {
    id: "tipo",
    rotulo: "tipo da obra",
    pendente: "[tipo da obra]",
  },
  META_DA_ANALISE: {
    id: "objetivo",
    rotulo: "seu objetivo",
    pendente: "[seu objetivo com a análise]",
  },
  NIVEL_DO_USUARIO: {
    id: "nivel",
    rotulo: "seu nível",
    pendente: "[seu nível de familiaridade]",
  },
  IMPRESSOES_INICIAIS: {
    id: "impressoes",
    rotulo: "suas impressões iniciais",
    pendente: "[suas impressões e hipótese iniciais]",
  },
  PERGUNTA_ESCOLHIDA: {
    id: "pergunta",
    rotulo: "pergunta escolhida",
    pendente: "[pergunta escolhida na Etapa 2.1]",
  },
  SEQUENCIA_ESCOLHIDA: {
    id: "sequencia",
    rotulo: "sequência escolhida",
    pendente: "[sequência escolhida para o close reading]",
  },
};

const IDS_CAMPOS = Object.values(CAMPOS).map((c) => c.id);

const ETAPAS = [
  {
    id: "0",
    rotulo: "Etapa 0",
    nome: "Preparação",
    arquivo: "prompts/etapa-00-preparacao.md",
    saida: "00-prompt-preparacao.md",
    descricao:
      "Preparação (opcional, mas recomendada): identifica a obra, registra a sua hipótese ANTES de a IA opinar e calibra a conversa ao seu objetivo e nível.",
    extras: ["TIPO_DE_OBRA", "META_DA_ANALISE", "NIVEL_DO_USUARIO", "IMPRESSOES_INICIAIS"],
  },
  {
    id: "1",
    rotulo: "Etapa 1",
    nome: "Análise 360°",
    arquivo: "prompts/etapa-01-analise-360.md",
    saida: "01-prompt-analise-360.md",
    descricao:
      "O raio-x completo da obra em 7 dimensões — da produção à recepção — numa única resposta. Prefere mais profundidade por dimensão? Use 1A + 1B no lugar desta.",
    extras: [],
  },
  {
    id: "1a",
    rotulo: "Etapa 1A",
    nome: "Texto (1º tempo)",
    arquivo: "prompts/etapa-01a-analise-texto.md",
    saida: "01a-prompt-analise-360-texto.md",
    descricao:
      "Alternativa em dois tempos à Etapa 1: só o texto da obra — narrativa, imagem, som e montagem (dimensões 2 a 5). Continue com a 1B na mesma conversa.",
    extras: [],
  },
  {
    id: "1b",
    rotulo: "Etapa 1B",
    nome: "Contexto (2º tempo)",
    arquivo: "prompts/etapa-01b-analise-contexto.md",
    saida: "01b-prompt-analise-360-contexto.md",
    descricao:
      "Segundo tempo: produção, sociocultural e recepção (dimensões 1, 6 e 7), conectados ao texto — e a tabela-resumo completa das 7 dimensões.",
    extras: [],
  },
  {
    id: "2.1",
    rotulo: "Etapa 2.1",
    nome: "Proposta de aprofundamento",
    arquivo: "prompts/etapa-02.1-proposta-aprofundamento.md",
    saida: "02.1-prompt-proposta-aprofundamento.md",
    descricao:
      "Na mesma conversa, a IA propõe de 3 a 5 perguntas analíticas. Escolha uma (ou formule a sua) para a próxima etapa.",
    extras: [],
  },
  {
    id: "2.2",
    rotulo: "Etapa 2.2",
    nome: "Análise focada",
    arquivo: "prompts/etapa-02.2-analise-focada.md",
    saida: "02.2-prompt-analise-focada.md",
    descricao:
      "Mergulho na pergunta escolhida: tese, evidências, contra-argumento e contexto. Pode repetir com outras perguntas da lista.",
    extras: ["PERGUNTA_ESCOLHIDA"],
  },
  {
    id: "2.3",
    rotulo: "Etapa 2.3",
    nome: "Close reading",
    arquivo: "prompts/etapa-02.3-close-reading.md",
    saida: "02.3-prompt-close-reading.md",
    descricao:
      "Opcional: uma única sequência dissecada plano a plano — decupagem, mise-en-scène, som, montagem e o sentido que a forma constrói.",
    extras: ["SEQUENCIA_ESCOLHIDA"],
  },
  {
    id: "3",
    rotulo: "Etapa 3",
    nome: "Síntese e conexões",
    arquivo: "prompts/etapa-03-sintese-conexoes.md",
    saida: "03-prompt-sintese-conexoes.md",
    descricao:
      "Fechamento do ciclo: síntese, balanço crítico, obras em diálogo, reflexões (com o antes/depois da sua leitura), fontes e a ficha-resumo.",
    extras: [],
  },
];

const EXEMPLO = {
  titulo: "Cidade de Deus (2002)",
  diretor: "Fernando Meirelles e Kátia Lund",
  tipo: "Filme (longa-metragem de ficção)",
  objetivo: "Estudar a fundo um clássico do cinema brasileiro",
  nivel: "Intermediário — leio críticas e quero aprofundar a técnica",
  impressoes:
    "Na primeira vez que vi, achei a violência espetacularizada demais, quase um videoclipe. Hoje desconfio que a forma acelerada é justamente o tema — mas ainda não sei dizer se o filme critica ou celebra esse mundo.",
  pergunta:
    "De que forma a montagem acelerada e fragmentada, combinada à narração em off de Buscapé, transforma a violência em espetáculo — e como o filme lida com a tensão ética entre estetizar essa violência e, ao mesmo tempo, criticá-la?",
  sequencia:
    "A abertura completa: a faca sendo amolada, a fuga e a perseguição ao frango, até o plano em que Buscapé fica preso entre o bando de Zé Pequeno e a polícia (≈0:00–3:30)",
};

const CHAVE_STORAGE = "fluxo-ui-v1";

/* ---------------- Estado e elementos ---------------- */

const estado = {
  etapaAtual: "0",
  templates: {},
  carregado: false,
  editadoManualmente: false,
  copiadas: new Set(),
};

const el = {};
[
  ...IDS_CAMPOS,
  "saida", "stepper", "etapa-desc", "contador", "pendencias", "dica-edicao",
  "aviso-erro", "toast", "btn-copiar", "btn-baixar", "btn-exemplo",
  "btn-limpar", "btn-regenerar",
].forEach((id) => { el[id] = document.getElementById(id); });

/* ---------------- Núcleo (mesma lógica da CLI) ---------------- */

function extrairPrompt(md) {
  const ini = md.indexOf(MARCADOR_INICIO);
  const fim = md.indexOf(MARCADOR_FIM);
  if (ini === -1 || fim === -1 || fim < ini) {
    throw new Error("Template sem os marcadores de prompt.");
  }
  return md.slice(ini + MARCADOR_INICIO.length, fim).trim();
}

function etapaAtual() {
  return ETAPAS.find((e) => e.id === estado.etapaAtual);
}

function valorCampo(chave) {
  const campo = CAMPOS[chave];
  if (!campo || !el[campo.id]) return "";
  return el[campo.id].value.trim();
}

function montarPrompt() {
  const template = estado.templates[estado.etapaAtual] || "";
  const pendentes = [];
  const texto = template.replace(RE_PLACEHOLDER, (_trecho, chave) => {
    const valor = valorCampo(chave);
    if (valor) return valor;
    const info = CAMPOS[chave];
    if (info && !pendentes.includes(info.rotulo)) pendentes.push(info.rotulo);
    return info ? info.pendente : "[" + chave + "]";
  });
  return { texto, pendentes };
}

/* Quais campos extras a etapa atual precisa?
   Derivados do próprio template (fonte única); antes do carregamento,
   vale a lista `extras` da configuração. */
function camposExtrasVisiveis() {
  const etapa = etapaAtual();
  const template = estado.templates[etapa.id];
  if (!template) return etapa.extras || [];
  return Object.keys(CAMPOS).filter((chave) =>
    new RegExp("\\{\\{\\s*" + chave + "\\s*\\}\\}").test(template)
  );
}

/* ---------------- Renderização ---------------- */

function atualizarMeta(montado) {
  const texto = el.saida.value;
  el.contador.textContent =
    texto.length > 0
      ? texto.length.toLocaleString("pt-BR") + " caracteres"
      : "";

  let pendentes = [];
  if (estado.editadoManualmente) {
    pendentes = Object.values(CAMPOS)
      .filter((c) => texto.includes(c.pendente))
      .map((c) => c.rotulo);
  } else if (montado) {
    pendentes = montado.pendentes;
  }

  if (pendentes.length > 0) {
    el.pendencias.textContent =
      "⚠️ Ainda falta preencher: " + pendentes.join(", ") +
      ". Os trechos entre colchetes no prompt marcam o lugar.";
    el.pendencias.hidden = false;
  } else {
    el.pendencias.hidden = true;
  }
}

function render() {
  const etapa = etapaAtual();
  el["etapa-desc"].textContent = etapa.descricao;

  const visiveis = camposExtrasVisiveis();
  document.querySelectorAll("[data-campo]").forEach((div) => {
    div.hidden = !visiveis.includes(div.dataset.campo);
  });

  document.querySelectorAll(".passo").forEach((btn) => {
    const id = btn.dataset.etapa;
    btn.setAttribute("aria-pressed", String(id === etapa.id));
    const feito = btn.querySelector(".feito");
    if (feito) feito.hidden = !estado.copiadas.has(id);
  });

  if (!estado.carregado) return;

  const montado = montarPrompt();
  if (!estado.editadoManualmente) {
    el.saida.value = montado.texto;
  }
  el["dica-edicao"].hidden = !estado.editadoManualmente;
  atualizarMeta(montado);
}

function construirStepper() {
  el.stepper.innerHTML = "";
  ETAPAS.forEach((etapa) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "passo";
    btn.dataset.etapa = etapa.id;
    btn.innerHTML =
      '<span class="feito" hidden>✓</span><small>' + etapa.rotulo +
      '</small><span class="passo-nome">' + etapa.nome + "</span>";
    btn.addEventListener("click", () => {
      estado.etapaAtual = etapa.id;
      estado.editadoManualmente = false;
      salvar();
      render();
    });
    el.stepper.appendChild(btn);
  });
}

/* ---------------- Persistência (localStorage) ---------------- */

function salvar() {
  try {
    const dados = {
      etapaAtual: estado.etapaAtual,
      copiadas: Array.from(estado.copiadas),
    };
    IDS_CAMPOS.forEach((id) => { dados[id] = el[id] ? el[id].value : ""; });
    localStorage.setItem(CHAVE_STORAGE, JSON.stringify(dados));
  } catch (_e) { /* navegador sem storage: segue o jogo */ }
}

function restaurar() {
  try {
    const bruto = localStorage.getItem(CHAVE_STORAGE);
    if (!bruto) return;
    const dados = JSON.parse(bruto);
    IDS_CAMPOS.forEach((id) => {
      if (dados[id] && el[id]) el[id].value = dados[id];
    });
    if (ETAPAS.some((e) => e.id === dados.etapaAtual)) {
      estado.etapaAtual = dados.etapaAtual;
    }
    (dados.copiadas || []).forEach((id) => estado.copiadas.add(id));
  } catch (_e) { /* dados corrompidos: começa do zero */ }
}

/* ---------------- Ações ---------------- */

let toastTimer = null;
function toast(mensagem) {
  el.toast.textContent = mensagem;
  el.toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.toast.hidden = true; }, 3600);
}

async function copiar() {
  const texto = el.saida.value;
  if (!texto) return;

  let ok = false;
  try {
    await navigator.clipboard.writeText(texto);
    ok = true;
  } catch (_e) {
    el.saida.select();
    try { ok = document.execCommand("copy"); } catch (_e2) { ok = false; }
    el.saida.setSelectionRange(0, 0);
  }

  if (ok) {
    estado.copiadas.add(estado.etapaAtual);
    salvar();
    render();
    const temPendente = Object.values(CAMPOS).some((c) =>
      texto.includes(c.pendente)
    );
    toast(
      temPendente
        ? "Copiado! ⚠️ Atenção: ainda há trechos por preencher (entre colchetes)."
        : "Prompt copiado! 🎬 Cole na sua IA — e lembre: todas as etapas na mesma conversa."
    );
  } else {
    toast("Não consegui copiar automaticamente. O texto está selecionado: use Ctrl+C (ou ⌘C).");
    el.saida.select();
  }
}

function baixar() {
  const etapa = etapaAtual();
  const blob = new Blob([el.saida.value + "\n"], {
    type: "text/markdown;charset=utf-8",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = etapa.saida;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  toast("Arquivo " + etapa.saida + " baixado.");
}

/* ---------------- Carregamento dos templates ---------------- */

async function carregarTemplates() {
  el.saida.value = "Carregando os templates de prompts/ ...";
  try {
    const respostas = await Promise.all(
      ETAPAS.map((e) => fetch(e.arquivo))
    );
    if (respostas.some((r) => !r.ok)) {
      throw new Error("Resposta HTTP inesperada ao buscar os templates.");
    }
    const textos = await Promise.all(respostas.map((r) => r.text()));
    ETAPAS.forEach((e, i) => {
      estado.templates[e.id] = extrairPrompt(textos[i]);
    });
    estado.carregado = true;
    render();
  } catch (erro) {
    console.error(erro);
    el["aviso-erro"].hidden = false;
    el.saida.value = "";
    atualizarMeta(null);
  }
}

/* ---------------- Eventos e inicialização ---------------- */

IDS_CAMPOS.forEach((id) => {
  if (!el[id]) return;
  el[id].addEventListener("input", () => {
    salvar();
    render();
  });
});

el.saida.addEventListener("input", () => {
  estado.editadoManualmente = true;
  el["dica-edicao"].hidden = false;
  atualizarMeta(null);
});

el["btn-copiar"].addEventListener("click", copiar);
el["btn-baixar"].addEventListener("click", baixar);

el["btn-regenerar"].addEventListener("click", () => {
  estado.editadoManualmente = false;
  render();
  toast("Prompt regerado a partir dos campos.");
});

el["btn-exemplo"].addEventListener("click", () => {
  IDS_CAMPOS.forEach((id) => {
    if (el[id] && EXEMPLO[id]) el[id].value = EXEMPLO[id];
  });
  estado.editadoManualmente = false;
  salvar();
  render();
  toast("Exemplo carregado: Cidade de Deus (2002). Experimente cada etapa!");
});

el["btn-limpar"].addEventListener("click", () => {
  IDS_CAMPOS.forEach((id) => { if (el[id]) el[id].value = ""; });
  estado.copiadas.clear();
  estado.etapaAtual = "0";
  estado.editadoManualmente = false;
  try { localStorage.removeItem(CHAVE_STORAGE); } catch (_e) { /* ok */ }
  render();
  el.titulo.focus();
  toast("Tudo limpo — pronta para uma nova análise.");
});

construirStepper();
restaurar();
render();
carregarTemplates();
