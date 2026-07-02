# Certificación del Lab 06 — Transformar y combinar

> Reporte de pruebas "mocito juega a ser alumno" (§12–§14 del SPEC-007).

## Datos de la corrida

| Ítem | Valor |
|------|-------|
| Fecha | 2026-07-02 |
| Máquina | macOS 26.5.1 (build 25F80), Apple Silicon |
| `uv` | 0.9.18 |
| Python resuelto | **3.13.7** (`==3.13.*`) |
| Bibliotecas | numpy 2.5.0 · pandas 3.0.3 · openpyxl 3.1.5 · **matplotlib 3.11.0** |
| Método | Clon limpio en directorio temporal; comandos como alumno (siempre `uv run`) |
| Verificaciones del lab | **14** (E01 → 13/14 con único error de interrogatorio) |

## Resultado por escenario

| Esc. | Veredicto | Evidencia breve |
|------|-----------|-----------------|
| **E01** Flujo feliz (Explorador) | ✅ CUMPLE | Preparador `✔ 11/11` (incluye matplotlib 3.11.0 y los 3 CSV con 25/12/8 filas). Solución → informe con `Saldo pendiente $2,025,000`, `9` sin pago, `Total huérfano $130,500`. `salidas/` con informe, `tablero.csv/xlsx` y `saldo_por_rubro.png` (28.213 bytes, firma `\x89PNG`). Verificador sin RESPUESTAS → `✘ 13/14`. Con respuestas → `✔ 14/14`, exit 0, cierre "El Concejo vota con los ojos". |
| **E02** Artesano a medio camino | ✅ CUMPLE | Plantilla → `✘ 6/14` (crosstab/pivote/dummies pasan por estar implementados; rubro/tramo/concat/merge/pct fallan con obtenido vs esperado). Tras completar SOLO el TODO 1 → `agregar_rubro` correcto {G:11, C:8, T:6}; el resto sigue fallando con pistas. |
| **E03** Tramposo (anti-loro) | ✅ CUMPLE | `construir_tablero` hardcodeado para devolver el tablero oficial ignorando la entrada. 3 corridas: los **datasets sorpresa** (mini-censo + pagos con huérfano en tempdir) lo cazan las 3 veces. `✘ 12/14`, exit 1 siempre. |
| **E04** Perdido (ubicación) | ✅ CUMPLE | `cp soluciones/tablero.py guia/ && cd guia && uv run python tablero.py` → `FileNotFoundError: ... guia/datos/censo_limpio.csv`. Cura verificada (raíz → `$2,025,000`). Documentado en troubleshooting. |
| **E05** Rompe cosas | ✅ CUMPLE | Borrar `saldo_por_rubro.png` → `✘ 13/14` "png ausente"; cura (reejecutar) → `✔ 14/14`. `SyntaxError` → `[ERROR]` de carga, 0 tracebacks. `breakpoint()` → **no cuelga**, neutralizado (C8). **`plt.show()` inyectado:** con Agg **NO cuelga** (exit sin timeout) y el informe se genera igual — la solución oficial (Agg) es inmune (C16). Alterar un CSV → entorno detecta `19 filas (deberían ser 25)`; `git checkout` → `✔ 11/11`. |
| **E06** Rezagado | ✅ CUMPLE | Alteré `pagos_junio.csv`; `recuperar_lab.py` → `✔ 4/4`: **restaura los 3 CSV con git checkout** (vuelve a 12 filas), repone `tablero.py`, regenera salidas (incluido el PNG) y copia `RESPUESTAS.md` sin responder. Verificador → `✘ 13/14`. |
| **E07** Idempotencia | ✅ CUMPLE | Preparador 2ª/3ª vez → `✔ 11/11`, **0 descargas**. Pipeline ×2 → `tablero.csv` idéntico; PNG existe y con tamaño estable (28.213 bytes) las dos veces. |
| **E08** Higiene del repo | ✅ CUMPLE | Clon "sucio" tras E06 → `git status --porcelain` = 0 líneas. `labs/*/tablero.py` y `salidas/` (incluido el PNG) ignorados; los 3 CSV versionados permanecen intactos (restaurados por git en el recuperador). |
| **E09** Regresión (Labs 01–05) | ✅ CUMPLE | Lab 01 `✔ 12/12`, Lab 02 `✔ 11/11`, Lab 03 `✔ 13/13`, Lab 04 `✔ 12/12`, Lab 05 `✔ 14/14`. `git diff` de los cinco labs entre `lab-05-v1.0.0` y HEAD = vacío: intactos. |

## Hallazgos

**Sin hallazgos.** Los 9 escenarios cumplen íntegros a la primera. Todas las cifras
de control coinciden con pandas real (rubros 11/8/6, tramos 4/11/7/3, concat
20/$1.213.000, saldo $2.025.000, huérfanos {PS-1032-C, PS-1040-G}=$130.500, saldo
por rubro 601k/99k/1325k, Buceo 34,0 %, crosstab y pivot). matplotlib 3.11.0 no está
yanked (doctrina H-03) y funciona headless con Agg (C16). Notas de construcción (no
son desvíos): el verificador valida el gráfico por el PNG que deja el propio
`tablero.py` (existencia, tamaño > 5 KB y firma `\x89PNG`), sin llamar a matplotlib
él mismo.

## Veredicto final

**CERTIFICADO.**

Los 9 escenarios (E01–E09) cumplen íntegros y los Labs 01–05 siguen certificados.
Sin deviación de la spec (todas las cifras exactas, sin dato duro alterado), sin
observaciones que bloqueen el tag `lab-06-v1.0.0`. Con esto se cierra el **Módulo 3**
y quedan construidos los 6 laboratorios regulares del curso.
