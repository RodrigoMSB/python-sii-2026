# Bitácora del Analista — El Arenario

> **La defensa escrita de tu informe.** No es un cuestionario de repaso: es donde
> demuestras que entendiste lo que hiciste y por qué. El Concejo puede citarte a
> defender cada cifra.
>
> **Cómo usar este archivo**
>
> 1. Cópialo a la raíz del capstone como `BITACORA.md`:
>    - macOS/Linux: `cp plantillas/BITACORA.md BITACORA.md`
>    - Windows: `Copy-Item plantillas\BITACORA.md BITACORA.md`
> 2. Responde con **tus** resultados (los de TU `salidas/`), no con teoría.
> 3. Debajo de cada pregunta hay una línea marcadora «escribe aquí tu respuesta»
>    (entre paréntesis). Reemplázala por tu defensa. El verificador cuenta cuántas
>    quedan sin tocar.
>
> **La IA está invitada como asistente**, pero la bitácora se defiende con TUS
> números y TU criterio. El relator lo nota.

---

## Pregunta 1 — El embudo de depuración

Reproduce la secuencia de tu depuración (31 → … → 27) y justifica **cada** descarte
citando la **regla oficial del curso** que lo respalda (duplicados: gana el
primero; códigos: formato `PS-####-Y`; faltantes: imputación a 0; outliers:
consenso IQR∩z).

(escribe aquí tu respuesta)

---

## Pregunta 2 — El veredicto de los outliers

¿A quién marcó IQR y a quién z-score en tu pipeline? ¿Por qué tu depuración
**conservó a Buceo Fondo Claro** (PS-1022-T) por tercera vez en el curso, y qué
**evidencia narrativa** (de labs anteriores) respalda esa decisión frente al
outlier que sí apartaste?

(escribe aquí tu respuesta)

---

## Pregunta 3 — Los saldos negativos (el hallazgo del año)

Identifica QUÉ contribuyentes quedaron con **saldo < 0** en TU tablero y explica la
causa de cada uno. Hay **al menos dos causas distintas**: una **operacional** y una
que es **consecuencia de una regla de limpieza**. ¿Qué le recomiendas al Concejo
hacer antes de devolver dinero?

(escribe aquí tu respuesta)

---

## Pregunta 4 — Los huérfanos del año

¿Qué **pago** y qué **multas** aparecieron como huérfanos (llegaron pero no están en
el censo depurado)? Da códigos y montos, y propón un **procedimiento** para cada
caso (¿se cobran? ¿se investigan? ¿se ingresan al registro?).

(escribe aquí tu respuesta)

---

## Pregunta 5 — La retrospectiva

Si pudieras cambiar **UNA** regla oficial del pipeline (imputación a 0, consenso
IQR∩z, gana-el-primero en duplicados), ¿cuál cambiarías, **por qué**, y qué **cifra
concreta** de tu informe anual cambiaría como consecuencia?

(escribe aquí tu respuesta)
