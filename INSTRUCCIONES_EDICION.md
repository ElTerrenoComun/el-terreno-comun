# Instrucciones para cada ucronía

El Terreno Común publica **una ucronía cada tres días**: un único texto largo
que parte de un hecho real y lo hace ocurrir de otra manera. La tarea programada
se ejecuta todos los días a las 19:16 (hora de Madrid) y decide aquí si le toca
publicar. Si quieres cambiar el criterio, cambia este archivo: la tarea lo lee
en cada ejecución.

## 1. ¿Toca publicar hoy?

- La fecha es la de hoy en Madrid (Europe/Madrid).
- Mirar el campo `"date"` de la ucronía más reciente en `ucronias_json/`.
- Si se publicó hace menos de tres días (por ejemplo, el día 16 → la siguiente
  es el 19), **no se hace nada más**: la ejecución termina aquí.
- Si han pasado tres días o más, se publica.
- El número de la nueva ucronía (`"number"`) es el de la más reciente más uno.

## 2. El punto de divergencia

Cada ucronía parte de un **punto de divergencia**: un hecho real, concreto y
fechado que en el texto ocurre de otra manera.

- **De cualquier parte del mundo.** No hay preferencia por España: Europa,
  América, Asia, África, Oriente Próximo... Variar de región de una entrega a
  la siguiente.
- **Se alterna el origen.** Una entrega parte de la actualidad (un hecho de
  las últimas semanas: una votación, un decreto, una sentencia, unas
  elecciones, un acuerdo, una dimisión que no se produjo...) y la siguiente de
  la historia (cualquier época). Para saber cuál toca, mirar el campo
  `"origin"` de la última ucronía (`"actualidad"` o `"historia"`) y usar el
  otro. Solo se repite si el hecho del momento lo justifica claramente.
- Para la actualidad, buscar los hechos en: eldiario.es, theobjective.com,
  euronews.com en español, jotdown.es, ethic.es y búsquedas web, también en
  prensa internacional. Para la historia, documentarse en fuentes fiables antes
  de escribir.
- No repetir un punto de divergencia, una época o un país ya tratados en las
  cinco ucronías anteriores.
- El mejor punto de divergencia no es el más espectacular, sino el que deja
  ver una estructura: lo que habría cambiado y, sobre todo, lo que **no** habría
  cambiado aunque el hecho fuera otro.

## 3. Escritura

Antes de escribir, leer entero `GUIA_POSICIONAMIENTO.md` y cargar la skill
`el-terreno-comun-voz`. La ucronía es ficción, pero mira el mundo desde la línea
de la publicación: posicionada, incisiva, sin equidistancias. Lo que dicen este
archivo y la guía prevalece sobre la skill.

- **Extensión:** entre 3.000 y 5.000 palabras.
- **Forma libre**, la que mejor sirva a cada historia: relato con personajes y
  escenas, crónica escrita desde el mundo alternativo, diario, cartas, informe
  oficial, reportaje, discurso, actas, una mezcla. Variar la forma de una
  entrega a otra.
- **Voz:** la de El Terreno Común. Los registros analítico y raíz pueden
  convivir dentro del mismo texto según lo pida la forma.
- **Rigor en la parte real.** Todo lo anterior al punto de divergencia es
  historia verdadera y debe ser exacto: fechas, cargos, lugares, cifras,
  contexto. La verosimilitud del mundo alternativo depende de eso. A partir del
  punto de divergencia, la invención sigue una lógica plausible: consecuencias
  políticas, económicas y sociales coherentes con lo que se sabe de esa época
  y de sus actores.
- **Figuras y personajes públicos:** pueden aparecer con libertad, con nombre
  y apellidos, actuar, hablar y decidir en el mundo alternativo. Las personas
  privadas que hayan sido noticia (víctimas, testigos, vecinos) no se nombran:
  se describen.
- **Sin subtítulos intermedios.** Para separar partes, escenas o cambios de
  tiempo se usa un párrafo que contenga solo `* * *`, que la web convierte en
  un separador.
- Sin moraleja ni llamada a la acción. El final cae seco, en una imagen.
- No se citan las fuentes ni se nombra a los autores que construyeron la voz.

## 4. Ficha de la ucronía

Cada ucronía es un archivo `ucronias_json/AAAA-MM-DD-slug.json` con la forma que
describe la cabecera de `generate_ucronia.py`:

- `"date"` y `"date_long"`: fecha de publicación (`"2026-10-19"`,
  `"19 de octubre de 2026"`).
- `"number"`: número de línea temporal.
- `"slug"`: título corto en minúsculas con guiones.
- `"title"`: titular. `"dek"`: una frase de bajada.
- `"place"`, `"divergence_date"`, `"year"`: lugar, fecha completa y año del
  punto de divergencia.
- `"origin"`: `"actualidad"` o `"historia"`.
- `"form"`: la forma elegida (`"Crónica"`, `"Relato"`, `"Diario"`, `"Cartas"`...).
- `"real"`: una o dos frases sobre lo que ocurrió de verdad.
- `"alternate"`: una o dos frases sobre lo que ocurre de otra manera en el texto.
- `"paragraphs"`: los párrafos, con `"* * *"` como separador cuando haga falta.

`"real"` y `"alternate"` son obligatorios: forman la ficha del punto de
divergencia que encabeza cada ucronía en la web.

## 5. Generación

1. Guardar la ucronía en `ucronias_json/`.
2. Ejecutar `python3 generate_ucronia.py`. Regenera la página de cada
   ucronía, la portada (la nueva, destacada, y las anteriores debajo) y el
   archivo.
3. Comprobar que `index.html` muestra la ucronía nueva y que su página se abre
   bien.

## 6. Publicación

- Autor de los commits, siempre:
  `El Terreno Común <341140003+ElTerrenoComun@users.noreply.github.com>`.
  Nunca un nombre real ni un correo personal.
- En las páginas publicadas no debe aparecer en ningún sitio que los textos se
  generan de forma automática.
- Mensaje de commit: `Ucronía del AAAA-MM-DD`.
- `git push` a la rama `main`. GitHub Pages publica solo en un minuto o dos.
