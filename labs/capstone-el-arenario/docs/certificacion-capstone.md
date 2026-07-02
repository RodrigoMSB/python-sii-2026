# Certificación del Capstone — El Arenario

> Reporte de pruebas y **regresión final del curso** (§11–§13 del SPEC-008).

## Datos de la corrida

| Ítem | Valor |
|------|-------|
| Fecha | 2026-07-02 |
| Máquina | macOS 26.5.1 (build 25F80), Apple Silicon |
| `uv` | 0.9.18 |
| Python resuelto | **3.13.7** (`==3.13.*`) |
| Bibliotecas | numpy 2.5.0 · pandas 3.0.3 · openpyxl 3.1.5 · matplotlib 3.11.0 |
| Método | Clon limpio; comandos como alumno (siempre `uv run`) |
| Verificaciones del capstone | **9** (mide PRODUCTOS, C18; E01 → 8/9 con único error de bitácora) |

## Resultado por escenario

| Esc. | Veredicto | Evidencia breve |
|------|-----------|-----------------|
| **E01** El alumno competente | ✅ CUMPLE | Preparador `✔ 12/12` (deps + 4 fuentes). Solución de referencia → los 6 productos en `salidas/`. Verificador sin BITACORA → `✘ 8/9`. Con BITACORA respondida → `✔ 9/9`, exit 0, Don Arquímedes firma y declara **Analista de Datos de Puerto Siracusa**. |
| **E02** El alumno a medias | ✅ CUMPLE | Solo `censo_depurado.csv` (correcto, 27×4, $3.238.000). Verificador → `✘ 1/9`: el censo pasa, y CADA producto faltante (tablero, tramos, informe, gráficos, gestion.db, bitácora) se reporta con su pista. Exit 1. |
| **E03** El fabricante | ✅ CUMPLE | Informe correcto ($990.000) PERO tablero alterado (saldo +$500.000). El verificador detecta la **inconsistencia** contra las fuentes: check de tablero falla (saldo $1.490.000 ≠ $990.000) y saldo por rubro falla (Gastronomía $506.500 ≠ $6.500), aunque el informe pase. `✘ 6/9`, exit 1. El anti-loro por consistencia funciona. |
| **E04** Perdido (ubicación) | ✅ CUMPLE | `arenario.py` ejecutado desde `escenario/` → `FileNotFoundError: ... escenario/datos/censo_anual.csv`. Cura verificada (raíz → `SALDO $990,000`). |
| **E05** Rompe cosas | ✅ CUMPLE | Borrar `saldo_por_rubro.png` → `✘ 8/9` "png ausente"; cura → `✔ 9/9`. Corromper `pagos_anuales.xlsx` → entorno lo detecta ("Falta o está mal"); borrar el corrupto + `generar_fuentes.py` (H-04) → `✔ 12/12`. `SyntaxError` en el script del alumno → el script no genera productos y el verificador (que mide productos, C18) reporta `✘ 1/9` sin explotar. |
| **E06** Rescate de demostración | ✅ CUMPLE | `recuperar_lab.py` → `✔ 4/4`, con la **advertencia visible de SOLO INSTRUCTOR / NO certifica**; reconstruye los productos de demostración y **NO toca la BITACORA** (queda pendiente). |
| **E07** Idempotencia | ✅ CUMPLE | Preparador 2ª/3ª vez → `✔ 12/12`. Generador ×2 (solo-faltantes) → no-op (2 fuentes no tocadas). Pipeline de referencia ×2 → `tablero_anual.csv` idéntico. |
| **E08** Higiene del repo | ✅ CUMPLE | Clon "sucio" tras E06/E07 → `git status --porcelain` = 0 líneas. `arenario.py`, `BITACORA.md` y `salidas/` ignorados; semilla, `censo_anual.csv`, `multas.json` y las fuentes generadas (xlsx/db) versionadas e intactas. |
| **E09** Regresión FINAL del curso | ✅ CUMPLE | Los **6 labs** verificados de una pasada: Lab 01 `✔ 12/12`, Lab 02 `✔ 11/11`, Lab 03 `✔ 13/13`, Lab 04 `✔ 12/12`, Lab 05 `✔ 14/14`, Lab 06 `✔ 14/14`. `git diff` de los seis labs entre `lab-06-v1.0.0` y HEAD = vacío: intactos. **El curso entero se certifica.** |

## Hallazgos

**Sin hallazgos.** Los 9 escenarios cumplen íntegros. Todas las cifras de control se
computaron con el pipeline de referencia completo en pandas real y coinciden con §0
(depurado 27/$3.238.000, pagos 31/$2.553.000, huérfanos $30.000 y $120.000, tablero
pagado $2.523.000, multas $275.000, **saldo anual $990.000**, tramos 4/13/7/3, saldo
por rubro 193.5k/6.5k/790k, al día 16/morosos 11, pivot Comercio/VENCIDA −$202.000).
Doctrinas aplicadas: H-03 (deps sin yank), H-04 (binarios vía generador
solo-faltantes; el recuperador maneja corrupción), H-05 (marcador `s/d`). El
verificador mide productos (C18) y el anti-loro es la consistencia (E03 lo confirma).

## Veredicto final

**CERTIFICADO.**

Los 9 escenarios (E01–E09) cumplen íntegros; la regresión final deja los 6 labs en
verde e intactos. Sin deviación de la spec, sin observaciones abiertas. **Con esto se
cierra el curso Python SII 2026 — "Puerto Siracusa": 6 laboratorios + capstone, tres
módulos, un puerto entero contado.** Se liberan los tags `capstone-v1.0.0` y
`curso-v1.0.0`. 🎓🏖️
