"use strict";

/* ============================================================================
   Fluxo — interface web (Fase 2)

   Lê os templates de `prompts/` em tempo real (mesma fonte da CLI), extrai o
   prompt entre os marcadores HTML e preenche os placeholders a partir do
   formulário. A lista ETAPAS abaixo espelha `src/fluxo/core.py` — se mudar
   um lado, mude o outro (tests/test_web.py verifica a consistência).
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
  PERGUNTA_ESCOLHIDA: {
    id: "pergunta",
    rotulo: "pergunta escolhida",
    pendente: "[pergunta escolhida na Etapa 2.1]",
  },
};

const ETAPAS = [
  {
    id: "1",
    rotulo: "Etapa 1",
    nome: "Análise 360°",
    arquivo: "prompts/etapa-01-analise-360.md",
    saida: "01-prompt-analise-360.md",
    descricao:
      "O raio-x completo da obra em 7 dimensões — da produção à recepção. Comece por aqui, em uma conversa nova com a IA.",
  },
  {
    id: "2.1",
    rotulo: "Etapa 2.1",
    nome: "Proposta de aprofundamento",
    arquivo: "prompts/etapa-02.1-proposta-aprofundamento.md",
    saida: "02.1-prompt-proposta-aprofundamento.md",
    descricao:
      "Na mesma conversa, a IA propõe de 3 a 5 perguntas analíticas. Escolha uma (ou formule a sua) para a próxima etapa.",
  },
  {
    id: "2.2",
    rotulo: "Etapa 2.2",
    nome: "Análise focada",
    arquivo: "prompts/etapa-02.2-analise-focada.md",
    saida: "02.2-prompt-analise-focada.md",
    descricao:
      "Mergulho na pergunta escolhida: tese, evidências, contra-argumento e contexto. Pode repetir com outras perguntas da lista.",
  },
  {
    id: "3",
    rotulo: "Etapa 3",
    nome: "Síntese e conexões",
    arquivo: "prompts/etapa-03-sintese-conexoes.md",
    saida: "03-prompt-sintese-conexoes.md",
    descricao:
      "Fechamento do ciclo: síntese, balanço crítico, obras em diálogo, reflexões, fontes e a ficha-resumo da análise.",
  },
];

const EXEMPLO = {
  titulo: "Cidade de Deus (2002)",
  diretor: "Fernando Meirelles e Kátia Lund",
  pergunta:
    "De que forma a montagem acelerada e fragmentada, combinada à narração em off de Buscapé, transforma a violência em espetáculo — e como o filme lida com a tensão ética entre estetizar essa violência e, ao mesmo tempo, criticá-la?",
};

const CHAVE_STORAGE = "fluxo-ui-v1";

/* ---------------- Estado e elementos ---------------- */

const estado = {
  etapaAtual: "1",
  templates: {},
  carregado: false,
  editadoManualmente: false,
  copiadas: new Set(),
};

const el = {};
[
  "titulo", "diretor", "pergunta", "saida", "stepper", "etapa-desc",
  "campo-pergunta", "contador", "pendencias", "dica-edicao", "aviso-erro",
  "toast", "btn-copiar", "btn-baixar", "btn-exemplo", "btn-limpar",
  "btn-regenerar",
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
  el["campo-pergunta"].hidden = etapa.id !== "2.2";

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
    localStorage.setItem(CHAVE_STORAGE, JSON.stringify({
      titulo: el.titulo.value,
      diretor: el.diretor.value,
      pergunta: el.pergunta.value,
      etapaAtual: estado.etapaAtual,
      copiadas: Array.from(estado.copiadas),
    }));
  } catch (_e) { /* navegador sem storage: segue o jogo */ }
}

function restaurar() {
  try {
    const bruto = localStorage.getItem(CHAVE_STORAGE);
    if (!bruto) return;
    const dados = JSON.parse(bruto);
    if (dados.titulo) el.titulo.value = dados.titulo;
    if (dados.diretor) el.diretor.value = dados.diretor;
    if (dados.pergunta) el.pergunta.value = dados.pergunta;
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

["titulo", "diretor", "pergunta"].forEach((id) => {
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
  el.titulo.value = EXEMPLO.titulo;
  el.diretor.value = EXEMPLO.diretor;
  el.pergunta.value = EXEMPLO.pergunta;
  estado.editadoManualmente = false;
  salvar();
  render();
  toast("Exemplo carregado: Cidade de Deus (2002). Experimente cada etapa!");
});

el["btn-limpar"].addEventListener("click", () => {
  el.titulo.value = "";
  el.diretor.value = "";
  el.pergunta.value = "";
  estado.copiadas.clear();
  estado.etapaAtual = "1";
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
