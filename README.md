# El Terreno Común — Ucronías

Web estática y ligera, sin frameworks: *Crónicas de la historia que no ocurrió*.
Cada tres días publica una ucronía: un texto largo (3.000–5.000 palabras) que
parte de un hecho real, de la actualidad o de la historia y de cualquier parte
del mundo, y lo hace ocurrir de otra manera.

## Estructura

```
index.html                 portada: la última ucronía destacada y las anteriores
archivo.html               todas las ucronías publicadas
ucronias/                  una página por ucronía
ucronias_json/             el texto y la ficha de cada ucronía (la fuente)
assets/style.css           diseño
assets/script.js           botón de copiar enlace
assets/og-image.jpg        imagen al compartir en redes
generate_ucronia.py        regenera toda la web a partir de ucronias_json/
INSTRUCCIONES_EDICION.md   pauta de cada entrega (la lee la tarea programada)
GUIA_POSICIONAMIENTO.md    línea editorial de El Terreno Común
```

## Publicar una ucronía

1. Guardar el JSON en `ucronias_json/` (formato en la cabecera de
   `generate_ucronia.py`).
2. `python3 generate_ucronia.py`
3. Commit y push a `main`. GitHub Pages publica en uno o dos minutos.

La tarea programada se ejecuta cada día a las 19:16 (hora de Madrid),
comprueba si han pasado tres días desde la última ucronía y, si toca, sigue
`INSTRUCCIONES_EDICION.md`.

## Diseño

Archivo de líneas temporales: papel de archivo, titulares en Cormorant
Garamond, texto en Source Serif 4 y datos en IBM Plex Mono. El motivo gráfico
es una línea que se bifurca: la continua es la historia real; la discontinua,
en rojo óxido, la que no ocurrió. Cada ucronía abre con una ficha de su punto
de divergencia, "Lo que ocurrió" frente a "Lo que ocurre aquí". Modo oscuro
automático.
