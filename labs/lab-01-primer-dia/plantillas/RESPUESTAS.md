# Interrogatorio del Lab 01 — El primer día en Rentas

> **Cómo usar este archivo**
>
> 1. Cópialo a la raíz del lab con el nombre `RESPUESTAS.md`:
>    - macOS/Linux: `cp plantillas/RESPUESTAS.md RESPUESTAS.md`
>    - Windows: `Copy-Item plantillas\RESPUESTAS.md RESPUESTAS.md`
> 2. Responde **con tus propias palabras**, mirando lo que pasó en TU terminal.
>    No hay respuestas "de libro": varias preguntas dependen de lo que TÚ
>    ejecutaste.
> 3. Debajo de cada pregunta hay una línea marcadora «escribe aquí tu
>    respuesta» (entre paréntesis). Reemplázala por tu explicación. El
>    verificador cuenta cuántas de esas líneas marcadoras quedan sin tocar.
>
> **La IA está invitada, no prohibida.** Puedes pedirle a una IA que te explique
> un concepto. Pero la respuesta la escribes tú, entendiéndola: el interrogatorio
> vive en tu terminal y en tu cabeza, no en un chat.

---

## Pregunta 1 — La rotura de la Guía 2

En la Guía 2 provocaste un `TypeError` a propósito al intentar concatenar texto
con un número. Pega aquí la **última línea** del error tal como apareció en TU
terminal y explica, con tus palabras, qué te está diciendo Python.

(escribe aquí tu respuesta)

---

## Pregunta 2 — Slicing sobre el código de patente

Tomando un código como `"PS-1007-T"`, explica cómo extraerías la **letra de
rubro** (la última, `T`) usando slicing o indexación. Explica además por qué
`codigo[-1]` también funciona para obtenerla.

(escribe aquí tu respuesta)

---

## Pregunta 3 — El número de tu triaje

Mirando el informe que generó TU `triaje.py`: ¿cuántas patentes **vencidas**
hay y cuál es la **deuda total**? Y algo más fino: la deuda total, ¿incluye o no
los $45.000 del **Café La Palanca**, que está **VIGENTE**? Justifica tu respuesta
mirando qué hace la función `deuda_total`.

(escribe aquí tu respuesta)

---

## Pregunta 4 — Predicción de pertenencia

En la Guía 4 armaste a mano una lista `vencidas` y probaste
`"PS-1013-C" in vencidas`. ¿Qué resultado dio (`True` o `False`)? ¿Coincidió con
lo que habías **predicho**? Explica por qué el resultado tiene sentido sabiendo
que la Botillería La Sirena (`PS-1013-C`) está **SUSPENDIDA**, no **VENCIDA**.

(escribe aquí tu respuesta)

---

## Pregunta 5 — Modifica y explica

En tu `triaje.py`, dentro de `codigos_vencidas`, cambia la condición
`== "VENCIDA"` por `!= "VIGENTE"` y vuelve a ejecutar el triaje. ¿Qué códigos
aparecen **de más** en la lista? ¿Qué significan en términos del municipio (qué
tipo de patentes se colaron)? Explica y luego **revierte** el cambio para dejar
tu código correcto.

(escribe aquí tu respuesta)
