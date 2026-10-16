# Instrucciones para generar cada entrega

Desde el 17 de octubre de 2026, El Terreno Común publica **una ucronía cada
tres días**: un único texto largo que imagina cómo habría sido la historia si un
hecho hubiera ocurrido de otra manera. Las ediciones diarias de artículos
anteriores se conservan en la hemeroteca.

La tarea programada se ejecuta todos los días a las 19:16 (hora de Madrid) y
decide aquí si le toca publicar. Si quieres cambiar el criterio, cambia este
archivo: la tarea lo lee en cada ejecución.

## 1. ¿Toca publicar hoy?

- La fecha es la de hoy en Madrid (Europe/Madrid).
- Mirar en `ediciones_json/` la última entrega cuya pieza tenga
  `"voice": "ucronia"`.
- Si existe y se publicó hace menos de tres días (por ejemplo, el día 17 →
  la siguiente es el 20), **no se hace nada más**: la ejecución termina aquí.
- Si no hay ninguna ucronía todavía, o han pasado tres días o más, se publica.
- Si ya existe `ediciones/AAAA-MM-DD.html` para hoy, tampoco se hace nada.
- El número de edición es el número de entradas de `hemeroteca.html` más uno.

## 2. El punto de divergencia

Cada ucronía parte de un **punto de divergencia**: un hecho real, concreto y
fechado que en el texto ocurre de otra manera.

- **Se alterna el origen.** Una entrega parte de la actualidad (un hecho de
  las últimas semanas: una votación, un decreto, una sentencia, un estreno,
  una dimisión que no se produjo...) y la siguiente de la historia (cualquier
  época, con preferencia por la de España: 1492, 1808, 1898, 1931, 1936, 1977,
  1981, 2004, 2008, 2011...). Para saber cuál toca, mirar el campo `"origin"`
  de la última ucronía (`"actualidad"` o `"historia"`) y usar el otro. Solo se
  repite si el hecho del momento lo justifica claramente.
- Para la actualidad, buscar los hechos en: eldiario.es, theobjective.com,
  euronews.com en español, jotdown.es, ethic.es y búsquedas web. Para la
  historia, documentarse en fuentes fiables antes de escribir.
- No repetir un punto de divergencia ni un tema ya tratado en las cinco
  entregas anteriores.
- El mejor punto de divergencia no es el más espectacular, sino el que deja
  ver una estructura: lo que habría cambiado, y sobre todo lo que **no** habría
  cambiado aunque el hecho fuera otro.

## 3. Escritura

Antes de escribir, leer entero `GUIA_POSICIONAMIENTO.md` y cargar la skill
`el-terreno-comun-voz`. La ucronía es ficción, pero mira el mundo desde la línea
de la publicación: posicionada, incisiva, sin equidistancias. Lo que dicen este
archivo y la guía prevalece sobre la skill.

- **Extensión:** entre 3.000 y 5.000 palabras.
- **Forma libre**, la que mejor sirva a cada historia: relato con personajes y
  escenas, crónica periodística escrita desde el mundo alternativo, diario,
  cartas, informe oficial, reportaje, discurso, una mezcla. Cada entrega puede
  ser distinta de la anterior.
- **Voz:** la de El Terreno Común. Los registros analítico y raíz pueden
  convivir dentro del mismo texto según lo pida la forma.
- **Rigor en la parte real.** Todo lo anterior al punto de divergencia es
  historia verdadera y debe ser exacto: fechas, cargos, lugares, contexto. La
  verosimilitud del mundo alternativo depende de eso. A partir del punto de
  divergencia, la invención debe seguir una lógica plausible: consecuencias
  políticas, económicas y sociales coherentes con lo que se sabe de esa época
  y esos actores.
- **Personas reales.** Las figuras públicas pueden aparecer en su papel
  público. En las ucronías de actualidad, los protagonistas de las escenas
  íntimas son personajes inventados. No se atribuyen a personas reales vivas
  delitos, escándalos privados ni declaraciones que puedan pasar por reales
  fuera de la ficción.
- **Sin subtítulos intermedios.** Para separar partes, escenas o cambios de
  tiempo se usa un párrafo que contenga solo `* * *`, que la web convierte en
  un separador.
- Sin moraleja ni llamada a la acción. El final cae seco, en una imagen.
- No se citan las fuentes ni se nombra a los autores que construyeron la voz.

## 4. Ficha de la entrega

El JSON de la edición tiene la forma que describe la cabecera de
`generate_edition.py`, con **un único artículo** y estos campos:

- `"slug"`: título corto en minúsculas con guiones.
- `"title"`: titular.
- `"dek"`: una frase de bajada.
- `"section"`: `"Ucronía — "` más lugar y año del punto de divergencia (por
  ejemplo `"Ucronía — España, 1981"`).
- `"voice"`: siempre `"ucronia"`.
- `"origin"`: `"actualidad"` o `"historia"`.
- `"divergence"`: una o dos frases que explican qué ocurrió en realidad y qué
  ocurre de otra manera en el texto. Es lo que deja claro al lector que está
  ante una ficción, así que es obligatorio.
- `"paragraphs"`: los párrafos, con `"* * *"` como separador cuando haga falta.

## 5. Generación

1. Guardar la entrega en `ediciones_json/edicion_AAAA-MM-DD.json`.
2. Ejecutar `python3 generate_edition.py ediciones_json/edicion_AAAA-MM-DD.json`.
   Con un solo artículo, la portada lo muestra destacado, con su punto de
   divergencia y el tiempo de lectura.
3. Comprobar que `index.html` muestra la entrega nueva y que la página del
   artículo se abre bien.

## 6. Publicación

- Autor de los commits, siempre:
  `El Terreno Común <341140003+ElTerrenoComun@users.noreply.github.com>`.
  Nunca un nombre real ni un correo personal.
- En las páginas publicadas no debe aparecer en ningún sitio que los textos se
  generan de forma automática.
- Mensaje de commit: `Ucronía del AAAA-MM-DD`.
- `git push` a la rama `main`. GitHub Pages publica solo en un minuto o dos.
