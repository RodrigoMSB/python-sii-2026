# Interrogatorio del Lab 05 — La gran limpieza

> **Cómo usar este archivo**
>
> 1. Cópialo a la raíz del lab como `RESPUESTAS.md`:
>    - macOS/Linux: `cp plantillas/RESPUESTAS.md RESPUESTAS.md`
>    - Windows: `Copy-Item plantillas\RESPUESTAS.md RESPUESTAS.md`
> 2. Responde **con tus propias palabras**, mirando lo que pasó en TU terminal.
> 3. Debajo de cada pregunta hay una línea marcadora «escribe aquí tu
>    respuesta» (entre paréntesis). Reemplázala por tu explicación. El
>    verificador cuenta cuántas de esas líneas marcadoras quedan sin tocar.
>
> **La IA está invitada, no prohibida.** Que te explique; la respuesta la
> escribes tú.

---

## Pregunta 1 — El diagnóstico

Antes de limpiar, corriste `value_counts()` sobre `estado`. ¿Cuántas **variantes
crudas** encontraste y cuáles eran (nómbralas)? ¿Cuántas quedaron **tras
homogeneizar**?

(escribe aquí tu respuesta)

---

## Pregunta 2 — El embudo

Copia de TU informe la secuencia del embudo (30 → … → 25) y explica qué se perdió
en **cada** salto y por qué está justificado (no basta con el número: di qué tipo
de fila se fue en cada etapa).

(escribe aquí tu respuesta)

---

## Pregunta 3 — El desacuerdo de los métodos

¿Qué códigos marcó TU `outliers_iqr` y cuáles TU `outliers_z`? ¿Por qué **difieren**?
Según tu reporte, ¿cuál fue el **veredicto final** de cada outlier (conservado o
apartado) y con qué argumento?

(escribe aquí tu respuesta)

---

## Pregunta 4 — La regla de negocio

¿Cuántas deudas **imputó** tu pipeline y con qué **valor**? ¿Qué **riesgo** tiene
esa regla (imputar 0) para el municipio, y qué **alternativa** ofrecía pandas que
viste en la Guía 2?

(escribe aquí tu respuesta)

---

## Pregunta 5 — Modifica y explica

En `limpiar_censo`, cambia el umbral del z-score de `3.0` a `2.0` (parámetro
`umbral_z`), re-ejecuta y observa: ¿cambiaron los códigos que marca `outliers_z`?
¿Cambió el **consenso** (los apartados) y por tanto el censo final? Explica qué
implica bajar el umbral, y **revierte** a `3.0`.

(escribe aquí tu respuesta)
