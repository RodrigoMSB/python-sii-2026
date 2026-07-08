# Certificación del SPEC-012 — Correcciones in-repo (paridad Windows)

> Reporte de las tres correcciones in-repo (cura sqlite, comando capstone, política
> de uv) detectadas en las auditorías SPEC-010 / SPEC-011.

## Datos de la corrida

| Ítem | Valor |
|------|-------|
| Fecha | 2026-07-07 (push/CI 2026-07-08 UTC) |
| Máquina (local, T1/T3/T4) | macOS 26.5.1 (build 25F80), Apple Silicon · `uv` 0.9.18 |
| CI (T2) | GitHub Actions — `windows-2025-vs2026` (Server 2025, pwsh 7) + `macos-latest` |
| uv en CI | **0.11.26 pineado** (antes "latest" por fallback) |
| Python resuelto | **3.13** (gestionado por `uv`) |
| Método | Cambios acotados a 4 rutas; regresión con el arnés oficial en copia temporal |
| Alcance | Doc + workflow + una línea de doc. **Cero código de labs tocado.** |

## Archivos modificados (4 rutas, sin colaterales)

| Arreglo | Archivo | Commit |
|---------|---------|--------|
| A — cura sqlite | `labs/lab-04-cuatro-fuentes/docs/troubleshooting.md` | `aa1f72e` |
| B — comando capstone | `labs/capstone-el-arenario/README.md` | `0630e9e` |
| C — política uv | `.github/workflows/pruebas-curso.yml` + `docs/setup-alumno.md` | `4c47a1e` |

## Resultado por prueba

| Prueba | Veredicto | Evidencia breve |
|--------|-----------|-----------------|
| **T1** Regresión del código intacto | ✅ CUMPLE | Arnés oficial (`probar_lab.py`) en copia temporal: **Lab 04 → flujo del alumno en verde** (18s) y **Capstone → en verde** (23s). El arnés reproduce `recuperar → anti-adorno (verificador exit 1 sin interrogatorio) → rellenar interrogatorio → verificar`, y solo reporta verde en el pase canónico completo (Lab 04 **12/12**, capstone **9/9**). El arreglo A (doc) no rozó el código. |
| **T2** CI verde con uv pineado | ✅ CUMPLE | Run `28913435537` (push a `main`). Windows job `85775373224`: `version: 0.11.26` → "Successfully installed uv version 0.11.26" (sin "Falling back to latest"). **Los 7** → CUMPLE en Windows; ambos jobs verdes (Windows 3m38s, macOS 42s). |
| **T3** Coherencia doctrinal | ✅ CUMPLE | `grep "with sqlite3.connect" labs/*/docs/*.md` → única aparición es la **prohibición** explícita ("NO uses …"), ninguna como cura. Comando `-ExecutionPolicy Bypass -File bin\00-preparar.ps1` presente en `capstone/README.md`. |
| **T4** Árbol limpio | ✅ CUMPLE | `git status` mostró **solo** las 4 rutas del §5; tras correr T1 el árbol siguió idéntico (el arnés trabaja en copia temporal, no toca el repo). Cero archivos colaterales. |

## Detalle de los arreglos

**A — Cura de `database is locked` (Lab 04).** La sección recomendaba
`with sqlite3.connect(...)` como forma de cierre; el gestor de contexto hace *commit*
pero **no** cierra el handle → `PermissionError: [WinError 32]` en Windows. Ahora la
cura es `con.close()` en `try/finally` (como ya hacían `fuentes.py` y `arenario.py`),
con advertencia explícita del caso Windows y cita a C11 / H-07.

**B — Comando del capstone.** El único lugar del curso donde el arranque Windows se
abreviaba a "(Windows: el `.ps1`)" ahora deletrea
`powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1`, igual que los 6 labs
y el header del `.ps1`. La meta `✔ 12/12` se preservó verbatim.

**C — Política de uv.** Se elimina la deriva de tres versiones (CI latest, PO 0.9.18,
alumno latest). CI corre uv **fijo 0.11.26** (`version:` en `setup-uv`);
`setup-alumno.md` documenta piso **≥ 0.11** con su comprobación. El instalador del
alumno (`irm … | iex`) sigue igual — "latest" satisface el piso.

## Hallazgos

**Sin hallazgos nuevos.** Los tres arreglos se aplicaron acotados a su alcance; no se
descubrió defecto adicional in-repo. Nota operativa (no bloqueante): el primer run con
el pin nuevo re-descargó uv y wheels (cambió la clave de caché de `setup-uv`), de ahí
los 3m38s del job Windows frente a los ~2m previos; las corridas siguientes vuelven a
caché.

## Acción del PO (fuera del repo, anotada)

- Subir `uv` local de 0.9.18 a ≥ 0.11 para alinear con CI. Beneficio lateral posible:
  versiones recientes de uv podrían ofrecer CPython gestionado nativo `win-arm64` (lo
  que SPEC-011 §B3 marcó ausente en 0.9.18). **No es requisito** — la validación
  primaria es win-amd64 (SPEC-013).

## Veredicto final

**CERTIFICADO.**

Las tres correcciones (A, B, C) aplicadas dentro de su alcance; T1–T4 íntegros; CI
verde en macOS y Windows con uv **0.11.26 pineado**; código de los labs intacto
(12/12 y 9/9 se mantienen). La brújula quedó enderezada antes de zarpar a la
validación en Windows real (SPEC-013). 🪟🧭
