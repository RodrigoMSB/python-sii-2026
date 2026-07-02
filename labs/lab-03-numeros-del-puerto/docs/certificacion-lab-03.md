# Certificación del Lab 03 — Los números del puerto

> Reporte de pruebas "mocito juega a ser alumno" (§12–§14 del SPEC-004).

## Datos de la corrida

| Ítem | Valor |
|------|-------|
| Fecha | 2026-07-02 |
| Máquina | macOS 26.5.1 (build 25F80), Apple Silicon |
| `uv` | 0.9.18 |
| Python resuelto | **3.13.7** (`==3.13.*`) |
| Bibliotecas | **numpy 2.5.0** · **pandas 3.0.3** (ver Hallazgo H-03) |
| Método | Clon limpio en directorio temporal; comandos como alumno (siempre `uv run`) |
| Verificaciones del lab | **13** (E01 → 12/13 con único error de interrogatorio) |

## Resultado por escenario

| Esc. | Veredicto | Evidencia breve |
|------|-----------|-----------------|
| **E01** Flujo feliz (Explorador) | ✅ CUMPLE | Preparador descarga numpy/pandas la 1ª vez → `✔ 7/7` (incluye `numpy 2.5.0`, `pandas 3.0.3`). `Python 3.13.7`. Informe con `$90,680,000`, `Mes récord ... Diciembre ($9,140,000)`, `Junio, Julio`, `Patentes vencidas: 8`, `Deuda vencida ... $976,000`. Verificador sin RESPUESTAS → `✘ 12/13` (solo interrogatorio). Con respuestas → `✔ 13/13`, exit 0, cierre de Don Arquímedes. |
| **E02** Artesano a medio camino | ✅ CUMPLE | Plantilla intacta → errores con obtenido vs esperado en por-mes/por-rubro/agregaciones/sorpresa/resumen. Tras completar SOLO el TODO 1 → `recaudacion_por_mes [oficial]` correcto; el resto sigue fallando con pistas. |
| **E03** Tramposo (anti-loro) | ✅ CUMPLE | Retornos oficiales hardcodeados (incluidos los arrays). 3 corridas: la **matriz sorpresa** y el **cuaderno sorpresa** (aleatorios) lo cazan las 3 veces. `✘ 10/13`, exit 1 siempre. |
| **E04** Perdido (ubicación) | ✅ CUMPLE | `cp soluciones/panorama.py guia/ && cd guia && uv run python panorama.py` → `ModuleNotFoundError: No module named 'datos'`, exit 1; cura verificada (volver a la raíz → `$90,680,000`). Documentado en troubleshooting. |
| **E05** Rompe cosas | ✅ CUMPLE | Borrar informe → `✘ 11/13` + pista, cura → `✔ 13/13`. `SyntaxError` → `[ERROR]` de carga, **0 tracebacks crudos**. `breakpoint()` en función que el verificador llama → **no se cuelga** (exit sin timeout), neutralizado y avisado (C8). **Biblioteca rota:** `verificar_entorno.py` sin numpy → `[ERROR] No pude importar numpy` + pista del preparador, **0 tracebacks**; re-preparar → `✔ 7/7`. (Ver nota E05 abajo.) |
| **E06** Rezagado | ✅ CUMPLE | `recuperar_lab.py` → `✔ 3/3`: repone `panorama.py`, regenera el informe, copia `RESPUESTAS.md` sin responder (5 marcadores). Verificador → `✘ 12/13` (solo interrogatorio). |
| **E07** Idempotencia | ✅ CUMPLE | Preparador 2ª y 3ª vez → `✔ 7/7`, **0 descargas** (numpy/pandas ya cacheados). |
| **E08** Higiene del repo | ✅ CUMPLE | Clon "sucio" (`panorama.py`, `RESPUESTAS.md`, `salidas/`, `.venv/`, `__pycache__/`) → `git status --porcelain` = 0 líneas. `.gitignore` ampliado con `labs/*/panorama.py` (lista explícita por programa, coherente con labs previos). |
| **E09** Regresión (Labs 01 y 02) | ✅ CUMPLE | Lab 01 → `✔ 12/12`; Lab 02 → `✔ 11/11`. `git diff` de ambos labs entre `lab-02-v1.0.0` y HEAD = vacío: intactos. |

### Nota E05 (biblioteca rota)
El comando literal del spec (`borrar .venv` + `uv run python -c "import numpy"`)
**se autocura**: `uv run` re-sincroniza el entorno antes de ejecutar, así que numpy
se reinstala y se importa OK. La conducta protectora que importa —que
`verificar_entorno.py` reporte con elegancia cuando numpy/pandas falten, sin
traceback— se verificó por la vía directa (`uv run --no-sync` sin numpy): reporta
`[ERROR]` con pista del preparador. La protección funciona; el comando literal
simplemente no llega a romper nada porque uv lo repara solo.

## Hallazgos

### H-03 — `pandas==3.0.4` (dato duro del spec) está YANKED en PyPI *(ABIERTO — requiere ratificación del Arquitecto)*

- **Síntoma:** al fijar `pandas==3.0.4` (§2/§0 del SPEC-004, "verificada contra
  PyPI"), `uv sync` advierte:
  `warning: pandas==3.0.4 is yanked (reason: "Reported segfaults with datetime-related functionality")`.
- **Impacto:** la 3.0.4 aún instala, y el lab **funciona idéntico** (no usa
  datetime; se verificó DataFrame, `str` dtype, filtrado, `value_counts`, `iloc`,
  `describe`). Pero cada alumno vería ese warning alarmante en su primer `uv sync`,
  y publicar una dependencia retirada en un "v1.0.0" contradice la meta de
  reproducibilidad/profesionalismo del propio spec.
- **Decisión del ejecutor (a ratificar):** se fijó **`pandas==3.0.3`** — la última
  3.0.x **no yanked** disponible (3.0.5/3.0.6/3.1.0 aún no existen; 3.0.2 también
  limpia). Misma API moderna (str dtype por defecto, CoW), verificada con todas las
  cifras de control. `numpy==2.5.0` se mantiene. Documentado en `pyproject.toml`,
  `uv.lock`, `verificar_entorno.py` (chequea 3.0.3), README y troubleshooting, y en
  la nota de ejecutor al inicio de `specs/SPEC-004.md`.
- **Por qué se procedió sin ratificación previa:** construir sobre la 3.0.4 yanked
  habría exigido rehacer pyproject/uv.lock igual al ratificar el cambio; el PO no
  respondió en el momento y la opción de menor riesgo era la 3.0.3. Se deja el
  **tag `lab-03-v1.0.0` SIN crear** hasta la ratificación (protocolo H-01).

## Veredicto final

**CERTIFICADO CON OBSERVACIÓN (H-03).**

Los 9 escenarios (E01–E09) cumplen íntegros y los Labs 01–02 siguen certificados.
La única observación abierta es H-03: la sustitución del pin `pandas==3.0.4`
(yanked) por `3.0.3`, que cambia un "dato duro" del spec y por eso queda a
ratificación del Arquitecto/PO antes de crear el tag `lab-03-v1.0.0`. Con la
ratificación, se enmienda el spec (v1.1) y se libera el tag.
