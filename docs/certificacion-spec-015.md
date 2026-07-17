# Certificación del SPEC-015 — Correcciones pedagógicas consolidadas

> Reporte de los 9 arreglos (A–I) surgidos de la revisión pedagógica completa de
> las 31 guías. **Solo documentación** (10 guías); cero código de labs tocado.
> Toda cifra publicada fue **ejecutada** antes (regla nacida del Arreglo B).

## Datos de la corrida

| Ítem | Valor |
|------|-------|
| Fecha | 2026-07-17 |
| Máquina | macOS 26.5.1 (build 25F80), Apple Silicon · `uv` 0.9.18 |
| Python de labs | 3.13 (gestionado por `uv`); verificación de snippets con `uv run` por lab |
| Regresión (T1) | Arnés oficial `pruebas/probar_curso.py` (7 unidades, copia temporal) |
| Alcance | Doc. **Cero** `soluciones/`, `plantillas/`, `bin/`, `datos/`, verificadores, capstone. |

## Archivos modificados (10 rutas)

| Arreglo | Archivo |
|---------|---------|
| **A** — Rómpelo Guía 3 (crea `salidas/`) | `lab-04-cuatro-fuentes/guia/03-json.md` |
| **B** — cifras `value_counts` (23→30) | `lab-05-gran-limpieza/guia/02-homogeneizacion.md` |
| **C** — enseñar keyword `global` | `lab-02-cuaderno-crece/guia/03-funciones.md` |
| **D.1** — cápsula 🤖 axis | `lab-03-numeros-del-puerto/guia/02-arrays.md` |
| **D.2 + F** — 🤖 broadcasting + nota `enumerate` | `lab-03-numeros-del-puerto/guia/03-vectorizacion.md` |
| **D.3** — cápsula 🤖 merge | `lab-06-transformar-combinar/guia/03-combinar.md` |
| **D.4** — cápsula 🤖 groupby/transform | `lab-06-transformar-combinar/guia/04-agregar-y-pivotear.md` |
| **E + G** — nota `.isdigit()` + comprensión de set | `lab-02-cuaderno-crece/guia/05-consolidacion.md` |
| **H** — `salidas/` en snippet matplotlib | `lab-06-transformar-combinar/guia/05-tablero.md` |
| **I** — paridad Mac/Windows (200 bytes) | `lab-04-cuatro-fuentes/guia/01-contexto.md` |

## Resultado por prueba

| Prueba | Veredicto | Evidencia |
|--------|-----------|-----------|
| **T1** Regresión completa (7 flujos) | ✅ CUMPLE | `probar_curso.py` → **`✔ 7/7`** (Lab 01–06 + capstone, todos CUMPLE). "Higiene: el repositorio quedó idéntico (git status sin cambios)" — el arnés trabaja en copia temporal; el código no se movió. |
| **T2** Arreglo A ejecutable | ✅ CUMPLE | Desde estado inicial (sin `salidas/`): `mkdir -p salidas && cp …` → **exit 0**, `salidas/multas_roto.json` creado (1072 bytes). El Rómpelo ya no choca por carpeta ausente. |
| **T3** Arreglo B exacto | ✅ CUMPLE | REPL sobre `censo_patentes.csv` con `.str.strip().str.upper()` → `VENCIDA 14 · VIGENTE 11 · SUSPENDIDA 5`, **total 30**. Coincide **literalmente** con las cifras nuevas, en ese orden. |
| **T4** Arreglo C ejecutable | ✅ CUMPLE | Ejemplo `global`: `acumular_global(1000)` → `1000`, `acumular_global(500)` → `1500`, `total` == `1500`. |
| **T5** E/F/G ejecutables | ✅ CUMPLE | **E:** `"200000".isdigit()` → `True`, `"200.000".isdigit()` → `False`. **F:** `enumerate` (estándar, sin cifra publicada nueva). **G:** `len([…])` → **18**, `len({…})` → **17** (verificado contra `datos/archivador.py`; idéntico al 18→17 de la Guía 1). Cero números de memoria. |
| **T6** Arreglo H | ✅ CUMPLE | Snippet matplotlib desde estado inicial (sin `salidas/`) → corre sin `FileNotFoundError`; `saldo_por_rubro.png` creado (28 KB). |
| **T7** Cobertura 🤖 | ✅ CUMPLE | Los **6** labs con `guia/` quedan ≥1: L01=3, L02=1, **L03=2** (era 0), L04=1, L05=1, **L06=2** (era 0). El capstone no tiene `guia/` (usa `escenario/pistas`) y está fuera de alcance (§10). Ningún lab-guía en 0. |
| **T8** Árbol limpio | ✅ CUMPLE | `git status --short` → **solo** las 10 rutas esperadas (A, B, C, D.1–4, E, F, G, H, I). Artefactos de verificación (`salidas/`) limpiados; cero colaterales. |

## Detalle de decisiones

**Arreglo B — la lección madre.** Las cifras 10/10/3 sumaban 23 sobre un censo de
**30 filas** y en orden incorrecto (`value_counts` ordena por frecuencia). Ahora
14/11/5, verificado en ejecución. De aquí nace la regla del DoD: **ninguna cifra
publicada sin ejecutar**.

**Arreglo C — ✔ del temario adjudicado.** La guía enseñaba scope pero nunca
mostraba `global` ("no escribe afuera salvo que se lo pidas explícitamente" — sin
mostrar cómo). Se insertó el ejemplo ejecutable + analogía de la pizarra del
pasillo + regla del curso (reconocerlo, no usarlo). El ✔ "scope y `global`" queda
cubierto sin recomendar la mala práctica.

**Arreglo I — paridad Mac/Windows (H-07 / ley número uno).** `head -c 200` (200
bytes) vs `Get-Content -TotalCount 1` (1 línea) no eran equivalentes: en un
binario sin saltos de línea, Windows volcaba mucho más. Reemplazado por
`[System.Text.Encoding]::ASCII.GetString([System.IO.File]::ReadAllBytes(...)[0..199])`
— los primeros 200 bytes, equivalente exacto a `head -c 200`. **No hay `pwsh` en
la máquina de certificación (macOS)**; correcto por construcción (lee bytes 0–199
y los decodifica); la confirmación física en PowerShell 5.1 queda para la
validación Windows real (SPEC-013).

## Hallazgos

**H-08 (resuelto en este spec) — el ejemplo del Arreglo G traía cifras y
estructura falsas.** El spec proponía mostrar
`[r["codigo"] for r in REGISTROS_BRUTOS][:3]` → `['PS-1001-C','PS-1002-G','PS-1002-G']`
para ilustrar "la lista puede repetir". Verificado contra `datos/archivador.py`:
los tres primeros códigos reales son **distintos** (`PS-1025-G`, `PS-1026-C`,
`PS-1027-T`) — el primer repetido (`PS-1026-C`) cae **más allá** del índice 3. El
`[:3]` no demostraba ningún repetido; publicar esas cifras habría reincidido en el
bug del Arreglo B. Siguiendo la instrucción del propio spec ("verifica… y corrige
las cifras si difieren; no publicar un número sin ejecutarlo"), se rindió la
lección con la demostración **verificada y honesta 18 → 17** (`len` de lista vs de
set), que además calza con el marco que la Guía 1 ya usa ("18 registros, 17
únicos"). La promesa de la Guía 1 queda cumplida. El disparador H-01 (ACTUAL que
no calza con el repo) **no** se activó: todos los textos ACTUAL coincidieron
exactos; la corrección quedó dentro de la latitud que el §7 delega al mocito.

Sin otros hallazgos: el barrido no encontró más cifras erróneas ni promesas
colgando fuera de lo previsto.

## Veredicto final

**CERTIFICADO.**

Los 9 arreglos (A–I) aplicados dentro de su alcance; T1–T8 íntegros (7/7 en
regresión, toda cifra ejecutada, cobertura 🤖 completa, árbol limpio); código de
los labs intacto (metas `5/5`, `11/11`, `9/9`, `9/9`, `9/9`, `14/14`, `9/9`
preservadas). Dos tablas sueltas enderezadas, una promesa cumplida y tres métodos
(`.isdigit`, `enumerate`, comprensión de set) ahora se explican antes de usarse.

> **Tag:** sugerido `curso-v1.2.0` (minor — agrega contenido: `global`, cápsulas
> 🤖, comprensión de set). **No** crear sin confirmación del PO (§12).
