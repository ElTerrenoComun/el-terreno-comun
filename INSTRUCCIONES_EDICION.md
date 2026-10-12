# Instrucciones para generar la edición diaria

Este documento es la pauta que sigue la tarea programada cada día a las 20:00
(hora de Madrid). Si quieres cambiar el criterio editorial, cambia este archivo:
la tarea lo lee en cada ejecución.

## 1. Fecha y número de edición

- La fecha es la de hoy en Madrid (Europe/Madrid).
- Si ya existe `ediciones/AAAA-MM-DD.html` para hoy, no se genera nada: la
  edición del día ya está publicada.
- El número de edición es el número de entradas de `hemeroteca.html` más uno.

## 2. Búsqueda de hechos

Buscar los hechos más relevantes de la jornada (últimas 24 horas) en política,
sociedad, economía y cultura, de España e internacionales. Fuentes de partida:

- Prensa generalista: eldiario.es (portada), theobjective.com (portada),
  euronews.com en español, y búsquedas web generales sobre la actualidad del día.
  Consultar medios de distinto signo sirve para encontrar hechos; la lectura
  de cada hecho es siempre la de El Terreno Común, no la del medio.
- Cultura y piezas de fondo: jotdown.es.
- Si un medio no es accesible, se sigue con los demás; no se intenta saltar
  bloqueos.

Abrir las páginas de las que se toman datos: un titular o un fragmento de
búsqueda no basta para escribir un artículo.

Evitar repetir un tema tratado en las tres ediciones anteriores, salvo que haya
un hecho nuevo y sustancial.

## 3. Selección

- **Al menos seis artículos.** Más si la jornada lo justifica.
- Repartidos entre política, sociedad, economía, cultura e internacional. Al
  menos uno de cultura.

## 4. Escritura

Cada artículo se escribe con la skill `el-terreno-comun-voz`, con estas
precisiones, que prevalecen sobre la skill:

- **Nada de confrontación de dos relatos.** No se estructura el artículo como
  "el relato de unos / el relato de otros", ni "por un lado / por otro", ni se
  reparte el texto entre dos posiciones contrapuestas. El artículo sigue una
  sola línea de lectura: el hecho, la estructura que hay detrás, la
  contradicción que revela, y se detiene donde el análisis se agota.
- **Tono:** el registro analítico de la voz, frío, con ironía clásica y
  irritación de fondo. No se busca la frase lapidaria por sí misma.
- **Extensión:** entre 600 y 1.000 palabras por artículo. La decide el
  argumento.
- **Voz normal o voz raíz** según encaje mejor con cada hecho. Lo habitual es
  una o dos piezas en voz raíz por edición, cuando el hecho toca el cuerpo, lo
  íntimo o lo vivido.
- Se mantienen las prohibiciones de la skill: sin subtítulos, sin soluciones,
  sin moraleja ni llamada a la acción, sin citar la fuente de la noticia, sin
  nombrar a los autores que construyeron la voz.
- **Exactitud:** solo hechos comprobados en las fuentes. Lo que sea una
  acusación o una investigación abierta se dice así. No se atribuyen delitos
  no juzgados a personas con nombre y apellidos.

Cada artículo lleva: titular, bajada (una frase), sección (por ejemplo
"Política — España", "Economía", "Cultura", "Internacional — Europa"), voz
("normal" o "raiz") y los párrafos.

## 5. Generación

1. Guardar los artículos en `ediciones_json/edicion_AAAA-MM-DD.json` con la
   forma que describe la cabecera de `generate_edition.py`.
2. Ejecutar `python3 generate_edition.py ediciones_json/edicion_AAAA-MM-DD.json`.
3. Comprobar que `index.html` muestra los artículos nuevos y que cada archivo de
   `articulos/` se abre bien.

## 6. Publicación

- Autor de los commits, siempre:
  `El Terreno Común <341140003+ElTerrenoComun@users.noreply.github.com>`.
  Nunca un nombre real ni un correo personal.
- En las páginas publicadas no debe aparecer en ningún sitio que la edición
  se genera de forma automática (ni en cabecera, ni en pie, ni en textos).
- Mensaje de commit: `Edición del AAAA-MM-DD`.
- `git push` a la rama `main`. GitHub Pages publica solo en un minuto o dos.
