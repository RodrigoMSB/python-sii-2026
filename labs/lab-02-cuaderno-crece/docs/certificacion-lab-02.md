# Certificación del Lab 02 — El cuaderno crece

> Reporte de pruebas "mocito juega a ser alumno" (§11–§12 del SPEC-003).

## Datos de la corrida

| Ítem | Valor |
|------|-------|
| Fecha | 2026-07-02 |
| Máquina | macOS 26.5.1 (build 25F80), Apple Silicon |
| `uv` | 0.9.18 (0cee76417 2025-12-16) |
| Python resuelto por el lab | **3.13.7** (pineado `==3.13.*` vía `uv`) |
| Método | Clon limpio del repo en directorio temporal; comandos como alumno (sin activar venv a mano, siempre `uv run`) |
| Total de verificaciones del lab | **11** (N=11 → E01 muestra 10/11 con único error de interrogatorio) |

## Resultado por escenario

| Esc. | Veredicto | Evidencia breve |
|------|-----------|-----------------|
| **E01** Flujo feliz (Explorador) | ✅ CUMPLE | Preparador `✔ 5/5`, `.venv/` creado. `uv run python --version` → `Python 3.13.7`. Consolidar → `Fichas consolidadas      : 15`, `Registros rechazados     : 3`, `Deuda total consolidada  : $1,042,000 CLP`, informe en `salidas/`. Verificador sin RESPUESTAS → `✘ 10/11`, exit 1, único fallo el interrogatorio. Con las 5 respuestas → `✔ 11/11`, exit 0, mensaje de Don Arquímedes. |
| **E02** Artesano a medio camino | ✅ CUMPLE | Plantilla sin tocar → `✘ 3/11`, exit 1, con valor obtenido vs esperado en `normalizar_deuda`, `consolidar(oficial)` (fichas=17/rechazos=0), `deuda_por_rubro` y archivador sorpresa. Tras completar SOLO el TODO 1 → `normalizar_deuda` correcto y `normalizar_deuda('S/I')` lanza RegistroInvalido; el resto sigue fallando con pistas (consolidar aún revienta por falta del try/except → pista de TODO 4). |
| **E03** Tramposo (anti-loro) | ✅ CUMPLE | `consolidar`/`deuda_por_rubro` con valores oficiales hardcodeados. 3 corridas: el **archivador sorpresa** (distinto cada vez, con datos sucios y un duplicado) lo caza las 3 veces (fichero y rubros difieren de la referencia). `✘ 9/11`, exit 1 siempre. |
| **E04** Perdido (ubicación) | ✅ CUMPLE | Comando corregido (heredado de H-01/SPEC-002): `cp soluciones/consolidar.py guia/consolidar.py && cd guia && uv run python consolidar.py` → `ModuleNotFoundError: No module named 'datos'`, exit 1. Documentado en `docs/troubleshooting.md` con reproducción y cura; cura verificada (volver a la raíz → `Fichas consolidadas      : 15`). Limpieza `rm guia/consolidar.py` OK. |
| **E05** Rompe cosas | ✅ CUMPLE | Borrar `salidas/informe_consolidacion.txt` → `[ERROR] No existe...` + pista, exit 1; cura (reejecutar) → `✔ 11/11`. `SyntaxError` (quitar un `:`) → `[ERROR] consolidar.py falló al cargar: SyntaxError` + pista, **0 tracebacks crudos**, exit 1. **breakpoint() olvidado** → el verificador **NO se cuelga** (exit sin timeout), lo neutraliza (C8) y avisa. |
| **E06** Rezagado | ✅ CUMPLE | `recuperar_lab.py` → `✔ 3/3`: repone `consolidar.py`, regenera el informe y copia `RESPUESTAS.md` **sin responder** (5 marcadores). Verificador → `✘ 10/11` (solo falta el interrogatorio). |
| **E07** Idempotencia | ✅ CUMPLE | Preparador 3 veces seguidas → `✔ 5/5`, exit 0, sin errores ni duplicaciones. |
| **E08** Higiene del repo | ✅ CUMPLE | Clon "sucio" (`consolidar.py`, `RESPUESTAS.md`, `salidas/`, `.venv/`, `__pycache__/`) → `git status --porcelain` = 0 líneas. Se **amplió el `.gitignore`** con `labs/*/consolidar.py` (decisión: lista explícita por programa de lab, coherente con `labs/*/triaje.py`). |
| **E09** Regresión Lab 01 | ✅ CUMPLE | Sobre un clon con Lab 01: `recuperar_lab.py` + respuestas dummy + verificador → `✔ 12/12`, exit 0. Además, `git diff` de `labs/lab-01-primer-dia/` entre el tag `lab-01-v1.0.0` y HEAD = vacío: el Lab 01 no fue modificado por SPEC-003. |

## Hallazgos

**Sin hallazgos.** Los 9 escenarios cumplen íntegros a la primera. Notas menores
de construcción (no son desvíos):

- El verificador implementa **11** checks (se separó "informe existe" de "informe
  con deuda correcta" para dar mejor diagnóstico, igual que en el Lab 01). E01
  muestra 10/11 con único error de interrogatorio, consistente con el criterio
  "N-1/N" del spec.
- Blindaje **anti-breakpoint (C8)**: el verificador reemplaza `sys.breakpointhook`
  por un no-op antes de cargar el código del alumno, así un `breakpoint()` olvidado
  no cuelga el proceso (cross-platform, sin depender de señales) y se reporta.
- Decisión documentada del check de informe: se busca la deuda total en formato
  con separador de miles de Python (`1,042,000`) y, como respaldo, se normaliza
  quitando separadores.

## Veredicto final

**CERTIFICADO.**

Los 9 escenarios (E01–E09) se ejecutaron y cumplen íntegros, sin observaciones
abiertas. El Lab 02 es funcional y pedagógicamente completo, y el Lab 01 sigue
certificado (regresión E09 en verde).
