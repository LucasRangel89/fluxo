"use strict";

/* ============================================================================
   Fluxo — pesquisa de metadados (Fase 5)

   Consulta somente quando o usuário busca: Wikipedia, Wikidata e TVMaze.
   O resultado nunca é aplicado silenciosamente; a pessoa escolhe a obra e
   pode corrigir qualquer campo depois.
   ========================================================================== */

(() => {
  const $ = (id) => document.getElementById(id);
  const el = {
    busca: $("busca-obra"),
    destino: $("busca-destino"),
    botao: $("btn-buscar-obra"),
    status: $("busca-status"),
    resultados: $("busca-resultados"),
    resumo: $("metadados-resumo"),
    dossie: $("dossie-fontes"),
    gerarDossie: $("btn-gerar-dossie-metadados"),
    limparDossie: $("btn-limpar-dossie"),
    links: $("links-pesquisa"),
    trilha: $("trilha"),
  };
  if (!el.busca || !el.resultados) return;

  const CHAVE_METADADOS = "fluxo-metadados-v1";
  let selecionados = {};
  try {
    selecionados = JSON.parse(localStorage.getItem(CHAVE_METADADOS) || "{}") || {};
  } catch (_e) {
    selecionados = {};
  }

  let resultadosAtuais = [];
  let sequenciaBusca = 0;
  let temporizador = null;

  function textoLimpo(valor) {
    if (!valor) return "";
    const area = document.createElement("textarea");
    area.innerHTML = String(valor).replace(/<[^>]*>/g, " ");
    return area.value.replace(/\s+/g, " ").trim();
  }

  function anoDe(valor) {
    const encontrado = String(valor || "").match(/(?:19|20)\d{2}/);
    return encontrado ? encontrado[0] : "";
  }

  function disparar(elemento) {
    if (!elemento) return;
    elemento.dispatchEvent(new Event("input", { bubbles: true }));
    elemento.dispatchEvent(new Event("change", { bubbles: true }));
  }

  function definirValor(id, valor) {
    const campo = $(id);
    if (!campo || !valor) return;
    campo.value = valor;
    disparar(campo);
  }

  function salvarSelecionados() {
    try {
      localStorage.setItem(CHAVE_METADADOS, JSON.stringify(selecionados));
    } catch (_e) { /* segue sem persistência */ }
  }

  async function buscarJson(url) {
    const resposta = await fetch(url, {
      headers: { Accept: "application/json" },
    });
    if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
    return resposta.json();
  }

  function urlApi(base, parametros) {
    const url = new URL(base);
    Object.entries(parametros).forEach(([chave, valor]) => {
      if (valor !== undefined && valor !== "") url.searchParams.set(chave, valor);
    });
    return url.toString();
  }

  async function buscarWikipedia(consulta) {
    const dados = await buscarJson(urlApi("https://pt.wikipedia.org/w/api.php", {
      action: "query",
      generator: "search",
      gsrsearch: `${consulta} (filme OR série OR televisão OR cinema)`,
      gsrlimit: "6",
      prop: "pageimages|extracts|info",
      inprop: "url",
      exintro: "1",
      explaintext: "1",
      pithumbsize: "160",
      format: "json",
      origin: "*",
    }));
    const paginas = Object.values(dados.query?.pages || {})
      .sort((a, b) => (a.index || 99) - (b.index || 99));
    return paginas.map((pagina) => ({
      fonte: "Wikipedia",
      id: `wiki-${pagina.pageid}`,
      titulo: pagina.title || consulta,
      ano: anoDe(`${pagina.title || ""} ${pagina.extract || ""}`),
      descricao: textoLimpo(pagina.extract).slice(0, 420),
      tipo: "",
      criadores: "",
      url: pagina.fullurl || "",
      imagem: pagina.thumbnail?.source || "",
      wikipediaTitulo: pagina.title || "",
      wikipediaIdioma: "ptwiki",
    }));
  }

  async function buscarWikidata(consulta) {
    const dados = await buscarJson(urlApi("https://www.wikidata.org/w/api.php", {
      action: "wbsearchentities",
      search: consulta,
      language: "pt",
      uselang: "pt",
      type: "item",
      limit: "8",
      format: "json",
      origin: "*",
    }));
    return (dados.search || [])
      .filter((item) => {
        const texto = `${item.label || ""} ${item.description || ""}`.toLocaleLowerCase("pt-BR");
        return /filme|série|serie|televis|cinema|animação|animacao|documentário|documentario|curta|obra audiovisual/.test(texto)
          || texto.includes(consulta.toLocaleLowerCase("pt-BR"));
      })
      .slice(0, 6)
      .map((item) => ({
        fonte: "Wikidata",
        id: `wikidata-${item.id}`,
        titulo: item.label || consulta,
        ano: anoDe(item.description),
        descricao: textoLimpo(item.description),
        tipo: "",
        criadores: "",
        url: item.concepturi || `https://www.wikidata.org/wiki/${item.id}`,
        imagem: "",
        wikidataId: item.id,
      }));
  }

  async function buscarTvMaze(consulta) {
    const dados = await buscarJson(
      `https://api.tvmaze.com/search/shows?q=${encodeURIComponent(consulta)}`
    );
    return (dados || []).slice(0, 6).map((item) => {
      const show = item.show || {};
      const emissora = show.network?.name || show.webChannel?.name || "";
      return {
        fonte: "TVMaze",
        id: `tvmaze-${show.id}`,
        titulo: show.name || consulta,
        ano: anoDe(show.premiered),
        descricao: textoLimpo(show.summary).slice(0, 420),
        tipo: ["Série", ...(show.genres || []), emissora].filter(Boolean).join(" · "),
        criadores: "",
        url: show.officialSite || show.url || "",
        imagem: show.image?.medium || "",
        tvmazeId: show.id,
        bruto: show,
      };
    });
  }

  function renderizarResultados() {
    el.resultados.innerHTML = "";
    resultadosAtuais.forEach((resultado, indice) => {
      const botao = document.createElement("button");
      botao.type = "button";
      botao.className = "resultado-obra";
      botao.dataset.indice = String(indice);

      if (resultado.imagem) {
        const img = document.createElement("img");
        img.src = resultado.imagem;
        img.alt = "";
        img.loading = "lazy";
        botao.appendChild(img);
      }

      const corpo = document.createElement("span");
      const titulo = document.createElement("strong");
      titulo.textContent = resultado.ano && !resultado.titulo.includes(resultado.ano)
        ? `${resultado.titulo} (${resultado.ano})`
        : resultado.titulo;
      const descricao = document.createElement("span");
      descricao.textContent = resultado.descricao || resultado.tipo || "Selecionar esta obra";
      corpo.append(titulo, descricao);

      const fonte = document.createElement("span");
      fonte.className = "resultado-fonte";
      fonte.textContent = resultado.fonte;
      botao.append(corpo, fonte);
      el.resultados.appendChild(botao);
    });
  }

  async function buscar() {
    const consulta = el.busca.value.trim();
    if (consulta.length < 2) {
      el.status.textContent = "Digite ao menos parte do título para buscar.";
      return;
    }
    const minhaSequencia = ++sequenciaBusca;
    el.status.textContent = "Buscando em Wikipedia, Wikidata e TVMaze…";
    el.resultados.innerHTML = "";

    const respostas = await Promise.allSettled([
      buscarWikipedia(consulta),
      buscarWikidata(consulta),
      buscarTvMaze(consulta),
    ]);
    if (minhaSequencia !== sequenciaBusca) return;

    const wikipedia = respostas[0].status === "fulfilled" ? respostas[0].value : [];
    const wikidata = respostas[1].status === "fulfilled" ? respostas[1].value : [];
    const tvmaze = respostas[2].status === "fulfilled" ? respostas[2].value : [];
    const seriesPrimeiro = el.trilha?.value === "serie";
    const combinados = seriesPrimeiro
      ? [...tvmaze, ...wikipedia, ...wikidata]
      : [...wikipedia, ...wikidata, ...tvmaze];

    const vistos = new Set();
    resultadosAtuais = combinados.filter((item) => {
      const chave = `${item.fonte}:${item.id}:${item.titulo}`.toLocaleLowerCase("pt-BR");
      if (vistos.has(chave)) return false;
      vistos.add(chave);
      return true;
    }).slice(0, 10);

    if (!resultadosAtuais.length) {
      el.status.textContent = "Nenhum resultado aproveitável. Tente o título original ou inclua o ano.";
      return;
    }
    el.status.textContent = `${resultadosAtuais.length} resultado(s). Escolha a obra correta para preencher os campos.`;
    renderizarResultados();
  }

  function valoresDeClaim(entidade, propriedade) {
    return (entidade?.claims?.[propriedade] || [])
      .map((claim) => claim?.mainsnak?.datavalue?.value)
      .filter(Boolean);
  }

  async function rotulosWikidata(ids) {
    const unicos = [...new Set(ids.filter(Boolean))].slice(0, 45);
    if (!unicos.length) return {};
    const dados = await buscarJson(urlApi("https://www.wikidata.org/w/api.php", {
      action: "wbgetentities",
      ids: unicos.join("|"),
      props: "labels",
      languages: "pt|en",
      format: "json",
      origin: "*",
    }));
    const mapa = {};
    Object.entries(dados.entities || {}).forEach(([id, entidade]) => {
      mapa[id] = entidade.labels?.pt?.value || entidade.labels?.en?.value || id;
    });
    return mapa;
  }

  async function detalhesWikidata(id) {
    const dados = await buscarJson(urlApi("https://www.wikidata.org/w/api.php", {
      action: "wbgetentities",
      ids: id,
      props: "labels|descriptions|claims|sitelinks/urls",
      languages: "pt|en",
      format: "json",
      origin: "*",
    }));
    const entidade = dados.entities?.[id];
    if (!entidade) return {};

    const idsCriadores = [
      ...valoresDeClaim(entidade, "P57").map((v) => v.id),
      ...valoresDeClaim(entidade, "P170").map((v) => v.id),
    ];
    const idsTipos = valoresDeClaim(entidade, "P31").map((v) => v.id);
    const idsGeneros = valoresDeClaim(entidade, "P136").map((v) => v.id);
    const idsElenco = valoresDeClaim(entidade, "P161").map((v) => v.id).slice(0, 8);
    const rotulos = await rotulosWikidata([
      ...idsCriadores, ...idsTipos, ...idsGeneros, ...idsElenco,
    ]);
    const nomes = (ids) => ids.map((item) => rotulos[item]).filter(Boolean);
    const data = valoresDeClaim(entidade, "P577")
      .map((valor) => valor.time)
      .find(Boolean);
    const sitelinks = entidade.sitelinks || {};
    const wikipediaUrl = sitelinks.ptwiki?.url || sitelinks.enwiki?.url || "";

    return {
      titulo: entidade.labels?.pt?.value || entidade.labels?.en?.value || "",
      descricao: entidade.descriptions?.pt?.value || entidade.descriptions?.en?.value || "",
      ano: anoDe(data),
      tipo: [...nomes(idsTipos), ...nomes(idsGeneros)].join(" · "),
      criadores: nomes([...new Set(idsCriadores)]).join(", "),
      elenco: nomes(idsElenco).join(", "),
      url: wikipediaUrl,
      wikidataId: id,
      wikidataUrl: `https://www.wikidata.org/wiki/${id}`,
    };
  }

  async function enriquecerWikipediaComWikidata(resultado) {
    const dados = await buscarJson(urlApi("https://www.wikidata.org/w/api.php", {
      action: "wbgetentities",
      sites: resultado.wikipediaIdioma || "ptwiki",
      titles: resultado.wikipediaTitulo,
      props: "labels",
      languages: "pt|en",
      format: "json",
      origin: "*",
    }));
    const id = Object.keys(dados.entities || {}).find((chave) => chave.startsWith("Q"));
    if (!id) return {};
    return detalhesWikidata(id);
  }

  async function detalhesTvMaze(resultado) {
    const show = resultado.bruto || {};
    const detalhes = { ...resultado };
    try {
      const [elenco, equipe] = await Promise.allSettled([
        buscarJson(`https://api.tvmaze.com/shows/${resultado.tvmazeId}/cast`),
        buscarJson(`https://api.tvmaze.com/shows/${resultado.tvmazeId}/crew`),
      ]);
      if (elenco.status === "fulfilled") {
        detalhes.elenco = elenco.value
          .slice(0, 8)
          .map((item) => item.person?.name)
          .filter(Boolean)
          .join(", ");
      }
      if (equipe.status === "fulfilled") {
        const prioridades = ["showrunner", "creator", "executive producer", "director"];
        const pessoas = [];
        prioridades.forEach((tipo) => {
          equipe.value
            .filter((item) => String(item.type || "").toLocaleLowerCase() === tipo)
            .forEach((item) => {
              if (item.person?.name && !pessoas.includes(item.person.name)) {
                pessoas.push(item.person.name);
              }
            });
        });
        detalhes.criadores = pessoas.slice(0, 5).join(", ");
      }
    } catch (_e) { /* os dados básicos continuam úteis */ }

    detalhes.tipo = [
      "Série",
      ...(show.genres || []),
      show.network?.name || show.webChannel?.name || "",
      show.status ? `status: ${show.status}` : "",
    ].filter(Boolean).join(" · ");
    detalhes.tvmazeUrl = show.url || "";
    detalhes.externos = show.externals || {};
    return detalhes;
  }

  function tituloComAno(metadado) {
    if (!metadado.titulo) return "";
    return metadado.ano && !metadado.titulo.includes(metadado.ano)
      ? `${metadado.titulo} (${metadado.ano})`
      : metadado.titulo;
  }

  function aplicarMetadado(metadado, destino) {
    const titulo = tituloComAno(metadado);
    if (destino === "obra-a") {
      definirValor("obra-a", titulo);
      definirValor("diretor-a", metadado.criadores);
      definirValor("trilha", "comparativa");
    } else if (destino === "obra-b") {
      definirValor("obra-b", titulo);
      definirValor("diretor-b", metadado.criadores);
      definirValor("trilha", "comparativa");
    } else {
      definirValor("titulo", titulo);
      definirValor("diretor", metadado.criadores);
      if (metadado.tipo) definirValor("tipo", metadado.tipo);
      if (metadado.fonte === "TVMaze") definirValor("trilha", "serie");
    }
    atualizarResumoMetadados();
    atualizarLinksPesquisa();
  }

  function atualizarResumoMetadados() {
    const itens = Object.entries(selecionados);
    if (!itens.length) {
      el.resumo.hidden = true;
      el.resumo.innerHTML = "";
      return;
    }
    el.resumo.hidden = false;
    el.resumo.innerHTML = "";
    const titulo = document.createElement("strong");
    titulo.textContent = "Metadados selecionados: ";
    el.resumo.appendChild(titulo);
    itens.forEach(([destino, item], indice) => {
      const span = document.createElement("span");
      span.textContent = `${indice ? " · " : ""}${destino}: ${tituloComAno(item)} (${item.fonte})`;
      el.resumo.appendChild(span);
      if (item.url) {
        const link = document.createElement("a");
        link.href = item.url;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.textContent = " fonte";
        el.resumo.appendChild(link);
      }
    });
  }

  async function selecionarResultado(resultado) {
    const destino = el.destino.value;
    el.status.textContent = `Buscando detalhes de ${resultado.titulo}…`;
    let detalhes = {};
    try {
      if (resultado.fonte === "Wikidata" && resultado.wikidataId) {
        detalhes = await detalhesWikidata(resultado.wikidataId);
      } else if (resultado.fonte === "Wikipedia" && resultado.wikipediaTitulo) {
        detalhes = await enriquecerWikipediaComWikidata(resultado);
      } else if (resultado.fonte === "TVMaze" && resultado.tvmazeId) {
        detalhes = await detalhesTvMaze(resultado);
      }
    } catch (_e) {
      detalhes = {};
    }

    const metadado = { ...resultado };
    Object.entries(detalhes).forEach(([chave, valor]) => {
      if (valor) metadado[chave] = valor;
    });
    delete metadado.bruto;
    selecionados[destino] = metadado;
    salvarSelecionados();
    aplicarMetadado(metadado, destino);
    el.status.textContent = `Selecionado: ${tituloComAno(metadado)}. Confira os campos — você pode corrigir qualquer informação.`;

    if (el.dossie && !el.dossie.value.trim()) {
      gerarDossieMetadados(false);
    }
  }

  function textoDoMetadado(destino, item) {
    const linhas = [
      `### ${destino === "principal" ? "Obra principal" : destino.toUpperCase()} — ${tituloComAno(item)}`,
      item.tipo ? `- Formato/tipo: ${item.tipo}` : "",
      item.criadores ? `- Direção/criação: ${item.criadores}` : "",
      item.elenco ? `- Elenco (parcial): ${item.elenco}` : "",
      item.descricao ? `- Descrição da fonte: ${item.descricao}` : "",
      `- Fonte do metadado: ${item.fonte}${item.url ? ` — ${item.url}` : ""}`,
      item.wikidataUrl ? `- Wikidata: ${item.wikidataUrl}` : "",
      item.tvmazeUrl ? `- TVMaze: ${item.tvmazeUrl}` : "",
    ].filter(Boolean);
    return linhas.join("\n");
  }

  function gerarDossieMetadados(annunciar = true) {
    const itens = Object.entries(selecionados);
    if (!itens.length) {
      if (annunciar) el.status.textContent = "Selecione uma obra na busca antes de gerar o dossiê.";
      return;
    }
    const gerado = [
      "## Metadados de bases abertas",
      "",
      "Use como ponto de partida e confira nas fontes. Metadado não é evidência de cena.",
      "",
      ...itens.map(([destino, item]) => textoDoMetadado(destino, item)),
    ].join("\n\n");

    const atual = el.dossie.value.trim();
    if (!atual) {
      el.dossie.value = gerado;
    } else if (!atual.includes("## Metadados de bases abertas")) {
      el.dossie.value = `${gerado}\n\n## Pesquisa adicionada\n\n${atual}`;
    } else {
      el.dossie.value = atual.replace(
        /## Metadados de bases abertas[\s\S]*?(?=\n## Pesquisa adicionada|$)/,
        gerado
      );
    }
    disparar(el.dossie);
    if (annunciar) el.status.textContent = "Dossiê atualizado com os metadados selecionados.";
  }

  function atualizarLinksPesquisa() {
    if (!el.links) return;
    const titulo = $("titulo")?.value.trim() || el.busca.value.trim();
    el.links.innerHTML = "";
    if (!titulo) return;
    const consultas = [
      ["Produção e bastidores", `${titulo} produção bastidores entrevista direção`, "https://duckduckgo.com/?q="],
      ["Fotografia e imagem", `${titulo} cinematography fotografia direção de arte análise`, "https://duckduckgo.com/?q="],
      ["Som e montagem", `${titulo} sound design trilha sonora montagem análise`, "https://duckduckgo.com/?q="],
      ["Recepção e legado", `${titulo} crítica recepção legado prêmios`, "https://duckduckgo.com/?q="],
      ["Textos acadêmicos", `${titulo} film analysis`, "https://scholar.google.com/scholar?q="],
      ["Entrevistas", `${titulo} entrevista diretor criador`, "https://duckduckgo.com/?q="],
    ];
    consultas.forEach(([rotulo, consulta, base]) => {
      const link = document.createElement("a");
      link.href = base + encodeURIComponent(consulta);
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.textContent = rotulo;
      el.links.appendChild(link);
    });
  }

  el.botao?.addEventListener("click", buscar);
  el.busca.addEventListener("keydown", (evento) => {
    if (evento.key === "Enter") {
      evento.preventDefault();
      buscar();
    }
  });
  el.busca.addEventListener("input", () => {
    clearTimeout(temporizador);
    if (el.busca.value.trim().length >= 3) {
      temporizador = setTimeout(buscar, 650);
    }
    atualizarLinksPesquisa();
  });
  el.resultados.addEventListener("click", (evento) => {
    const botao = evento.target.closest("[data-indice]");
    if (!botao) return;
    const resultado = resultadosAtuais[Number(botao.dataset.indice)];
    if (resultado) selecionarResultado(resultado);
  });
  el.gerarDossie?.addEventListener("click", () => gerarDossieMetadados(true));
  el.limparDossie?.addEventListener("click", () => {
    if (!el.dossie) return;
    el.dossie.value = "";
    disparar(el.dossie);
  });
  $("btn-limpar")?.addEventListener("click", () => {
    selecionados = {};
    salvarSelecionados();
    atualizarResumoMetadados();
    el.resultados.innerHTML = "";
    el.status.textContent = "";
  });
  ["titulo", "obra-a", "obra-b"].forEach((id) => {
    $(id)?.addEventListener("input", atualizarLinksPesquisa);
  });

  atualizarResumoMetadados();
  atualizarLinksPesquisa();

  window.FluxoPesquisa = {
    selecionados: () => JSON.parse(JSON.stringify(selecionados)),
    gerarDossieMetadados,
  };
})();
