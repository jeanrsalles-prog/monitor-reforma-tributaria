#!/usr/bin/env python3
"""
Gerador de relatório do Monitor da Reforma Tributária.

Lê um JSON com os achados de uma rodada e gera dois entregáveis:
  1. dashboard_RT.html  — painel visual e didático, renderizado offline
  2. monitor_RT_AAAA-MM-DD.md — relatório em texto, no layout clássico

O JSON é preenchido pelo assistente a partir da varredura nas fontes oficiais.
Nenhum dado de cliente entra aqui — o relatório acompanha apenas legislação.

Uso:
    python3 scripts/gerar_relatorio.py --dados rodada.json --saida "<pasta>"
    python3 scripts/gerar_relatorio.py --dados rodada.json --saida "<pasta>" --rodape "Seu Escritório"

Esquema do JSON (todos os campos de lista são opcionais):
{
  "data": "2026-06-15",                  # data da rodada (AAAA-MM-DD)
  "titulo": "Monitor Reforma Tributária",
  "fontes_verificadas": 7,
  "rodape": "",                          # assinatura opcional (sobrescrita por --rodape)
  "nova_legislacao": [
    {"titulo": "...", "data": "03/06/2026", "fonte": "DOU / CGIBS",
     "tipo": "Ato Conjunto", "resumo": "...", "link": "https://..."}
  ],
  "destaques": [
    {"classificacao": "RELEVANTE", "titulo": "...", "data": "...",
     "fonte": "...", "resumo": "...", "link": "https://..."}
  ],
  "alertas": [
    {"data": "15/06/2026", "titulo": "...", "descricao": "..."}
  ]
}

Classificações aceitas em "destaques": CRITICO, RELEVANTE, INFORMATIVO
(os acentos são opcionais; o script normaliza).

Ao final, imprime uma linha JSON com o resumo da rodada, para o assistente
conversar com o usuário.
"""

import argparse
import html
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

# -------------------------------------------------------------------- cores
ACCENT = {
    "NOVA": "#1f8a4c",        # verde — norma publicada
    "CRITICO": "#c0392b",     # vermelho
    "RELEVANTE": "#d98a00",   # âmbar
    "INFORMATIVO": "#2d6cdf", # azul
    "ALERTA": "#7a5cc6",      # roxo
    "ALERTA_URGENTE": "#c0392b",
}
ROTULO = {
    "CRITICO": "CRÍTICO",
    "RELEVANTE": "RELEVANTE",
    "INFORMATIVO": "INFORMATIVO",
}


def norm_classe(valor):
    """Normaliza a classificação para CRITICO / RELEVANTE / INFORMATIVO."""
    if not valor:
        return "INFORMATIVO"
    v = (
        valor.strip().upper()
        .replace("Í", "I").replace(" Í", "I")
        .replace("Á", "A").replace("É", "E").replace("Ó", "O")
    )
    if v.startswith("CRIT"):
        return "CRITICO"
    if v.startswith("RELEV"):
        return "RELEVANTE"
    return "INFORMATIVO"


def parse_data_br(valor):
    """Tenta ler uma data DD/MM/AAAA; devolve um objeto date ou None."""
    if not valor:
        return None
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", valor)
    if not m:
        return None
    try:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None


def dias_restantes(valor, hoje):
    d = parse_data_br(valor)
    if d is None:
        return None
    return (d - hoje).days


def esc(texto):
    return html.escape(str(texto or ""))


# -------------------------------------------------------------------- HTML
def bloco_item_html(item, classe):
    cor = ACCENT.get(classe, ACCENT["INFORMATIVO"])
    rotulo = ROTULO.get(classe, classe)
    link = item.get("link", "")
    link_html = (
        f'<a class="lnk" href="{esc(link)}" target="_blank" rel="noopener">abrir fonte ↗</a>'
        if link else ""
    )
    meta = " · ".join(
        x for x in [esc(item.get("data", "")), esc(item.get("fonte", ""))] if x
    )
    tipo = item.get("tipo", "")
    tipo_html = f'<div class="tipo">{esc(tipo)}</div>' if tipo else ""
    return f"""
    <article class="card" data-classe="{classe}" data-busca="{esc((item.get('titulo','') + ' ' + item.get('resumo','') + ' ' + item.get('fonte','')).lower())}">
      <div class="tag" style="background:{cor}">{esc(rotulo)}</div>
      <h3>{esc(item.get('titulo',''))}</h3>
      {tipo_html}
      <div class="meta">{meta}</div>
      <p>{esc(item.get('resumo',''))}</p>
      {link_html}
    </article>"""


def bloco_alerta_html(alerta, hoje):
    dr = dias_restantes(alerta.get("data", ""), hoje)
    if dr is not None and dr < 0:
        selo, cor = "vencido", ACCENT["ALERTA_URGENTE"]
    elif dr is not None and dr <= 7:
        selo, cor = f"em {dr} dia(s)", ACCENT["ALERTA_URGENTE"]
    elif dr is not None:
        selo, cor = f"em {dr} dias", ACCENT["ALERTA"]
    else:
        selo, cor = "—", ACCENT["ALERTA"]
    return f"""
    <article class="alerta" data-busca="{esc((alerta.get('titulo','') + ' ' + alerta.get('descricao','')).lower())}">
      <div class="alerta-data" style="border-color:{cor};color:{cor}">
        <span class="ad-dia">{esc(alerta.get('data','—'))}</span>
        <span class="ad-selo" style="background:{cor}">{esc(selo)}</span>
      </div>
      <div class="alerta-txt">
        <h4>{esc(alerta.get('titulo',''))}</h4>
        <p>{esc(alerta.get('descricao',''))}</p>
      </div>
    </article>"""


def gerar_html(dados, hoje, rodape):
    titulo = dados.get("titulo", "Monitor da Reforma Tributária")
    data_rodada = dados.get("data", hoje.isoformat())
    try:
        data_extenso = datetime.strptime(data_rodada, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        data_extenso = data_rodada

    novas = dados.get("nova_legislacao", []) or []
    destaques = dados.get("destaques", []) or []
    alertas = dados.get("alertas", []) or []

    cont = {"CRITICO": 0, "RELEVANTE": 0, "INFORMATIVO": 0}
    for d in destaques:
        cont[norm_classe(d.get("classificacao"))] += 1

    cards = []
    for n in novas:
        cards.append(bloco_item_html(n, "NOVA"))
    for d in destaques:
        cards.append(bloco_item_html(d, norm_classe(d.get("classificacao"))))
    cards_html = "\n".join(cards) or '<p class="vazio">Nenhuma novidade nesta rodada.</p>'

    alertas_html = "\n".join(bloco_alerta_html(a, hoje) for a in alertas) \
        or '<p class="vazio">Sem prazos cadastrados.</p>'

    def chip(rotulo, valor, cor):
        return f'<div class="chip"><span class="chip-n" style="color:{cor}">{valor}</span>{rotulo}</div>'

    chips = "".join([
        chip("nova legislação", len(novas), ACCENT["NOVA"]),
        chip("crítico", cont["CRITICO"], ACCENT["CRITICO"]),
        chip("relevante", cont["RELEVANTE"], ACCENT["RELEVANTE"]),
        chip("informativo", cont["INFORMATIVO"], ACCENT["INFORMATIVO"]),
        chip("alertas", len(alertas), ACCENT["ALERTA"]),
        chip("fontes verificadas", dados.get("fontes_verificadas", "—"), "#555"),
    ])

    rodape_html = (
        f'<div class="assinatura">{esc(rodape)}</div>' if rodape else ""
    )

    return f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(titulo)} — {esc(data_extenso)}</title>
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
          background:#f5f5f3; color:#1a1a1a; line-height:1.5; }}
  .wrap {{ max-width: 960px; margin:0 auto; padding: 28px 20px 60px; }}
  header h1 {{ font-size: 1.55rem; margin:0 0 2px; }}
  header .data {{ color:#666; font-size:.95rem; margin-bottom:18px; }}
  .painel {{ display:flex; flex-wrap:wrap; gap:10px; margin: 0 0 22px; }}
  .chip {{ background:#fff; border:1px solid #e3e3df; border-radius:10px; padding:10px 14px;
           font-size:.78rem; color:#555; display:flex; flex-direction:column; gap:2px; min-width:96px; }}
  .chip-n {{ font-size:1.4rem; font-weight:700; line-height:1; }}
  .toolbar {{ margin: 0 0 16px; }}
  .toolbar input {{ width:100%; padding:11px 14px; border:1px solid #ddd; border-radius:10px; font-size:.95rem; }}
  .filtros {{ display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 0; }}
  .filtros button {{ border:1px solid #ddd; background:#fff; border-radius:20px; padding:6px 13px;
                     font-size:.8rem; cursor:pointer; color:#444; }}
  .filtros button.on {{ background:#1a1a1a; color:#fff; border-color:#1a1a1a; }}
  h2.sec {{ font-size:.82rem; letter-spacing:.08em; text-transform:uppercase; color:#888;
            margin:30px 0 12px; border-bottom:1px solid #e3e3df; padding-bottom:6px; }}
  .card {{ background:#fff; border:1px solid #e8e8e4; border-left:4px solid #ccc; border-radius:12px;
           padding:16px 18px; margin-bottom:12px; }}
  .card .tag {{ display:inline-block; color:#fff; font-size:.68rem; font-weight:700; letter-spacing:.05em;
               padding:3px 9px; border-radius:6px; margin-bottom:8px; }}
  .card h3 {{ margin:2px 0 4px; font-size:1.05rem; }}
  .card .tipo {{ font-size:.78rem; color:#1f8a4c; font-weight:600; margin-bottom:2px; }}
  .card .meta {{ font-size:.8rem; color:#888; margin-bottom:8px; }}
  .card p {{ margin:0 0 10px; font-size:.94rem; }}
  .card .lnk {{ font-size:.84rem; color:#2d6cdf; text-decoration:none; }}
  .card .lnk:hover {{ text-decoration:underline; }}
  .alerta {{ display:flex; gap:14px; background:#fff; border:1px solid #e8e8e4; border-radius:12px;
             padding:14px 16px; margin-bottom:10px; align-items:flex-start; }}
  .alerta-data {{ border:2px solid #7a5cc6; border-radius:10px; padding:8px 10px; text-align:center;
                  min-width:108px; display:flex; flex-direction:column; gap:5px; }}
  .ad-dia {{ font-weight:700; font-size:.9rem; }}
  .ad-selo {{ color:#fff; font-size:.68rem; border-radius:5px; padding:2px 6px; }}
  .alerta-txt h4 {{ margin:2px 0 4px; font-size:1rem; }}
  .alerta-txt p {{ margin:0; font-size:.9rem; color:#444; }}
  .vazio {{ color:#999; font-style:italic; }}
  footer {{ margin-top:34px; padding-top:16px; border-top:1px solid #e3e3df; font-size:.8rem; color:#888; }}
  .assinatura {{ font-weight:600; color:#555; margin-bottom:4px; }}
  .hidden {{ display:none !important; }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>{esc(titulo)}</h1>
    <div class="data">Rodada de {esc(data_extenso)}</div>
  </header>

  <section class="painel">{chips}</section>

  <div class="toolbar">
    <input id="busca" type="search" placeholder="Buscar por palavra (ato, tema, fonte)…" oninput="filtrar()">
    <div class="filtros" id="filtros">
      <button class="on" data-f="TODOS" onclick="setFiltro(this)">Todos</button>
      <button data-f="NOVA" onclick="setFiltro(this)">Nova legislação</button>
      <button data-f="CRITICO" onclick="setFiltro(this)">Crítico</button>
      <button data-f="RELEVANTE" onclick="setFiltro(this)">Relevante</button>
      <button data-f="INFORMATIVO" onclick="setFiltro(this)">Informativo</button>
    </div>
  </div>

  <h2 class="sec">Novidades</h2>
  <div id="lista">
    {cards_html}
  </div>

  <h2 class="sec">Alertas e prazos</h2>
  <div id="alertas">
    {alertas_html}
  </div>

  <footer>
    {rodape_html}
    Esta análise tem caráter informativo, baseada em fontes abertas. Não substitui
    parecer jurídico ou contábil formal. Confira sempre a norma na fonte oficial.
  </footer>
</div>

<script>
  let filtroAtivo = "TODOS";
  function setFiltro(btn) {{
    document.querySelectorAll('#filtros button').forEach(b => b.classList.remove('on'));
    btn.classList.add('on');
    filtroAtivo = btn.dataset.f;
    filtrar();
  }}
  function filtrar() {{
    const termo = (document.getElementById('busca').value || '').toLowerCase();
    document.querySelectorAll('#lista .card').forEach(c => {{
      const okClasse = (filtroAtivo === 'TODOS') || (c.dataset.classe === filtroAtivo);
      const okTermo = !termo || (c.dataset.busca || '').includes(termo);
      c.classList.toggle('hidden', !(okClasse && okTermo));
    }});
    document.querySelectorAll('#alertas .alerta').forEach(a => {{
      const okTermo = !termo || (a.dataset.busca || '').includes(termo);
      a.classList.toggle('hidden', !okTermo);
    }});
  }}
</script>
</body>
</html>"""


# -------------------------------------------------------------------- TEXTO
def gerar_texto(dados, hoje, rodape):
    titulo = dados.get("titulo", "Monitor da Reforma Tributária")
    data_rodada = dados.get("data", hoje.isoformat())
    try:
        data_extenso = datetime.strptime(data_rodada, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        data_extenso = data_rodada

    novas = dados.get("nova_legislacao", []) or []
    destaques = dados.get("destaques", []) or []
    alertas = dados.get("alertas", []) or []

    L = []
    L.append(f"# {titulo}")
    L.append(f"_{data_extenso}_")
    L.append("")

    if novas:
        L.append("## Nova legislação — consulte seu advogado")
        L.append("")
        for n in novas:
            L.append(f"### {n.get('titulo','')}")
            meta = " · ".join(x for x in [n.get("data",""), n.get("fonte","")] if x)
            if meta:
                L.append(f"{meta}")
            if n.get("tipo"):
                L.append(f"Tipo: {n['tipo']}")
            L.append("")
            L.append(n.get("resumo", ""))
            if n.get("link"):
                L.append(f"Link: {n['link']}")
            L.append("")

    if destaques:
        L.append("## Destaques da semana")
        L.append("")
        for d in destaques:
            classe = ROTULO.get(norm_classe(d.get("classificacao")), "INFORMATIVO")
            L.append(f"### {classe} — {d.get('titulo','')}")
            meta = " · ".join(x for x in [d.get("data",""), d.get("fonte","")] if x)
            if meta:
                L.append(f"{meta}")
            L.append("")
            L.append(d.get("resumo", ""))
            if d.get("link"):
                L.append(f"Link: {d['link']}")
            L.append("")

    if alertas:
        L.append("## Alertas normativos")
        L.append("")
        for a in alertas:
            dr = dias_restantes(a.get("data",""), hoje)
            selo = ""
            if dr is not None and dr >= 0:
                selo = f" (em {dr} dia(s))"
            elif dr is not None:
                selo = " (vencido)"
            L.append(f"### {a.get('data','—')}{selo} — {a.get('titulo','')}")
            L.append(a.get("descricao", ""))
            L.append("")

    L.append("---")
    if rodape:
        L.append(f"**{rodape}**")
    L.append(
        "Esta análise tem caráter informativo, baseada em fontes abertas. "
        "Não substitui parecer jurídico ou contábil formal. Confira sempre a "
        "norma na fonte oficial."
    )
    L.append("")
    return "\n".join(L)


# -------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Gera os relatórios do Monitor da Reforma Tributária.")
    ap.add_argument("--dados", required=True, help="Caminho do JSON com os achados da rodada.")
    ap.add_argument("--saida", required=True, help="Pasta onde salvar os relatórios.")
    ap.add_argument("--rodape", default=None, help="Assinatura/rodapé opcional (ex.: nome do escritório).")
    args = ap.parse_args()

    caminho = Path(args.dados)
    if not caminho.exists():
        sys.exit(f"ERRO: arquivo de dados não encontrado: {caminho}")
    try:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"ERRO: JSON inválido em {caminho}: {e}")

    hoje = date.today()
    data_rodada = dados.get("data", hoje.isoformat())
    rodape = args.rodape if args.rodape is not None else dados.get("rodape", "")

    saida = Path(args.saida)
    saida.mkdir(parents=True, exist_ok=True)

    html_out = saida / "dashboard_RT.html"
    txt_out = saida / f"monitor_RT_{data_rodada}.md"
    html_out.write_text(gerar_html(dados, hoje, rodape), encoding="utf-8")
    txt_out.write_text(gerar_texto(dados, hoje, rodape), encoding="utf-8")

    resumo = {
        "ok": True,
        "data": data_rodada,
        "nova_legislacao": len(dados.get("nova_legislacao", []) or []),
        "destaques": len(dados.get("destaques", []) or []),
        "alertas": len(dados.get("alertas", []) or []),
        "dashboard": str(html_out),
        "texto": str(txt_out),
    }
    print(json.dumps(resumo, ensure_ascii=False))


if __name__ == "__main__":
    main()
