#!/usr/bin/env python3
"""
Genera la edición diaria de El Terreno Común a partir de un JSON con los
artículos del día, y actualiza portada, hemeroteca y archivo de la edición.

Uso:
    python3 generate_edition.py edicion_2026-10-12.json

El JSON de entrada tiene esta forma:

{
  "date": "2026-10-12",
  "weekday_long": "lunes",
  "date_long": "12 de octubre de 2026",
  "edition_number": 2,
  "articles": [
    {
      "slug": "titulo-corto-en-kebab-case",
      "title": "Titular del artículo",
      "dek": "Una frase de bajada.",
      "section": "Política — España",
      "voice": "normal",            # "normal", "raiz" o "ucronia"
      "origin": "historia",         # solo ucronías: "actualidad" o "historia"
      "divergence": "Qué pasó y qué cambia.",  # solo ucronías (obligatorio)
      "paragraphs": [
        "Primer párrafo...",
        "Segundo párrafo...",
        "* * *",                    # separador de partes (opcional)
        "..."
      ]
    },
    ...
  ]
}

No reescribe artículos de días anteriores. Sobrescribe index.html (la
portada pasa a ser la del día), crea ediciones/<date>.html (copia fija de
esa portada) y añade una entrada a hemeroteca.html.
"""
import json
import re
import sys
import html
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_BASE = "https://elterrenocomun.github.io/el-terreno-comun"

HEAD = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — El Terreno Común</title>
<meta name="description" content="{description}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{canonical_base}/assets/og-image.jpg">
<meta property="og:url" content="{og_url}">
<link rel="canonical" href="{og_url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:,">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&display=swap">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
<header class="masthead">
  <div class="top-rule"></div>
  <div class="kicker-row">
    <span>Madrid — Año I, n.º {edition_number}</span>
    <span>{header_right}</span>
  </div>
  <h1><a href="{rel}index.html">El Terreno Común</a></h1>
  <p class="tagline">Los hechos del día, leídos sin épica</p>
  <nav>
    <a href="{rel}index.html">Portada</a>
    <a href="{rel}hemeroteca.html">Hemeroteca</a>
  </nav>
</header>
"""

FOOT = """<footer>
  El Terreno Común · <a href="{rel}hemeroteca.html">Hemeroteca completa</a>
</footer>
"""

ARTICLE_TEMPLATE = HEAD + """
<main class="wrap">
  <div class="article-head">
    {kicker}
    <h1 class="headline">{title}</h1>
    <p class="dek">{dek}</p>
    {divergence}
    <p class="byline">{section}</p>
  </div>

  <div class="article-body">
{paragraphs}
  </div>

  <div class="share-bar">
    <span class="label">Compartir</span>
    <a class="share-btn" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text={share_text}&url={share_url}">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"/></svg>
      X
    </a>
    <a class="share-btn" target="_blank" rel="noopener" href="https://wa.me/?text={share_text}%20%E2%80%94%20{share_url}">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-12.4 7.5L3 20l1.1-5.4A8.5 8.5 0 1 1 21 11.5z"/></svg>
      WhatsApp
    </a>
    <button class="share-btn" type="button" data-copy="{canonical_url}">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="9" y="9" width="12" height="12" rx="1"/><path d="M5 15H4a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v1"/></svg>
      <span class="copy-label">Copiar enlace</span>
    </button>
  </div>

  <div class="back-wrap">
    <a class="back-link" href="{rel}index.html">← Volver a la portada</a>
  </div>
</main>
""" + FOOT + """<script src="{rel}assets/script.js"></script>
</body>
</html>
"""

FRONT_TEMPLATE = HEAD + """
<main class="wrap">
  <p class="edition-note">{weekday_long_cap}, {date_long}</p>

  <div class="{grid_class}">
{articles_block}
  </div>
</main>
""" + FOOT + """</body>
</html>
"""

HEM_ITEM_TEMPLATE = """    <li>
      <span class="hem-date">{weekday_long_cap}, {date_long}</span><br>
      <a href="ediciones/{date}.html">{titles_joined}</a>
    </li>
"""


def slugify_titles(articles):
    return ", ".join(a["title"] for a in articles)


def esc(s):
    return html.escape(s, quote=True)


KICKERS = {"raiz": "Voz raíz", "ucronia": "Ucronía"}
SECTION_BREAK = "* * *"


def kicker_html(article, trailing=""):
    label = KICKERS.get(article.get("voice", "normal"))
    return f'<span class="kicker">{label}</span>{trailing}' if label else ""


def divergence_html(article):
    d = article.get("divergence")
    if not d:
        return ""
    return f'<p class="divergence"><span>Punto de divergencia.</span> {esc(d)}</p>'


def reading_minutes(article):
    words = sum(len(p.split()) for p in article["paragraphs"])
    return max(1, round(words / 220))


def render_paragraphs(paragraphs):
    out = []
    for p in paragraphs:
        if p.strip() == SECTION_BREAK:
            out.append('    <p class="section-break" aria-hidden="true">⁂</p>')
        else:
            out.append(f"    <p>{esc(p)}</p>")
    return "\n".join(out)


def render_article_file(article, meta, rel, canonical_base):
    kicker = kicker_html(article)
    share_text = urllib.parse.quote(article["title"])
    canonical_url = f"{canonical_base}/articulos/{meta['date']}-{article['slug']}.html"
    share_url = urllib.parse.quote(canonical_url, safe="")
    return ARTICLE_TEMPLATE.format(
        title=esc(article["title"]),
        description=esc(article["dek"]),
        og_type="article",
        og_title=esc(article["title"]),
        rel=rel,
        edition_number=meta["edition_number"],
        header_right=meta["date_long"],
        kicker=kicker,
        dek=esc(article["dek"]),
        divergence=divergence_html(article),
        section=esc(article["section"]) + (f" · Lectura: {reading_minutes(article)} min" if article.get("voice") == "ucronia" else ""),
        paragraphs=render_paragraphs(article["paragraphs"]),
        share_text=share_text,
        share_url=share_url,
        canonical_url=canonical_url,
        canonical_base=canonical_base,
        og_url=canonical_url,
    )


def render_front_article_block(article, meta, rel=""):
    kicker = kicker_html(article, "\n      ")
    first_para = article["paragraphs"][0]
    if len(first_para) <= 280:
        lede = first_para
    else:
        cut = first_para[:280]
        last_stop = cut.rfind(". ")
        if last_stop >= 120:
            lede = cut[: last_stop + 1]
        else:
            lede = cut.rsplit(" ", 1)[0].rstrip(",;:—–- ") + "…"
    href = f"{rel}articulos/{meta['date']}-{article['slug']}.html"
    return (
        '    <article>\n'
        '      <hr class="sep">\n'
        f'      {kicker}<h2 class="headline"><a href="{href}">{esc(article["title"])}</a></h2>\n'
        f'      <p class="dek">{esc(article["dek"])}</p>\n'
        f'      <p class="lede">{esc(lede)}</p>\n'
        f'      <a class="readmore" href="{href}">Leer el artículo completo →</a>\n'
        '    </article>\n'
    )


def render_feature_block(article, meta, rel=""):
    body = [p for p in article["paragraphs"] if p.strip() != SECTION_BREAK]
    lede, total = [], 0
    for para in body:
        if total and total + len(para) > 900:
            break
        lede.append(para)
        total += len(para)
        if total > 500:
            break
    href = f"{rel}articulos/{meta['date']}-{article['slug']}.html"
    label = "Leer la ucronía completa" if article.get("voice") == "ucronia" else "Leer el texto completo"
    ledes = "\n".join(f'      <p class="lede">{esc(x)}</p>' for x in lede)
    return (
        '    <article class="front-feature">\n'
        f'      {kicker_html(article)}\n'
        f'      <h2 class="headline"><a href="{href}">{esc(article["title"])}</a></h2>\n'
        f'      <p class="dek">{esc(article["dek"])}</p>\n'
        f'      {divergence_html(article)}\n'
        f'      <p class="byline">{esc(article["section"])} · Lectura: {reading_minutes(article)} min</p>\n'
        f'{ledes}\n'
        f'      <a class="readmore" href="{href}">{label} →</a>\n'
        '    </article>\n'
    )


def render_front_page(meta, articles, rel, canonical_base, og_url):
    if len(articles) == 1:
        blocks = render_feature_block(articles[0], meta, rel)
    else:
        blocks = "\n".join(render_front_article_block(a, meta, rel) for a in articles)
    return FRONT_TEMPLATE.format(
        title=f"Edición del {meta['date_long']}",
        description="Los hechos del día, leídos sin épica.",
        og_type="website",
        og_title=f"El Terreno Común — Edición del {meta['date_long']}",
        rel=rel,
        edition_number=meta["edition_number"],
        header_right=meta["date_long"] if rel == "" else "Edición archivada",
        weekday_long_cap=meta["weekday_long"].capitalize(),
        date_long=meta["date_long"],
        articles_block=blocks,
        grid_class="front-single" if len(articles) == 1 else "front-grid",
        canonical_base=canonical_base,
        og_url=og_url,
    )


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 generate_edition.py edicion_YYYY-MM-DD.json")
        sys.exit(1)

    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    date = data["date"]
    meta = {
        "date": date,
        "weekday_long": data["weekday_long"],
        "date_long": data["date_long"],
        "edition_number": data["edition_number"],
    }
    articles = data["articles"]
    canonical_base = data.get("canonical_base", DEFAULT_BASE).rstrip("/")

    # 1) Un archivo por artículo
    (ROOT / "articulos").mkdir(exist_ok=True)
    for a in articles:
        out = ROOT / "articulos" / f"{date}-{a['slug']}.html"
        out.write_text(render_article_file(a, meta, rel="../", canonical_base=canonical_base), encoding="utf-8")
        print("  artículo:", out.relative_to(ROOT))

    # 2) Portada del día (index.html, rel="")
    (ROOT / "index.html").write_text(render_front_page(meta, articles, rel="", canonical_base=canonical_base, og_url=canonical_base + "/"), encoding="utf-8")
    print("  portada actualizada: index.html")

    # 3) Copia fija en ediciones/<date>.html (rel="../")
    (ROOT / "ediciones").mkdir(exist_ok=True)
    (ROOT / "ediciones" / f"{date}.html").write_text(
        render_front_page(meta, articles, rel="../", canonical_base=canonical_base, og_url=f"{canonical_base}/ediciones/{date}.html"), encoding="utf-8"
    )
    print("  edición archivada: ediciones/%s.html" % date)

    # 4) Hemeroteca: insertar la nueva entrada justo tras <ul class="hem-list">
    hem_path = ROOT / "hemeroteca.html"
    hem = hem_path.read_text(encoding="utf-8")
    item = HEM_ITEM_TEMPLATE.format(
        weekday_long_cap=meta["weekday_long"].capitalize(),
        date_long=meta["date_long"],
        date=date,
        titles_joined=esc(slugify_titles(articles)),
    )
    marker = '<ul class="hem-list">'
    if f'ediciones/{date}.html' in hem:
        print("  aviso: la hemeroteca ya tenía una entrada para", date, "- no se duplica")
    else:
        hem = hem.replace(marker, marker + "\n" + item, 1)
        hem_path.write_text(hem, encoding="utf-8")
        print("  hemeroteca actualizada")

    print("\nListo. Revisa y haz commit + push de los cambios.")


if __name__ == "__main__":
    main()
