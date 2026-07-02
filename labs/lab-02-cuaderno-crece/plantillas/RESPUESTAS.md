# Interrogatorio del Lab 02 — El cuaderno crece

> **Cómo usar este archivo**
>
> 1. Cópialo a la raíz del lab con el nombre `RESPUESTAS.md`:
>    - macOS/Linux: `cp plantillas/RESPUESTAS.md RESPUESTAS.md`
>    - Windows: `Copy-Item plantillas\RESPUESTAS.md RESPUESTAS.md`
> 2. Responde **con tus propias palabras**, mirando lo que pasó en TU terminal.
>    Varias preguntas dependen de lo que TÚ ejecutaste.
> 3. Debajo de cada pregunta hay una línea marcadora «escribe aquí tu
>    respuesta» (entre paréntesis). Reemplázala por tu explicación. El
>    verificador cuenta cuántas de esas líneas marcadoras quedan sin tocar.
>
> **La IA está invitada, no prohibida.** Que te explique conceptos; la respuesta
> la escribes tú, entendiéndola.

---

## Pregunta 1 — El KeyError de la Guía 2

En la Guía 2 provocaste un `KeyError` al pedir una clave inexistente de un
diccionario con corchetes `[]`. Pega aquí la **última línea** del error tal como
salió en TU terminal y explica qué habría devuelto `.get()` en ese mismo caso
(en vez de reventar).

(escribe aquí tu respuesta)

---

## Pregunta 2 — Duplicados

Según TU informe de consolidación, ¿qué código fue rechazado por **duplicado**?
¿Por qué quedó la PRIMERA aparición y no la segunda? Cita la línea de la función
`consolidar` que toma esa decisión.

(escribe aquí tu respuesta)

---

## Pregunta 3 — Los números de TU consolidación

Mirando `salidas/informe_consolidacion.txt`: ¿cuántas **fichas consolidadas**,
cuántos **rechazados** y cuál es la **deuda total consolidada**? Y una fina: la
deuda total, ¿incluye a las patentes **SUSPENDIDAS**? Justifica mirando el código
(qué suma `construir_informe` / `deuda_por_rubro`).

(escribe aquí tu respuesta)

---

## Pregunta 4 — La sesión de pdb

Cuando insertaste `breakpoint()` y recorriste el bucle de `consolidar`, ¿en qué
registro del archivador estabas cuando el programa entró al `except` (o sea, cuál
tenía la deuda que no se pudo convertir)? Indica el **código** y el contenido de
su `deuda`, y qué **comando de pdb** usaste para inspeccionarlo.

(escribe aquí tu respuesta)

---

## Pregunta 5 — Modifica y explica

Cambia la regla de duplicados para que gane el **ÚLTIMO** visto (pista: asignar
`fichero[codigo] = ficha` sin preguntar `in`). Re-ejecuta el programa. ¿Qué
cambió en el informe y por qué importa en términos del municipio (qué versión de
una patente repetida queda registrada)? Luego **revierte** para dejar la regla
correcta (gana el primero).

(escribe aquí tu respuesta)
