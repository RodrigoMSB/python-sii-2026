# Certificación del SPEC-014 — Corrección doctrinal del `with` de sqlite3 (Lab 04)

> Reporte del barrido a las **guías** del Lab 04: la afirmación falsa "el `with`
> cierra la conexión" —ya curada en `troubleshooting.md` por SPEC-012, pero viva
> en la superficie que leen *todos* los alumnos— convertida en un 💥 Rómpelo y
> reemplazada por el patrón profesional `try: with con: … finally: con.close()`.

## Datos de la corrida

| Ítem | Valor |
|------|-------|
| Fecha | 2026-07-17 |
| Máquina (T1–T5, local) | macOS 26.5.1 (build 25F80), Apple Silicon · `uv` 0.9.18 |
| Python resuelto | **3.13** (gestionado por `uv` en los labs) |
| Método | Cambios acotados a 3 rutas de doc; regresión con el verificador oficial en copia de trabajo (artefactos gitignored) |
| Alcance | **Solo documentación.** Cero código de labs/bin/soluciones/plantillas tocado. |

## Archivos modificados (3 rutas, sin colaterales)

| Arreglo | Archivo | Qué cambió |
|---------|---------|------------|
| **A** — la guía estrella | `labs/lab-04-cuatro-fuentes/guia/04-base-de-datos.md` | A.1 promesa falsa (C11 + WinError 32) · A.2 sección "cierre automático" → **💥 Rómpelo** + patrón profesional · A.3 Checkpoint |
| **B** — el consolidado | `labs/lab-04-cuatro-fuentes/guia/05-consolidado.md` | Snippet `gestion.db`: patrón prohibido → `try/finally: con.close()` |
| **C** — el README | `labs/lab-04-cuatro-fuentes/README.md` | "patrón `with`" (objetivo) → "`with con:` transaccional y cierre explícito (C11)" |

## Resultado por prueba

| Prueba | Veredicto | Evidencia breve |
|--------|-----------|-----------------|
| **T1** Regresión (código intacto) | ✅ CUMPLE | Con el código sin tocar, flujo feliz sobre copia de trabajo: **Lab 04 → `✔ 12/12`** y **Capstone → `✔ 9/9`**. La transacción real (commit del pago válido, rollback del inexistente) sigue verde. El spec es solo-doc; el verificador confirma que nada del código se rozó. |
| **T2** Barrido doctrinal | ✅ CUMPLE | `grep -rn "with sqlite3.connect" labs/` → **cero** ocurrencias como *recomendación*. Las 8 restantes son legítimas: la demo del propio 💥 Rómpelo (guía 04, presentada como trampa) + su explicación y prohibición (C11), comentarios de `bin/verificar.py` y los dos `generar_fuentes.py`, y la advertencia de `troubleshooting.md`. |
| **T3** Verdad ejecutable | ✅ CUMPLE | Ejecutado el snippet del nuevo Rómpelo: tras `with sqlite3.connect(...)`, `con.execute("SELECT COUNT(*) …").fetchone()` → `(1,)` y `con.execute("SELECT 1")` **no** lanza `ProgrammingError`. **La conexión sigue viva.** La guía dice lo comprobable en la terminal del alumno. |
| **T4** Coherencia | ✅ CUMPLE | `grep -rn "cierre automático\|cierra sola\|se cierra solo" labs/` → **cero**. Ningún rastro de la vieja promesa falsa. |
| **T5** Árbol limpio | ✅ CUMPLE | `git status --short` → **solo** las 3 rutas del §2–§4 (`guia/04-…md`, `guia/05-…md`, `README.md`). Los artefactos de la regresión (`fuentes.py`, `RESPUESTAS.md`, `arenario.py`, `BITACORA.md`, `salidas/`) son gitignored y se limpiaron; cero colaterales. |

## Detalle de la corrección

**La distinción que es la lección.** `with sqlite3.connect(ruta)` abre una
conexión y, al salir del bloque, hace **commit** — pero **no** `close()`: el
handle queda vivo. `with con:` sobre una conexión **ya abierta** es el context
manager **transaccional** legítimo (commit al salir, rollback si hay excepción).
El patrón profesional combina ambos y honra C11:

```python
con = sqlite3.connect(ruta)
try:
    with con:                 # transacción: commit al salir, rollback si falla
        con.execute("INSERT ...")
finally:
    con.close()               # C11: el cierre es SIEMPRE explícito
```

**Por qué importa (H-07 / la ley número uno).** Una conexión viva mantiene el
`.db` tomado; en Windows el próximo intento de reescribir el archivo revienta con
`PermissionError: [WinError 32]`. La casa ya lo sabía en su código
(`verificar.py`, `generar_fuentes.py`, `soluciones/`, `plantillas/`, SPEC-009);
solo la guía enseñaba la mentira. Ahora la guía dice lo que la casa sabe, y de
paso el patrón trampa se aprovecha como 💥 Rómpelo —el gesto insignia del
curso—: el alumno aprende **el error que parece correcto**, el más peligroso.

## Guardia de alcance (lo que NO se tocó)

- **Cero código:** `soluciones/`, `plantillas/`, `bin/`, `datos/` intactos — son
  la prueba de que el material se contradecía a sí mismo.
- Cifras de control (`✔ 12/12`, `9/9`), verificador y datasets intactos.
- Demos 1–3 de la Guía 4 (boleta sin timbre / commit / rollback) y la cápsula 🤖
  de ACID: conservadas.
- `troubleshooting.md` (ya curado por SPEC-012): no re-tocado.
- Otros labs: el barrido confirmó que el patrón prohibido **solo** vivía en el
  Lab 04. Sin trabajo extra.

## Hallazgos

**Sin hallazgos nuevos.** La corrección se aplicó acotada a §2–§4; el barrido T2
no descubrió el patrón prohibido fuera del Lab 04, y las ocurrencias restantes en
`bin/` y specs ya eran prohibiciones/explicaciones correctas. No se detectó otro
defecto in-repo.

## Veredicto final

**CERTIFICADO.**

Arreglos A (3 puntos), B y C aplicados dentro de su alcance; T1–T5 íntegros
(Lab 04 **12/12**, capstone **9/9**, verdad ejecutable confirmada en terminal,
coherencia y árbol limpios); código de los labs intacto. La guía dejó de enseñar
la mentira que su propio código ya desmentía. 🏛️🔌⚓

> **Tag:** sugerido `curso-v1.1.1` (patch — corrección de doc sin cambio de
> alcance). **No** crear sin confirmación del PO (§7).
