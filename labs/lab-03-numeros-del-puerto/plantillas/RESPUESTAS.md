# Interrogatorio del Lab 03 — Los números del puerto

> **Cómo usar este archivo**
>
> 1. Cópialo a la raíz del lab con el nombre `RESPUESTAS.md`:
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

## Pregunta 1 — El axis que colapsa

En TU sesión, ¿`matriz.sum(axis=0)` devolvió **3** números o **12**? ¿Y
`axis=1`? Explica con este ejemplo la regla "`axis` es el eje que colapsa".

(escribe aquí tu respuesta)

---

## Pregunta 2 — La máscara booleana

¿Qué meses quedaron **bajo el umbral** de $6.500.000 en TU informe? Copia el
array de `True`/`False` que imprimiste en la Guía 3 (la máscara) y marca a mano
cuáles `True` corresponden a esos meses.

(escribe aquí tu respuesta)

---

## Pregunta 3 — El error más googleado de NumPy

En la Guía 3 provocaste un `ValueError` al combinar dos arrays con `and` (en vez
de `&`). Pega aquí la **última línea** del error tal como salió en TU terminal y
explica, con tus palabras, por qué NumPy no puede decidir el valor de verdad de
un array completo.

(escribe aquí tu respuesta)

---

## Pregunta 4 — loc vs iloc

En TU sesión, ¿qué devolvió `df.iloc[6]` y a qué patente corresponde (código)?
Ahora imagina que ordenas el DataFrame por deuda descendente: ¿`iloc[6]` te daría
la MISMA patente? ¿Por qué sí o por qué no? (piensa qué mira `iloc`: ¿la etiqueta
o la posición?).

(escribe aquí tu respuesta)

---

## Pregunta 5 — Modifica y explica

En `main`, cambia el umbral de `meses_bajo_umbral` de `6_500_000` a `7_000_000`,
re-ejecuta `panorama.py` y observa qué meses aparecen **de más** en "Meses bajo
umbral". ¿Qué le dirías al Concejo con ese nuevo corte (qué significan esos meses
extra)? Luego **revierte** el umbral a $6.500.000.

(escribe aquí tu respuesta)
