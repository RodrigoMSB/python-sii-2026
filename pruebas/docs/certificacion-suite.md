# Certificación — Suite de Pruebas del Curso (SPEC-009)

> **Proyecto:** Curso Programación en Python — SII 2026 · "Puerto Siracusa"
> **Constructor:** mocito (Claude Code) · **Aprobación pendiente:** Rodrigo Silva Bravo (PO)
> **Fecha:** 2026-07-03 · **Base:** `curso-v1.0.0` (7 unidades certificadas)
> **Estado:** ✅ CERTIFICADO técnicamente · ⏸️ **tag `pruebas-v1.0.0` EN ESPERA** de
> ratificación del PO (dos hallazgos tocaron labs certificados).

---

## 0. Veredicto en una línea

La suite corre el **flujo feliz del alumno de las 7 unidades** en macOS **y en Windows
reales** vía GitHub Actions, y el semáforo quedó **verde en ambos SO (7/7)**. En el
camino encontró **dos defectos reales de portabilidad** que el curso arrastraba y que
ningún alumno de Mac habría visto jamás — exactamente para lo que se construyó.

**Corrida estrella (M05):** [`run 28630203022`](https://github.com/RodrigoMSB/python-sii-2026/actions/runs/28630203022)
— `macos-latest: success (7/7)` · `windows-latest: success (7/7)` · higiene: repo idéntico en ambos.

---

## 1. Tabla de meta-pruebas (SPEC-009 §7)

| Meta | Qué exige | Resultado |
|---|---|:---:|
| **M01** | Verde local (macOS): `probar_curso.py` → 7/7, tabla, repo limpio | ✅ |
| **M02** | La suite puede fallar: `--autocheck` detecta el sabotaje; insignia falsa falla claro | ✅ |
| **M03** | Un solo lab: `probar_lab.py lab-04` → verde, duración razonable | ✅ |
| **M04** | Aislamiento: archivo sin commitear intacto tras correr (P1) | ✅ |
| **M05** | **CI verde en macOS Y Windows reales** — el entregable estrella | ✅ |
| **M06** | CI reporta al fallar: lab correcto señalado + artifacts presentes | ✅ (por incidente real, ver §3) |
| **M07** | Higiene: `.gitignore` cubre `_reportes/`; `git status` limpio | ✅ |

### Detalle de las corridas de CI

| Corrida | Commit | macOS | Windows | Qué destapó |
|---|---|:---:|:---:|---|
| [28629713460](https://github.com/RodrigoMSB/python-sii-2026/actions/runs/28629713460) | (pre-fix) | ✅ | ❌ | **H-06** — `UnicodeEncodeError` en stdout cp1252 |
| [28630016496](https://github.com/RodrigoMSB/python-sii-2026/actions/runs/28630016496) | `b7a2ffc` | ✅ | ❌ (6/7) | **H-07** — `WinError 32` en Lab 04 (handle sqlite) |
| [**28630203022**](https://github.com/RodrigoMSB/python-sii-2026/actions/runs/28630203022) | `c09abbb` | ✅ **7/7** | ✅ **7/7** | — verde total |

---

## 2. Hallazgos (ORO PURO — requieren ratificación del PO)

Ambos son **defectos reales de portabilidad a Windows**, invisibles en macOS/Linux
porque POSIX es más permisivo. Ambos tocaron **código certificado**, por lo que —
siguiendo el protocolo de H-01/H-03/H-04 — se aplicó el fix, se verificó verde en CI,
pero **el tag se retiene** hasta que el PO ratifique.

### 🟡 H-06 — La salida del curso revienta en stdout no-consola de Windows

- **Síntoma:** en la primera corrida de CI, el job de Windows abortó con
  `UnicodeEncodeError: 'charmap' codec can't encode character` al imprimir `═` (título)
  y, aguas abajo, cualquier `✔`, `→` o emoji.
- **Causa raíz:** en Windows, cuando `stdout` **no es una consola** sino un *pipe*
  (CI, redirección `> archivo`, `| more`), Python usa el encoding **cp1252** por
  defecto, que no tiene los símbolos del curso. Un alumno en una terminal interactiva
  **no** lo ve (la consola sí es UTF-8); solo aparece con salida canalizada, como en CI.
  Afectaba a **los 7 verificadores** (`lib_comunes.py`) y a **los programas del alumno**
  (p. ej. Lab 02 imprime `código → motivo`).
- **Fix (dos capas, `commit b7a2ffc`):**
  1. **Infra robusta por sí misma:** `lib_comunes.py` (7 labs) y el arnés
     (`lib_pruebas.py`) reconfiguran `sys.stdout/stderr` a `utf-8` con
     `errors="replace"`. No-op en macOS.
  2. **CI:** `PYTHONUTF8: "1"` a nivel de workflow → **todo** proceso Python del runner
     (incluidos los programas del alumno, que se mantienen **limpios** de andamiaje de
     encoding) usa UTF-8 bajo el pipe de Actions.
- **Por qué no se tocan los programas del alumno:** su código pedagógico no debe cargar
  boilerplate de encoding; además ya escriben sus informes a disco en UTF-8. La robustez
  vive en la **infraestructura** (verificadores) y en la **config de CI**.

### 🟡 H-07 — El fabricador del verificador de Lab 04 filtra una conexión sqlite

- **Síntoma:** ya sin el crash de H-06, Windows quedó en **6/7**: Lab 04 falló con
  `PermissionError: [WinError 32] ... c.db ... being used by another process` al limpiar
  el `TemporaryDirectory` de la prueba sorpresa.
- **Causa raíz:** `_fuentes_sorpresa` creaba la BD sorpresa con
  `with sqlite3.connect(r_db) as con:`. Ese context manager de sqlite3 es
  **transaccional** (hace commit/rollback), **no cierra la conexión**. En POSIX da igual
  (se puede borrar un archivo con handle abierto); en Windows el handle vivo sobre `c.db`
  **bloquea** el borrado del directorio temporal → `WinError 32`. Irónicamente, el
  **fabricador del propio verificador** violaba el contrato **C11 ("cierre garantizado")**
  que el lab enseña; la **solución del alumno sí lo cumplía**.
- **Fix (`commit c09abbb`):** cerrar la conexión a mano con `try/finally` (patrón C11).
  No-op funcional en macOS.

---

## 3. Nota sobre M06 (CI reporta al fallar)

M06 se validó con **evidencia real**, mejor que un sabotaje sintético: la corrida
[28630016496](https://github.com/RodrigoMSB/python-sii-2026/actions/runs/28630016496)
falló de verdad y demostró la cadena completa de reporte:

- La tabla resumen señaló **exactamente el lab correcto** (`FALLA  Lab 04`), no otro.
- El paso `if: failure()` **subió el artifact** `reportes-windows-latest.zip` (7 ficheros:
  `log.txt` con el traceback + `salidas/` de la copia caída), que se **descargó y usó**
  para diagnosticar H-07.
- La higiene (P1) se mantuvo aun en el fallo: `git status` sin cambios.

Complementariamente, `--autocheck` (P5) demuestra en local, de forma determinista, que
la suite **puede** fallar (sabotea una copia y afirma el fallo). Se decide **no** gastar
minutos extra de Windows (tasa 2×) en un sabotaje sintético cuando dos incidentes reales
ya ejercieron el camino de fallo + artifact + identificación del lab.

---

## 4. Cumplimiento de contratos P1–P5

| Contrato | Evidencia |
|---|---|
| **P1** — el repo jamás se ensucia | copia a `tempfile.mkdtemp`; `git status` idéntico antes/después, en macOS y Windows (M04, M07). |
| **P2** — 100 % stdlib, portable | `pathlib`, `subprocess.run` con listas (nunca `shell=True`), utf-8 + `errors=replace`, timeouts 600 s, ANSI/UTF-8 en Windows. |
| **P3** — data-driven | el arnés es genérico; cada lab es una entrada en `flujos.py`. |
| **P4** — salida estándar | `[OK]`/`[ERROR]`+pista/`[INFO]`, resumen `N/N`, exit 0 solo si todo pasa. |
| **P5** — la suite se prueba a sí misma | `--autocheck` (M02) + dos hallazgos reales atrapados en Windows. |

---

## 5. DoD (SPEC-009 §9)

- [x] Estructura §2 (`pruebas/` + workflow).
- [x] Contratos P1–P5.
- [x] Flujos de las 7 unidades verdes local (M01).
- [x] **CI verde en macOS Y Windows (M05).**
- [x] Badge en la portada.
- [x] M01–M07 certificadas.
- [x] Commits pusheados (`feat:` suite, `feat:` CI, `docs:` spec, dos `fix:` de hallazgos).
- [x] Hallazgos reportados (H-06, H-07).
- [ ] **Tag `pruebas-v1.0.0`** — ⏸️ retenido a la espera de la **ratificación del PO**
      de H-06 y H-07 (ambos tocan labs certificados; precedente H-01/H-03/H-04).

---

*"En este puerto no se dice 'debería funcionar en Windows'. Se muestra el semáforo en
verde — en un Windows de verdad."* 🏛️🚦📐
