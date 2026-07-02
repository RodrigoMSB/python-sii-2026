# Certificación del Lab 01 — El primer día en Rentas

> Reporte de pruebas "mocito juega a ser alumno" (§11–§12 del SPEC-002).

## Datos de la corrida

| Ítem | Valor |
|------|-------|
| Fecha | 2026-07-02 |
| Máquina | macOS 26.5.1 (build 25F80), Apple Silicon |
| `uv` | 0.9.18 (0cee76417 2025-12-16) |
| Python resuelto por el lab | **3.13.7** (pineado `==3.13.*` vía `uv`) |
| Método | Clon limpio del repo en directorio temporal; comandos como alumno (sin activar venv a mano, siempre `uv run`) |

## Resultado por escenario

| Esc. | Veredicto | Evidencia breve |
|------|-----------|-----------------|
| **E01** Flujo feliz (Explorador) | ✅ CUMPLE | Preparador `✔ 5/5`, `.venv/` creado. `uv run python --version` → `Python 3.13.7`. Triaje → `Patentes vigentes    : 13`, `Deuda total          : $2350000 CLP`, `salidas/informe_triaje.txt` creado. Verificador sin RESPUESTAS → `✘ 11/12`, exit 1, único fallo el interrogatorio. Con las 5 respuestas → `✔ 12/12`, exit 0, mensaje de Don Arquímedes. |
| **E02** Artesano a medio camino | ✅ CUMPLE | Plantilla sin tocar → `✘ 3/12`, exit 1, los 3 cálculos con valor obtenido vs esperado (`contar_vigentes: obtuvo 0, se esperaba 13`, etc.). Tras completar SOLO el TODO 1 a mano → `contar_vigentes` pasa (oficial y sorpresa); `codigos_vencidas` y `deuda_total` siguen fallando con pistas. |
| **E03** Tramposo (anti-loro) | ✅ CUMPLE | `triaje.py` con las 3 funciones devolviendo los valores oficiales hardcodeados. 3 corridas: en las 3, los 3 checks del cuaderno oficial pasan pero los 3 del **cuaderno sorpresa** fallan (dataset aleatorio distinto cada vez). `✘ 8/12`, exit 1 siempre. |
| **E04** Perdido (ubicación) | ⚠️ CUMPLE con observación | Ver **Hallazgo H-01**. El comando **literal** del spec (`uv run python ../triaje.py` desde `guia/`) **no** reproduce el error: Python pone el directorio del script (la raíz) en `sys.path` y `datos` sí se encuentra. La **intención** del escenario sí se cumple: la reproducción real (tener/ejecutar `triaje.py` dentro de `guia/`) da `ModuleNotFoundError: No module named 'datos'`, está documentada en `docs/troubleshooting.md` con síntoma y cura, y la cura verificada funciona (volver a la raíz → `13` vigentes). |
| **E05** Rompe cosas | ✅ CUMPLE | Borrar `salidas/informe_triaje.txt` → `[ERROR] No existe salidas/informe_triaje.txt` + pista de re-ejecutar, exit 1; aplicar cura → `✔ 12/12`. Introducir `SyntaxError` (quitar un `:`) → `[ERROR] triaje.py falló al cargar: SyntaxError: expected ':'` + pista, exit 1; **0 tracebacks crudos** (el verificador no explota). |
| **E06** Rezagado | ✅ CUMPLE | `recuperar_lab.py` → `✔ 3/3`: repone `triaje.py`, regenera `salidas/informe_triaje.txt` y copia `RESPUESTAS.md` **sin responder** (5 marcadores). Verificador → `✘ 11/12` (solo falta el interrogatorio). La comprensión no se regala. |
| **E07** Idempotencia | ✅ CUMPLE | Preparador 2ª y 3ª vez seguidas → `✔ 5/5`, exit 0, sin errores ni duplicaciones. Bonus: `recuperar_lab.py` respeta un `RESPUESTAS.md` ya empezado (`lo respeto, no lo piso`). |
| **E08** Higiene del repo | ✅ CUMPLE | Con el clon "sucio" (`triaje.py`, `RESPUESTAS.md`, `salidas/`, `.venv/`, `__pycache__/` presentes) → `git status` = *"nothing to commit, working tree clean"*. El `.gitignore` con patrones de ruta hace su pega. |

## Hallazgos

### H-01 — El comando literal de E04 no reproduce `No module named 'datos'` *(no bloqueante; requiere ratificación del Arquitecto)*

- **Síntoma:** el paso literal del spec —`cd guia && uv run python ../triaje.py`—
  **no falla**: imprime el informe normal (`Patentes vigentes    : 13`).
- **Causa (comprobada):** al ejecutar `python ../triaje.py`, Python coloca en
  `sys.path[0]` el **directorio del script** (que resuelve a la **raíz del lab**),
  no el directorio de trabajo actual. Por eso `from datos.cuaderno import PATENTES`
  encuentra `datos/` sin importar desde qué carpeta se invoque. El error
  `No module named 'datos'` sólo aparece cuando el **propio `triaje.py` está
  ubicado** en la carpeta equivocada (p. ej. una copia en `guia/`), caso en que
  `sys.path[0]` es `guia/` y ahí no hay `datos/`.
- **Cómo se resolvió sin romper contratos:** NO se alteró el código del lab (los
  contratos §6 y el import de §8.1 se mantienen intactos). `docs/troubleshooting.md`
  documenta el síntoma con su **reproducción real** (triaje ubicado en `guia/`) y
  la cura (ejecutar el triaje de la raíz, parado en la raíz), ambas verificadas.
- **Propuesta de fix del spec (para el Arquitecto):** cambiar el paso de E04 de
  `uv run python ../triaje.py` a algo que sí reproduzca el síntoma, p. ej.:
  `cp soluciones/triaje.py guia/triaje.py && cd guia && uv run python triaje.py`.
  Es un ajuste del **guion de pruebas**, no del laboratorio.

### H-02 — (Corregido durante la construcción) El encabezado de `RESPUESTAS.md` contenía el marcador literal

- Durante E01 se detectó que el texto de instrucciones del interrogatorio incluía
  la cadena exacta `(escribe aquí tu respuesta)`, por lo que el verificador contaba
  **6** marcadores en vez de 5 y el alumno jamás habría llegado a `12/12`.
- **Corregido** antes de la certificación: el encabezado ahora describe el marcador
  con guillemets («escribe aquí tu respuesta») sin reproducir la cadena contable.
  Verificado: la plantilla tiene exactamente **5** marcadores y E01 cierra en `12/12`.

## Veredicto final

**CERTIFICADO CON OBSERVACIÓN.**

Los 8 escenarios se ejecutaron; 7 cumplen íntegros y E04 cumple en intención
(síntoma real reproducible, documentado y con cura funcional), con la salvedad de
que el **comando literal** de E04 no dispara el error por semántica de `sys.path`
de Python. El laboratorio es funcional y pedagógicamente completo; el único punto
abierto (H-01) es un ajuste del **guion de pruebas** del spec, no del lab, y queda
a ratificación del Arquitecto.
