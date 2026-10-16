#!/usr/bin/env python3
"""
Construye la web de El Terreno Común a partir de las ucronías guardadas en
ucronias_json/. Cada ejecución regenera todo: la página de cada ucronía, la
portada (la más reciente, destacada, y las anteriores debajo) y el archivo.

Uso:
    python3 generate_ucronia.py

Cada ucronía es un archivo ucronias_json/AAAA-MM-DD-slug.json con esta forma:

{
  "date": "2026-10-16",                 # fecha de publicación
  "date_long": "16 de octubre de 2026",
  "number": 1,                          # número de línea temporal (1, 2, 3...)
  "slug": "la-crisis-que-no-tuvo-fecha",
  "title": "Titular",
  "dek": "Una frase de bajada.",
  "place": "Nueva York",                # dónde transcurre (o empieza) la ucronía
  "year": 2008,                         # año del punto de divergencia
  "origin": "historia",                 # "historia" o "actualidad" (uso interno)
  "form": "Relato",                     # forma elegida: relato, crónica, diario...
  "paragraphs": [
    "Primer párrafo...",
    "* * *",                            # separador de partes
    "..."
  ]
}
"""
import html
import json
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "ucronias_json"
OUT = ROOT / "ucronias"
BASE = "https://elterrenocomun.github.io/el-terreno-comun"
SECTION_BREAK = "* * *"
FONTS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,500"
         "&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap")


def esc(s):
    return html.escape(str(s), quote=True)


def words(u):
    return sum(len(p.split()) for p in u["paragraphs"] if p.strip() != SECTION_BREAK)


def minutes(u):
    return max(1, round(words(u) / 220))


def page_url(u):
    return f"{BASE}/ucronias/{u['date']}-{u['slug']}.html"


FORK_SVG = """<svg class="fork" viewBox="0 0 1000 40" preserveAspectRatio="none" aria-hidden="true">
  <path class="fork-real" d="M0 12 H1000"/>
  <path class="fork-alt" d="M470 12 C 540 12, 560 30, 640 30 H1000"/>
  <circle class="fork-node" cx="470" cy="12" r="4"/>
</svg>"""


def head(title, description, rel, og_type, og_url):
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{BASE}/assets/og-image.jpg">
<meta property="og:url" content="{og_url}">
<link rel="canonical" href="{og_url}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:,">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{rel}assets/style.css">
</head>
<body>
"""


def masthead(rel, left, right):
    return f"""<header class="masthead">
  <div class="meta-row"><span>{left}</span><span>{right}</span></div>
  <p class="masthead-title"><a href="{rel}index.html">El Terreno Común</a></p>
  <p class="tagline">Crónicas de la historia que no ocurrió</p>
  {FORK_SVG}
  <nav aria-label="Secciones">
    <a href="{rel}index.html">Portada</a>
    <a href="{rel}archivo.html">Archivo</a>
  </nav>
</header>
"""


def footer(rel):
    return f"""<footer>
  <p>Todos los textos de El Terreno Común son ucronías: ficciones que parten de un hecho real y lo hacen ocurrir de otra manera.</p>
  <p><a href="{rel}index.html">Portada</a> · <a href="{rel}archivo.html">Archivo</a></p>
</footer>
"""


def kicker(u):
    return f"Ucronía · {esc(u['place'])}, {esc(u['year'])} · {esc(u['form'])}"


def body(u):
    out = []
    for p in u["paragraphs"]:
        if p.strip() == SECTION_BREAK:
            out.append('    <p class="section-break" aria-hidden="true">⁂</p>')
        else:
            out.append(f"    <p>{esc(p)}</p>")
    return "\n".join(out)


def share(u):
    url = page_url(u)
    q = urllib.parse.quote
    text = q(f"{u['title']} — una ucronía de El Terreno Común")
    return f"""<div class="share-bar">
    <span class="label">Compartir</span>
    <a class="share-btn" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?text={text}&amp;url={q(url, safe='')}">X</a>
    <a class="share-btn" target="_blank" rel="noopener" href="https://wa.me/?text={text}%20{q(url, safe='')}">WhatsApp</a>
    <button class="share-btn" type="button" data-copy="{esc(url)}"><span class="copy-label">Copiar enlace</span></button>
  </div>"""


def render_page(u):
    rel = "../"
    return (head(f"{esc(u['title'])} — El Terreno Común", esc(u["dek"]), rel, "article", page_url(u))
            + masthead(rel, f"Línea temporal n.º {u['number']}", esc(u["date_long"]))
            + f"""
<main class="wrap">
  <article>
    <header class="piece-head">
      <p class="kicker">{kicker(u)}</p>
      <h1 class="headline">{esc(u['title'])}</h1>
      <p class="dek">{esc(u['dek'])}</p>
      <p class="byline">Lectura: {minutes(u)} min</p>
    </header>
    <div class="piece-body">
{body(u)}
    </div>
  </article>
  {share(u)}
  <p class="back"><a href="../index.html">← Volver a la portada</a></p>
</main>
""" + footer(rel) + """<script src="../assets/script.js"></script>
</body>
</html>
""")


def opening(u, limit=900):
    out, total = [], 0
    for p in u["paragraphs"]:
        if p.strip() == SECTION_BREAK:
            break
        if total and total + len(p) > limit:
            break
        out.append(p)
        total += len(p)
        if total > 450:
            break
    return out


def list_item(u, rel=""):
    return f"""    <li>
      <p class="list-meta">Línea n.º {u['number']} · {esc(u['place'])}, {esc(u['year'])}</p>
      <h3><a href="{rel}ucronias/{u['date']}-{u['slug']}.html">{esc(u['title'])}</a></h3>
      <p class="list-dek">{esc(u['dek'])}</p>
    </li>"""


def render_index(items):
    latest, older = items[0], items[1:]
    href = f"ucronias/{latest['date']}-{latest['slug']}.html"
    ledes = "\n".join(f'      <p class="lede">{esc(p)}</p>' for p in opening(latest))
    older_html = ""
    if older:
        older_html = ('  <section class="older" aria-labelledby="older-h">\n'
                      '    <h2 id="older-h" class="section-title">Líneas anteriores</h2>\n'
                      '    <ul class="piece-list">\n'
                      + "\n".join(list_item(u) for u in older[:6])
                      + '\n    </ul>\n    <p class="more"><a href="archivo.html">Todo el archivo →</a></p>\n  </section>\n')
    return (head("El Terreno Común — Crónicas de la historia que no ocurrió",
                 "Ucronías: la historia que no ocurrió, contada desde El Terreno Común.", "", "website", BASE + "/")
            + masthead("", f"Línea temporal n.º {latest['number']}", esc(latest["date_long"]))
            + f"""
<main class="wrap">
  <article class="feature">
    <p class="kicker">{kicker(latest)}</p>
    <h1 class="headline"><a href="{href}">{esc(latest['title'])}</a></h1>
    <p class="dek">{esc(latest['dek'])}</p>
    <p class="byline">Lectura: {minutes(latest)} min</p>
{ledes}
    <p class="readmore"><a href="{href}">Leer la ucronía completa →</a></p>
  </article>
{older_html}</main>
""" + footer("") + """</body>
</html>
""")


def render_archive(items):
    return (head("Archivo — El Terreno Común", "Todas las ucronías publicadas.", "", "website", BASE + "/archivo.html")
            + masthead("", "Archivo", f"{len(items)} líneas temporales")
            + """
<main class="wrap">
  <h1 class="section-title page-title">Archivo de líneas temporales</h1>
  <ul class="piece-list">
""" + "\n".join(list_item(u) for u in items) + """
  </ul>
</main>
""" + footer("") + """</body>
</html>
""")


def main():
    items = [json.loads(f.read_text(encoding="utf-8")) for f in DATA.glob("*.json")]
    if not items:
        raise SystemExit("No hay ucronías en ucronias_json/.")
    items.sort(key=lambda u: (u["date"], u["number"]), reverse=True)
    OUT.mkdir(exist_ok=True)
    for u in items:
        (OUT / f"{u['date']}-{u['slug']}.html").write_text(render_page(u), encoding="utf-8")
    (ROOT / "index.html").write_text(render_index(items), encoding="utf-8")
    (ROOT / "archivo.html").write_text(render_archive(items), encoding="utf-8")
    print(f"{len(items)} ucronía(s). Última: {items[0]['title']} ({words(items[0])} palabras)")


if __name__ == "__main__":
    main()
