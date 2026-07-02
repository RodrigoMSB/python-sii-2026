# Interrogatorio del Lab 04 — Las cuatro fuentes

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

## Pregunta 1 — La boleta sin timbre

En la demo de la Guía 4 insertaste una fila **sin** hacer `commit`, cerraste la
conexión y volviste a abrir la BD. ¿La fila **estaba** o **no estaba**? Explica,
con la analogía de la caja municipal, qué protege ese comportamiento.

(escribe aquí tu respuesta)

---

## Pregunta 2 — El rollback real

Según TU informe, ¿qué retornó `registrar_pago` con el código `PS-9999-X`?
¿Cuántas filas tenía `pagos_registrados` **antes** y **después** de ese intento?
¿Qué línea de tu `registrar_pago` garantiza que no quede "media boleta"?

(escribe aquí tu respuesta)

---

## Pregunta 3 — Los dos caminos del JSON

En TU sesión, ¿qué **tipo de dato Python** te devolvió `json.load` al leer
`multas.json`? ¿En qué caso preferirías ese camino (stdlib) sobre
`pd.read_json` directo?

(escribe aquí tu respuesta)

---

## Pregunta 4 — El dtype del dinero

Mirando `df.info()` de los pagos, ¿con qué **dtype** llegó la columna `monto` del
CSV? Y una hipótesis: si Tesorería hubiera escrito los montos como `"45.000"`
(con punto de miles), ¿qué habría pasado con ese dtype y qué **perilla** de
`read_csv` lo arreglaría?

(escribe aquí tu respuesta)

---

## Pregunta 5 — Modifica y explica

En `main`, cambia el pago **válido** (`PS-1031-G`) por un código que **NO** esté
en `contribuyentes` (por ejemplo `PS-0000-Z`). Re-ejecuta `fuentes.py` y observa:
¿qué cambió en el informe (línea "Pago válido") y en la tabla
`pagos_registrados`? Explica por qué, y **revierte** al terminar.

(escribe aquí tu respuesta)
