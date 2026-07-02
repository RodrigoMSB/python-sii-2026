# Certificación del Lab 04 — Las cuatro fuentes

> Reporte de pruebas "mocito juega a ser alumno" (§12–§14 del SPEC-005).

## Datos de la corrida

| Ítem | Valor |
|------|-------|
| Fecha | 2026-07-02 |
| Máquina | macOS 26.5.1 (build 25F80), Apple Silicon |
| `uv` | 0.9.18 |
| Python resuelto | **3.13.7** (`==3.13.*`) |
| Bibliotecas | numpy 2.5.0 · pandas 3.0.3 · **openpyxl 3.1.5** (+ sqlite3 stdlib) |
| Método | Clon limpio en directorio temporal; comandos como alumno (siempre `uv run`) |
| Verificaciones del lab | **12** (E01 → 11/12 con único error de interrogatorio) |

## Resultado por escenario

| Esc. | Veredicto | Evidencia breve |
|------|-----------|-----------------|
| **E01** Flujo feliz (Explorador) | ✅ CUMPLE | Preparador descarga openpyxl → `✔ 9/9` (incluye las 4 fuentes, que vienen versionadas). Solución → informe con `TOTAL ... $2,072,500 CLP`, `Pago válido: ACEPTADO (commit)`, `Pago inválido: RECHAZADO (rollback)`. `salidas/` con los 4 exportados (`resumen.csv/.xlsx/.json`, `gestion.db`) + `registro.db`. Verificador sin RESPUESTAS → `✘ 11/12`. Con respuestas → `✔ 12/12`, exit 0, cierre de Don Arquímedes. |
| **E02** Artesano a medio camino | ✅ CUMPLE | Plantilla → `✘ 4/12` con obtenido vs esperado; `cargar_contribuyentes` pasa (no es TODO). Tras completar SOLO el TODO 1 → `cargar_pagos [oficial]` correcto; el resto (permisos, multas, resumen, sorpresa, transacción) sigue fallando con pistas. |
| **E03** Tramposo (anti-loro) | ✅ CUMPLE | Retornos oficiales hardcodeados. 3 corridas: las **fuentes sorpresa** (archivos aleatorios en tempdir) y el **check transaccional** lo cazan las 3 veces. `✘ 8/12`, exit 1 siempre. |
| **E04** Perdido (ubicación) | ✅ CUMPLE | `cp soluciones/fuentes.py guia/ && cd guia && uv run python fuentes.py` → `FileNotFoundError: ... guia/datos/fuentes/pagos.csv` (error de RUTA, porque `fuentes.py` lee por ruta relativa al script; no importa `datos` como módulo). Cura verificada (raíz → `$2,072,500`). Troubleshooting corregido a FileNotFoundError. |
| **E05** Rompe cosas | ✅ CUMPLE | Borrar `multas.json` → entorno reporta `Faltan fuentes: multas.json` + pista del generador (0 tracebacks); regenerar → `✔ 9/9`. Corromper JSON (coma colgante) → `cargar_multas` → `JSONDecodeError: Illegal trailing comma ... line 5`. `SyntaxError` → `[ERROR]` de carga, 0 tracebacks. `breakpoint()` en función llamada → **no cuelga**, neutralizado (C8). **Transaccional ×2:** ejecutar `fuentes.py` dos veces → `pagos_registrados` = 1 y 1 (main recrea la copia de trabajo cada corrida; sin duplicación descontrolada). |
| **E06** Rezagado | ✅ CUMPLE | `recuperar_lab.py` → `✔ 4/4` (regenera fuentes faltantes, repone `fuentes.py`, regenera salidas, copia `RESPUESTAS.md` sin responder). Verificador → `✘ 11/12`. El `.xlsx` presente NO se reescribe (ver H-04) → git limpio. |
| **E07** Idempotencia | ✅ CUMPLE | Preparador 2ª/3ª vez → `✔ 9/9`, **0 descargas**. Generador ×2 (solo-faltantes): no-op → las 4 fuentes idénticas (nada se reescribe). |
| **E08** Higiene del repo | ✅ CUMPLE | Clon "sucio" tras E05/E06/E07 (`fuentes.py`, `RESPUESTAS.md`, `salidas/`, `.venv/`, `__pycache__/`) → `git status --porcelain` = 0 líneas. `datos/fuentes/` versionado permanece intacto (gracias a H-04). |
| **E09** Regresión (Labs 01/02/03) | ✅ CUMPLE | Lab 01 → `✔ 12/12`; Lab 02 → `✔ 11/11`; Lab 03 → `✔ 13/13`. `git diff` de los tres labs entre `lab-03-v1.0.0` y HEAD = vacío: intactos. |

## Hallazgos

### H-04 — El `.xlsx` de openpyxl no es byte-determinista *(resuelto por diseño; deviación de §5.5 a ratificar)*

- **Síntoma:** `generar_fuentes.py`, tal como pide §5.5 ("idempotente, **borra y
  crea** todo desde cero"), regenera el `permisos_eventos.xlsx` con bytes
  **distintos** cada vez, porque openpyxl incrusta una marca de tiempo en el
  archivo (probado: fijar propiedades del workbook y timestamps del zip **no**
  basta). El `.csv`, `.json` y `.db` sí son deterministas.
- **Impacto:** como `datos/fuentes/` se versiona (§3) y el recuperador regenera
  (§8.3), cualquier regeneración del xlsx dejaba el repo **sucio** → E07/E08
  fallaban tras E06.
- **Contradicción de spec:** §5.5 ("borra y crea todo") choca con §12-E08 ("git
  limpio"). El propio §12-E07 ya anticipaba que "xlsx/db pueden variar en
  metadatos — documentar qué se compara", señal de que la variación era conocida.
- **Decisión del ejecutor (a ratificar):** `generar_fuentes.py` ahora regenera
  **solo las fuentes que faltan** por defecto (con `--force` para reconstruir
  todo). Así, con las cuatro presentes es un no-op y NO reescribe el xlsx →
  `datos/fuentes/` versionado se mantiene intacto y E07/E08 pasan. El recuperador
  lo invoca sin `--force`. No se tocó ningún contrato (C1–C12), cifra de control
  (§5) ni nombre. Documentado en el docstring del generador y en el README.
- **Fix de spec propuesto:** ajustar §5.5 para decir "regenera **lo que falte**
  por defecto (`--force` reconstruye todo)", coherente con la nota de §12-E07.

## Veredicto final

**CERTIFICADO CON OBSERVACIÓN (H-04).**

Los 9 escenarios (E01–E09) cumplen íntegros y los Labs 01–03 siguen certificados.
La única observación es H-04: el cambio del generador de "borra y crea" (§5.5) a
"regenera solo lo que falta", necesario porque el `.xlsx` no es reproducible byte
a byte y §5.5 chocaba con E08. No altera contratos, cifras ni nombres, y el propio
§12-E07 anticipaba la variación de binarios. Queda a ratificación del Arquitecto/PO
antes de crear el tag `lab-04-v1.0.0`; con la ratificación se enmienda §5.5 (v1.1)
y se libera el tag.
