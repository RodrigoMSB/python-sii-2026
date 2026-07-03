# SPEC-009 — Suite de Pruebas del Curso + CI multiplataforma (macOS/Windows)

> **Proyecto:** Curso Programación en Python — SII 2026 · "Puerto Siracusa"
> **Emitido por:** El Arquitecto (Claude) · **Aprobado por:** Rodrigo Silva Bravo (PO)
> **Ejecutor:** mocito (Claude Code) — dueño del repositorio y único constructor
> **Fecha:** 2026-07-02 · **Versión:** 1.1 (enmendada 2026-07-03 — ver §10)
> **Dependencias:** repo con tag `curso-v1.0.0` (los 7 labs certificados)

---

## ⚠️ 0. Verificación del Arquitecto (leer PRIMERO)

**Premisas verificadas por el Arquitecto:**
- ✅ **Acción de CI verificada:** `astral-sh/setup-uv` **v8.1.0**. Astral DEJÓ de
  publicar tags mayores (`@v8` ya no se actualiza) para prevenir ataques de cadena
  de suministro — la acción se pinea por **hash de commit inmutable**
  (`08807647e7069bb48b6ef5acd8ec9567f424441b # v8.1.0`), alineado con H-03.
- ✅ La suite NO requiere dependencias nuevas: arnés 100 % stdlib; cada lab prueba
  con SU propio entorno (`uv sync` respeta cada `uv.lock`). El caché de uv acelera.
- ✅ Estrategia: cada prueba reproduce el **flujo feliz (E01)** de la certificación
  de cada lab, en una **copia temporal** (el repo jamás se ensucia), y exige el
  verificador del lab en N/N. Las cifras ya viven en los verificadores certificados
  — la suite NO las duplica: los invoca.

**Supuestos a validar por el PO o mocito ANTES de ejecutar:**
1. GitHub Actions habilitado en `python-sii-2026`. Plan gratuito 2.000 min/mes; los
   runners Windows consumen a tasa **2×** — los triggers se diseñan para gastar poco.
2. mocito verifica y pinea `actions/checkout` y `actions/upload-artifact` vigentes.
3. Repo en `main` limpio con `curso-v1.0.0` presente.

---

## 1. Objetivo

Una **prueba automática por cada una de las 7 unidades** que: (1) verifique el lab de
punta a punta como lo viviría un alumno; (2) sea ejecutable con UN comando en
macOS y en cualquier relator futuro; (3) corra automáticamente en **macOS Y Windows
reales** vía GitHub Actions — porque "debería funcionar" no es un veredicto de
ingeniería.

## 2. Estructura a crear

```
python-sii-2026/
├── pruebas/ (README.md · lib_pruebas.py · flujos.py · probar_lab.py · probar_curso.py)
└── .github/workflows/pruebas-curso.yml
```

## 3. Contratos de la suite

- **P1 — El repo jamás se ensucia:** cada prueba copia el lab a un directorio
  temporal (`tempfile.mkdtemp`, `shutil.copytree` ignorando `.venv`/`__pycache__`/
  `salidas`) y trabaja SOLO ahí; limpieza con try/finally; `git status` idéntico.
- **P2 — Arnés 100 % stdlib y multiplataforma:** `pathlib`; `subprocess.run` con
  listas de argumentos (jamás `shell=True`); `encoding="utf-8"` + `errors="replace"`;
  ANSI activado en Windows; timeouts en TODO subproceso (600 s; anti-cuelgue).
- **P3 — Data-driven:** el arnés es genérico; lo que varía por lab vive en
  `flujos.py`. Agregar un lab futuro = agregar una entrada.
- **P4 — Salida estándar del curso:** `[OK]`/`[ERROR]`+pista/`[INFO]`, resumen
  `N/N pruebas correctas`, exit 0 solo si todo pasa.
- **P5 — La suite se prueba a sí misma:** `--autocheck` sabotea una copia (borra la
  solución) y AFIRMA que la prueba FALLA. Una suite que no puede fallar es un adorno.

## 4. El flujo por lab — `flujos.py`

Dict por lab: carpeta, script del alumno, archivo de respuestas
(`RESPUESTAS.md`/`BITACORA.md`), informe y cadenas insignia esperadas (`2350000`,
`1,042,000`, `90,680,000`, `2,072,500`, `3,107,500`, `2,025,000`, `990,000`).

Pasos por lab EN ORDEN en la copia temporal (reproduce E01): (1) `uv sync`;
(2) `verificar_entorno.py` exit 0; (3) `recuperar_lab.py` (el alumno resuelve; en el
capstone la advertencia de solo-instructor es esperada); (5) ANTES de responder,
correr el verificador y AFIRMAR exit 1 (debe reclamar el interrogatorio; anti-adorno
P5-lite); (4) rellenar los marcadores del interrogatorio; (6) `verificar.py` exit 0 +
`N/N` + cadenas insignia en el informe; (7) higiene: el repo no cambió.

`probar_curso.py`: corre las 7 con tabla resumen, flags `--lab`, `--desde`,
`--listar`, `--autocheck`. `probar_lab.py`: atajo para una.

## 5. Uso local (`pruebas/README.md`)

```bash
uv run --no-project python pruebas/probar_curso.py            # todo
uv run --no-project python pruebas/probar_lab.py lab-05       # una
```
`--no-project`: el arnés es stdlib y no arrastra el entorno de ningún lab; cada lab
sincroniza el suyo en su copia temporal. Documentar duración (1ª corrida con
descargas vs cacheada).

## 6. CI — `.github/workflows/pruebas-curso.yml`

- **Matriz:** `runs-on: [macos-latest, windows-latest]`, `fail-fast: false`.
- **Triggers ahorradores:** `workflow_dispatch` (principal) + `push` a `main` con
  filtro de rutas `labs/**`, `pruebas/**`, `.github/workflows/**`.
- **Pasos:** checkout (pineado) → setup-uv **por hash**
  (`08807647e7069bb48b6ef5acd8ec9567f424441b # v8.1.0`) con `enable-cache: true` y
  `python-version: "3.13"` → `uv run --no-project python pruebas/probar_curso.py`.
- **Al fallar:** subir como artifact los logs y `salidas/` del lab caído (el arnés
  los deja en `pruebas/_reportes/`, que va al `.gitignore`).
- **Badge** del workflow en la portada — el semáforo público del curso.
- Documentar el costo (Windows 2×; por eso el trigger principal es manual).

## 7. Guion de meta-pruebas 🎭

- **M01 — Verde local (macOS):** `probar_curso.py` → 7/7, tabla resumen, repo limpio.
- **M02 — La suite puede fallar (P5):** `--autocheck` detecta el sabotaje; además,
  una cadena insignia falsa en `flujos.py` hace fallar la prueba con mensaje claro.
- **M03 — Un solo lab:** `probar_lab.py lab-04` → verde, duración razonable.
- **M04 — Aislamiento:** repo con un archivo sin commitear → la suite pasa y el
  archivo queda intacto (P1).
- **M05 — CI en ambos SO:** `workflow_dispatch` → **verde en macOS Y Windows**. EL
  entregable estrella: la primera certificación del curso en Windows real.
- **M06 — CI reporta al fallar:** en rama temporal, sabotear un lab → falla el lab
  correcto en ambos SO, artifacts presentes → borrar la rama.
- **M07 — Higiene:** `.gitignore` cubre `pruebas/_reportes/`; `git status` limpio.

## 8. Protocolo ante problemas

Si un lab FALLA en Windows en M05, es ORO PURO — no parchar en silencio: reportar
como hallazgo (síntoma, causa raíz, fix propuesto) y el Arquitecto emite la
corrección (probablemente al lab). La suite existe para encontrar eso ANTES que un
alumno del SII.

## 9. Flujo Git, certificación y DoD

Commits convencionales (`feat: suite de pruebas del curso` · `feat: CI
multiplataforma macOS/Windows` · `docs: spec SPEC-009` · `test: certificación
M01–M07`) · reporte `pruebas/docs/certificacion-suite.md` (tabla M01–M07, links a
las corridas de CI, Hallazgos, veredicto) · CERTIFICADO limpio → tag `pruebas-v1.0.0`
+ push · observación abierta → detener y consultar.

**DoD:** estructura §2 · contratos P1–P5 · flujos de las 7 unidades verdes local
(M01) · **CI verde en macOS Y Windows (M05)** · badge en portada · M01–M07
CERTIFICADO · commits + tag pusheados · hallazgos reportados.

---

## 10. Bitácora de la enmienda v1.1 (2026-07-03) — dos hallazgos ratificados

La suite hizo su trabajo en la primera corrida de CI: encontró **dos defectos reales de
portabilidad a Windows** que el curso arrastraba y que ningún alumno de macOS/Linux
habría visto (POSIX es más permisivo). Ambos tocaron código certificado; el PO los
**ratificó** con los fixes propuestos, y sus lecciones se elevan a **doctrina permanente
del curso**.

### H-06 — La salida del curso revienta en stdout no-consola de Windows

- **Síntoma:** el job de Windows abortó con `UnicodeEncodeError: 'charmap' codec can't
  encode` al imprimir `═` (título) y, aguas abajo, `✔`, `→`, emojis.
- **Causa raíz:** en Windows, cuando `stdout` **no es una consola** sino un *pipe* (CI,
  redirección), Python usa **cp1252**, que no contiene los símbolos del curso. Un alumno
  en terminal interactiva NO lo ve; solo aparece con salida canalizada. Afectaba a los
  **7 `lib_comunes.py`** y a los programas del alumno (p. ej. Lab 02 imprime `código → motivo`).
- **Fix (dos capas):** (1) la **infraestructura** (`lib_comunes.py` de los 7 labs +
  arnés `lib_pruebas.py`) reconfigura `sys.stdout/stderr` a `utf-8` con `errors="replace"`
  al arrancar — no-op en macOS; (2) `PYTHONUTF8: "1"` a nivel del workflow, para que
  **todo** proceso Python del runner (incluidos los programas del alumno) use UTF-8 bajo
  el pipe de Actions, **sin** ensuciar el código pedagógico con andamiaje de encoding.

### H-07 — El fabricador del verificador de Lab 04 filtra una conexión sqlite

- **Síntoma:** ya sin el crash de H-06, Windows quedó en **6/7**: Lab 04 falló con
  `PermissionError [WinError 32] ... c.db ... being used by another process` al limpiar
  el `TemporaryDirectory` de la prueba sorpresa.
- **Causa raíz:** `_fuentes_sorpresa` creaba la BD con `with sqlite3.connect(r_db) as con:`.
  Ese context manager de sqlite3 es **transaccional** (commit/rollback), **no cierra** la
  conexión. En POSIX es inocuo (se puede borrar un archivo con handle abierto); en Windows
  el handle vivo bloquea el borrado del directorio temporal. El **fabricador del propio
  verificador** violaba el contrato **C11** que el lab enseña; la **solución del alumno sí
  lo cumplía**.
- **Fix:** cerrar con `try/finally` (patrón C11). Se auditó el curso completo y se
  corrigió el **mismo patrón** en `generar_fuentes.py` de Lab 04 y del capstone (no
  crasheaban por escribir a archivo persistente, pero el patrón queda proscrito).

### Doctrina permanente derivada (contratos del curso)

- **C19 (nuevo) — UTF-8 en toda infraestructura:** todo *verificador*, *arnés* y
  *recuperador* reconfigura `stdout`/`stderr` a UTF-8 (`errors="replace"`) al arrancar,
  para no depender de la consola. **El código del alumno queda libre de andamiaje de
  encoding**: su robustez la aporta la infraestructura y, en CI, `PYTHONUTF8=1`.
- **C11 (aclaración, alcance ampliado) — cierre garantizado, también en código de
  verificación:** el cierre explícito de conexiones sqlite aplica a **todo** el código del
  curso, no solo a la solución del alumno. **`with sqlite3.connect(...)` queda prohibido
  como mecanismo de cierre en todo el curso** (es transaccional, no de cierre); se usa
  `con = sqlite3.connect(...)` + `try/finally: con.close()`.

### Nota de certificación

- **M06** (CI reporta al fallar) se validó por **incidente real**, no por sabotaje
  sintético: la corrida [`28630016496`](https://github.com/RodrigoMSB/python-sii-2026/actions/runs/28630016496)
  falló de verdad, señaló **exactamente `FALLA Lab 04`** y el paso `if: failure()` **subió
  el artifact** que se descargó y usó para diagnosticar H-07. Mejor evidencia que un
  sabotaje fabricado, y ahorra minutos de Windows (tasa 2×).
- **M05** verde total: [`28630203022`](https://github.com/RodrigoMSB/python-sii-2026/actions/runs/28630203022)
  — `macos-latest 7/7` · `windows-latest 7/7`.

---

*Firmado: El Arquitecto de Puerto Siracusa.*
*"En este puerto no se dice 'debería funcionar en Windows'. Se muestra el semáforo
en verde — en un Windows de verdad."* 🏛️🚦📐
