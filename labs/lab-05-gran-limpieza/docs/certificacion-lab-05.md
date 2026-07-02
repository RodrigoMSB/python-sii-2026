# Certificación del Lab 05 — La gran limpieza

> Reporte de pruebas "mocito juega a ser alumno" (§12–§14 del SPEC-006).

## Datos de la corrida

| Ítem | Valor |
|------|-------|
| Fecha | 2026-07-02 |
| Máquina | macOS 26.5.1 (build 25F80), Apple Silicon |
| `uv` | 0.9.18 |
| Python resuelto | **3.13.7** (`==3.13.*`) |
| Bibliotecas | numpy 2.5.0 · pandas 3.0.3 · openpyxl 3.1.5 |
| Método | Clon limpio en directorio temporal; comandos como alumno (siempre `uv run`) |
| Verificaciones del lab | **14** (E01 → 13/14 con único error de interrogatorio) |

## Resultado por escenario

| Esc. | Veredicto | Evidencia breve |
|------|-----------|-----------------|
| **E01** Flujo feliz (Explorador) | ✅ CUMPLE | Preparador `✔ 8/8`, **0 descargas** (deps del Lab 04 en caché). Solución → informe con embudo `30 → 28 → 26 → 25`, veredictos (PS-1022-T CONSERVADO, PS-1046-C APARTADO) y `Deuda total : $3,107,500 CLP`. `salidas/` con informe + `censo_limpio.csv/.xlsx` (25 filas). Verificador sin RESPUESTAS → `✘ 13/14`. Con respuestas → `✔ 14/14`, exit 0, cierre de Don Arquímedes. |
| **E02** Artesano a medio camino | ✅ CUMPLE | Plantilla → `✘ 5/14` con obtenido vs esperado (homogeneizar muestra las 10 variantes, quitar_duplicados (30,0), etc.). Tras completar SOLO el TODO 1 → `homogeneizar` correcto; el resto sigue fallando con pistas. |
| **E03** Tramposo (anti-loro) | ✅ CUMPLE | Reporte y retornos oficiales hardcodeados. 3 corridas: el **censo sorpresa** (mugre aleatoria en tempdir) lo caza las 3 veces (el reporte difiere de la referencia). `✘ 11/14`, exit 1 siempre. |
| **E04** Perdido (ubicación) | ✅ CUMPLE | `cp soluciones/limpiar.py guia/ && cd guia && uv run python limpiar.py` → `FileNotFoundError: ... guia/datos/censo_patentes.csv` (error de ruta; limpiar.py lee el censo relativo al script). Cura verificada (raíz → `$3,107,500`). Documentado en troubleshooting. |
| **E05** Rompe cosas | ✅ CUMPLE | Borrar una fila del censo → entorno reporta `El censo tiene 29 filas (deberían ser 30)` + pista `git checkout`; restaurar → `✔ 8/8`. `SyntaxError` → `[ERROR]` de carga, 0 tracebacks. `breakpoint()` en función llamada → **no cuelga**, neutralizado (C8). **Marcador de faltante desconocido:** ver Hallazgo H-05 — con un marcador realmente desconocido (p. ej. `s/d`) la columna `deuda` queda como texto (síntoma), y la cura es agregarlo a `na_values`. |
| **E06** Rezagado | ✅ CUMPLE | Rompí el censo (a 24 filas); `recuperar_lab.py` → `✔ 4/4`: **restaura el censo con git checkout** (vuelve a 30 filas), repone `limpiar.py`, regenera salidas y copia `RESPUESTAS.md` sin responder. Verificador → `✘ 13/14`. |
| **E07** Idempotencia | ✅ CUMPLE | Preparador 2ª/3ª vez → `✔ 8/8`. Pipeline ×2 → `censo_limpio.csv` byte-idéntico (CSV determinista). |
| **E08** Higiene del repo | ✅ CUMPLE | Clon "sucio" tras E06 → `git status --porcelain` = 0 líneas. `labs/*/limpiar.py` y `salidas/` ignorados; `datos/censo_patentes.csv` versionado permanece intacto (restaurado por git en el recuperador). |
| **E09** Regresión (Labs 01–04) | ✅ CUMPLE | Lab 01 `✔ 12/12`, Lab 02 `✔ 11/11`, Lab 03 `✔ 13/13`, Lab 04 `✔ 12/12`. `git diff` de los cuatro labs entre `lab-04-v1.0.0` y HEAD = vacío: intactos. |

## Hallazgos

### H-05 — El ejemplo "N/A" de E05 es un marcador NA por defecto de pandas *(menor, no bloqueante; recomendación para el spec)*

- **Observación:** el escenario E05 propone agregar una 4ª variante de faltante
  **`"N/A"`** para demostrar que el pipeline "no la conoce". Pero `"N/A"` está en la
  **lista de marcadores NA por defecto de pandas** (junto con `NA`, `NaN`, `null`,
  etc.), y como la solución usa `keep_default_na=True`, pandas **la detecta sola**:
  el síntoma (deuda como texto) **no** se reproduce con `"N/A"`.
- **Cómo se cubrió la intención:** el síntoma sí se reproduce con un marcador
  **genuinamente desconocido** (p. ej. `s/d`, `pendiente`): ahí `deuda` queda como
  `str` y la cura es agregarlo a `na_values`. Se validó ambos caminos. El
  `docs/troubleshooting.md` ya documenta el caso "deuda quedó como texto → na_values".
- **Recomendación (para el Arquitecto):** en E05, cambiar el ejemplo `"N/A"` por un
  marcador que no esté en la lista NA por defecto (`s/d`, `pendiente`, `s/i`
  minúscula, etc.) para que el escenario reproduzca el síntoma como se pretende.
  Es un ajuste del **guion de pruebas**, no del laboratorio.

## Veredicto final

**CERTIFICADO.**

Los 9 escenarios (E01–E09) cumplen íntegros y los Labs 01–04 siguen certificados.
Todas las cifras de control coinciden con pandas real (30→28→26→25, $3.107.500,
IQR {PS-1022-T, PS-1046-C}, z {PS-1046-C}). El único hallazgo (H-05) es una mejora
menor al **ejemplo** de un escenario de prueba, no altera contratos, cifras ni
código del lab, y su intención quedó demostrada. Sin observaciones que bloqueen el
tag `lab-05-v1.0.0`.
