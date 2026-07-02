# Interrogatorio del Lab 06 — Transformar y combinar

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

## Pregunta 1 — El borde del tramo

Según TU ejecución, ¿en qué tramo cayó una deuda de **exactamente $100.000**?
¿Qué regla de `pd.cut` lo decide (borde derecho incluyente o excluyente) y cómo
lo verificaste?

(escribe aquí tu respuesta)

---

## Pregunta 2 — Las tres uniones

En TU demo de la Guía 3, ¿cuántas filas obtuviste con `merge` usando `how="left"`,
`how="inner"` y `how="outer"`? Explica cada número con la analogía de **carpetas
(censo) y boletas (pagos)**.

(escribe aquí tu respuesta)

---

## Pregunta 3 — Los huérfanos

¿Qué códigos aparecieron como **pagos huérfanos** en TU informe, cuánto suman, y
de qué **lab del curso** provienen esos contribuyentes? ¿Qué le recomendarías a
Don Arquímedes hacer con esa plata?

(escribe aquí tu respuesta)

---

## Pregunta 4 — agg vs transform

En TUS resultados, ¿qué **largo** (número de filas) tiene la salida del
`groupby`-agg del saldo por rubro, y qué largo la del `transform` del `pct_rubro`?
¿Por qué esa diferencia es exactamente lo que necesita cada caso?

(escribe aquí tu respuesta)

---

## Pregunta 5 — Modifica y explica

En `construir_tablero`, cambia el merge de `how="left"` a `how="inner"`, re-ejecuta
`tablero.py` y observa: ¿qué pasó con el **total del saldo** y con los
**contribuyentes sin pago**? ¿Por qué `left` es la decisión correcta para un
tablero de cobranza? **Revierte** al terminar.

(escribe aquí tu respuesta)
