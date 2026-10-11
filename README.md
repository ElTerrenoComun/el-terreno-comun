# El Terreno Común — Diario

Web ligera, estática, sin frameworks ni base de datos. Una edición nueva cada día,
generada reinterpretando los hechos de la jornada con la voz editorial de
*El Terreno Común* (voz analítica por defecto, voz raíz cuando el hecho encaja mejor
en ese registro).

## Estructura

```
index.html              ← portada (siempre la edición del día más reciente)
hemeroteca.html          ← listado de todas las ediciones pasadas
ediciones/YYYY-MM-DD.html ← copia fija de cada portada, para que el enlace no cambie
articulos/YYYY-MM-DD-slug.html ← cada artículo, con su propia URL permanente
assets/style.css         ← todo el diseño (periódico antiguo, tipografía Playfair Display + Source Serif 4)
assets/script.js         ← solo el botón "copiar enlace"
assets/og-image.jpg      ← imagen que aparece al compartir en redes
generate_edition.py      ← script que monta la edición del día a partir de un JSON
```

No hay build step, ni Node, ni dependencias de JavaScript. Es HTML y CSS servidos tal cual.

## Cómo se genera cada edición

1. Un proceso (la tarea programada diaria, ver más abajo) busca los hechos más
   relevantes del día — política, sociedad, economía, cultura, España e
   internacional — y redacta un artículo por cada uno siguiendo el proceso de la
   voz de El Terreno Común: identificar el hecho, buscar la estructura que hay
   detrás, los dos relatos disponibles y lo que ninguno de los dos puede ver,
   terminando donde el análisis se agota. Sin subtítulos, sin solución, sin citar
   la fuente de la noticia.
2. Esos artículos se guardan como un JSON con la forma que describe la cabecera
   de `generate_edition.py`.
3. Se ejecuta `python3 generate_edition.py edicion_YYYY-MM-DD.json`. Esto:
   - crea un archivo HTML por artículo en `articulos/`
   - sobrescribe `index.html` con la portada del día
   - guarda una copia fija de esa portada en `ediciones/YYYY-MM-DD.html`
   - añade una entrada a `hemeroteca.html`
4. Se hace `git add -A && git commit -m "Edición del YYYY-MM-DD" && git push`.
   GitHub Pages redespliega solo, en menos de un minuto.

Los artículos y portadas de días anteriores nunca se tocan: cada día solo añade
archivos nuevos y reescribe `index.html` y `hemeroteca.html`.

## Puesta en marcha en GitHub Pages (gratis)

1. Crea un repositorio (puede ser público o privado — Pages gratuito en repos
   privados requiere GitHub Pro, así que si quieres privacidad real hay que
   valorarlo; lo habitual para esto es un repo público, ya que el contenido
   está pensado para compartirse).
2. Sube el contenido de esta carpeta a la rama `main`, en la raíz del repo.
3. Añade un archivo vacío llamado `.nojekyll` en la raíz (ya incluido aquí) para
   que GitHub no intente procesar el sitio con Jekyll.
4. En el repositorio: **Settings → Pages → Build and deployment → Source: Deploy
   from a branch → Branch: main / (root)**.
5. GitHub te da una URL del tipo `https://TU-USUARIO.github.io/TU-REPO/`. Puedes
   apuntar un dominio propio desde la misma pantalla si lo tienes.
6. La URL del sitio está fijada en `DEFAULT_BASE` dentro de `generate_edition.py`;
   si algún día usas un dominio propio, cámbiala ahí.

## La tarea diaria

Una tarea programada de Claude se ejecuta cada día a las 20:00 (hora de Madrid)
y sigue la pauta de `INSTRUCCIONES_EDICION.md`: busca los hechos del día, escribe
al menos seis artículos con la voz de El Terreno Común, genera las páginas con
`generate_edition.py` y publica. Para cambiar el criterio editorial basta con
editar ese archivo.

## Diseño

Pensado para parecer un periódico de verdad, no una maqueta de "periódico": sin
degradados, sin iconos redondos, sin tarjetas con sombra. Tipografía Playfair
Display para titulares, Source Serif 4 para cuerpo de texto, fondo color papel
envejecido (con variante automática para modo oscuro), capitulares, filetes en
vez de líneas de interfaz. Los artículos en voz raíz llevan una pequeña etiqueta
en cursiva, "Voz raíz", como único marcador visual del cambio de registro.
