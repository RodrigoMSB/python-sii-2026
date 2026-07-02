# SPEC-005 — Lab 04: "Las cuatro fuentes"

> **Proyecto:** Curso Programación en Python — SII 2026 · "Puerto Siracusa"
> **Emitido por:** El Arquitecto (Claude) · **Aprobado por:** Rodrigo Silva Bravo (PO)
> **Ejecutor:** mocito (Claude Code) — dueño del repositorio y único constructor
> **Fecha:** 2026-07-02 · **Versión:** 1.1
> **Dependencias:** repo con tags `lab-01/02/03-v1.0.0` (SPEC-002/003/004 completados)

> **Bitácora de enmiendas**
> - **SPEC-005 v1.1 — Hallazgo H-04 (generador de fuentes), ratificado por el
>   Arquitecto** (2026-07-02):
>   - **(a) Causa raíz:** un `.xlsx` es internamente un **ZIP** que incrusta
>     marcas de tiempo (en las entradas del zip y en `docProps/core.xml`), por lo
>     que openpyxl **no** produce el archivo byte a byte idéntico entre
>     generaciones (fijar propiedades del workbook y timestamps del zip no basta).
>     El `.csv`, `.json` y `.db` sí son deterministas.
>   - **(b) Idempotencia redefinida:** la idempotencia del generador se mide por el
>     **estado final** (las cuatro fuentes válidas y presentes en `datos/fuentes/`),
>     **no** por los bytes exactos. Por eso §5.5 cambia de "borra y crea todo desde
>     cero" a "**regenera solo lo que falte** por defecto; `--force` reconstruye
>     todo". Con las cuatro presentes es un no-op y el repo versionado no se ensucia
>     (resuelve la contradicción §5.5 ↔ §12-E08, ya anticipada por la nota de §12-E07).
>   - **(c) Rider — fuente corrupta pero presente:** como el modo por defecto no
>     reescribe lo presente, la cura de una fuente **dañada pero en su lugar** es
>     **borrar el archivo + correr el generador**. El **recuperador** aplica esa
>     misma lógica automáticamente: detecta las fuentes ilegibles, las elimina y las
>     repone. `docs/troubleshooting.md` documenta la cura manual; ambos ajustados en
>     el commit de la enmienda.

---

## ⚠️ 0. Verificación del Arquitecto (leer PRIMERO)

**Premisas verificadas por el Arquitecto:**
- ✅ **Versiones pineadas, verificadas contra PyPI el 2026-07-02, INCLUYENDO
  estado de retiro (lección H-03):** `numpy==2.5.0` y `pandas==3.0.3`
  (mismas del Lab 03, ya validadas y con H-03 resuelto) +
  `openpyxl==3.1.5` (última estable, publicada 2024-06-28, **sin yank**,
  motor estándar de pandas para `.xlsx`). SQLite NO requiere dependencia:
  `sqlite3` es stdlib.
- ✅ **Cifras de control computadas y validadas** (§5): CSV pagos → 12
  registros, $677.500 · XLSX permisos → 8 registros, $1.000.000 · JSON
  multas → 10 registros, $395.000 · BD contribuyentes → 10 registros ·
  **gran total de ingresos: $2.072.500**.
- ✅ Spec autosuficiente. Los archivos binarios (.xlsx, .db) NO se
  especifican byte a byte: se especifica el **generador** que los produce
  desde datos verbatim (§5.5) — misma garantía de reproducibilidad.
- ✅ Alcance cruzado contra temario: cierra el **Módulo 2** (carga desde
  CSV, Excel, JSON y BD relacionales + transacciones + exportación).

**Supuestos a validar por el PO o mocito ANTES de ejecutar:**
1. Repo en `main` limpio y sincronizado; Labs 01–03 certificados intactos.
2. Internet disponible para el `uv sync` (openpyxl es descarga nueva).
3. Sin cambios de sistema desde SPEC-004.

---

## 1. Contexto y narrativa del lab

Don Arquímedes convocó a las oficinas del municipio a entregar sus datos
del mes... y cada una respondió en su propio dialecto: **Tesorería** mandó
un CSV exportado de su sistema, la **Oficina de Turismo** un Excel hecho a
mano, el **sistema antiguo de multas** solo sabe escupir JSON, y el
**registro de contribuyentes** vive en una base SQLite que nadie se atreve
a tocar "porque una vez se borró algo".

> *"Cuatro oficinas, cuatro formatos, un solo analista. Dame un lector
> para cada dialecto y moveré el informe mensual."* — Don Arquímedes

El dolor pedagógico: hasta ahora los datos llegaban cómodamente como
módulos Python. **En la vida real los datos llegan en archivos** — y este
lab es el rito de paso. Además, el miedo del municipio a la BD ("una vez
se borró algo") motiva el tema estrella del temario: **transacciones** —
commit cuando todo salió bien, rollback cuando algo falló, y nada queda a
medias.

Misión: construir `fuentes.py` — lee las cuatro fuentes, registra un pago
nuevo en la BD **transaccionalmente**, consolida el resumen de ingresos y
lo **exporta** en los cuatro formatos (el informe viaja de vuelta a cada
oficina en su propio dialecto 😄).

## 2. Datos duros

| Ítem | Valor |
|------|-------|
| Carpeta del lab | `labs/lab-04-cuatro-fuentes/` |
| Duración objetivo | ~2,0 horas (Módulo 2, 2ª mitad → lo cierra; presupuesto: 7 labs / 20 hrs) |
| Python | 3.13 pineado con `uv` |
| Dependencias | `numpy==2.5.0` · `pandas==3.0.3` · `openpyxl==3.1.5` |
| Tag al certificar | `lab-04-v1.0.0` |

## 3. Estructura del lab

Anatomía estándar, con la novedad de la carpeta de fuentes:

```
labs/lab-04-cuatro-fuentes/
├── README.md · pyproject.toml · .python-version
├── bin/ (00-preparar.sh/.ps1 · lib_comunes.py · verificar_entorno.py ·
│         verificar.py · recuperar_lab.py · generar_fuentes.py)
├── datos/
│   ├── fuentes_semilla.py       ← datos VERBATIM (§5.1–5.4) — única fuente de verdad
│   └── fuentes/                 ← generada por generar_fuentes.py (§5.5):
│       ├── pagos.csv
│       ├── permisos_eventos.xlsx
│       ├── multas.json
│       └── contribuyentes.db
├── guia/ (01-contexto.md · 02-csv-y-excel.md · 03-json.md ·
│          04-base-de-datos.md · 05-consolidado.md)
├── plantillas/ (fuentes.py con TODO 1..6 · RESPUESTAS.md)
├── soluciones/ (fuentes.py · desafio-quinta-fuente.md)
└── docs/troubleshooting.md
```

**Decisión de arquitectura sobre binarios:** `datos/fuentes/` **SÍ se
versiona en git** (archivos pequeños, el alumno los recibe listos), pero su
única fuente de verdad es `fuentes_semilla.py` + el generador. Si un alumno
corrompe una fuente, el generador la reconstruye (y el recuperador lo
invoca). Regla: los archivos de `datos/fuentes/` que el ALUMNO modifica
jamás — son entrada de solo lectura; todo lo que el alumno produce va a
`salidas/`.

## 4. Alcance pedagógico (temario Módulo 2, cierre)

**Cubre:** lectura con pandas: `read_csv` (separadores, encoding UTF-8,
`decimal`/`thousands` como parámetros mencionados), `read_excel`
(`sheet_name`, motor openpyxl), `read_json` / módulo `json` stdlib
(diferencia entre ambos caminos), `read_sql` + `sqlite3` stdlib
(conexión, cursor, consultas) · **transacciones en BD**: `commit`,
`rollback`, `IntegrityError`, patrón `with` para conexiones ·
**exportación**: `to_csv` (index=False), `to_excel`, `to_json`, `to_sql` ·
inspección post-carga (`head/info/dtypes`) como hábito.

**Fuera de alcance (Módulo 3 / Labs 05–06):** limpieza de datos sucios,
merge/concat entre fuentes, groupby/pivot. Aquí cada fuente se resume POR
SEPARADO — la combinación es el plato fuerte del Lab 06 y no se adelanta.

## 5. Datos semilla — `datos/fuentes_semilla.py` (VERBATIM, es contrato)

Módulo con docstring narrativo y CUATRO constantes. Formato de código de
patente ya conocido (`PS-####-Y`).

### 5.1 `PAGOS_CSV` — lo que Tesorería exporta (12 filas)
Lista de listas `[codigo, fecha, monto]` (fecha como str ISO). 12 pagos,
total **$677.500**.

### 5.2 `PERMISOS_XLSX` — lo que Turismo arma a mano (8 filas)
`[folio, evento, valor]`. 8 permisos, total **$1.000.000** (redondo a
propósito: la guía lo usa para que el alumno desconfíe y verifique).

### 5.3 `MULTAS_JSON` — lo que el sistema antiguo escupe (10 objetos)
`[codigo, motivo, monto]`. 10 multas, total **$395.000**.

### 5.4 `CONTRIBUYENTES_BD` — el registro maestro (10 filas)
`[codigo, nombre, giro]` — tabla `contribuyentes`, `codigo` PRIMARY KEY.
10 contribuyentes. **Gran total de ingresos del mes: $2.072.500.**

(Los cuatro datasets van VERBATIM en `datos/fuentes_semilla.py` — ver ese
archivo para los registros exactos.)

### 5.5 `bin/generar_fuentes.py` — el generador (herramienta del curso)
Script que construye `datos/fuentes/` desde la semilla:
- `pagos.csv`: UTF-8, separador coma, CON encabezado `codigo,fecha,monto`.
- `permisos_eventos.xlsx`: hoja `Permisos`, encabezados `folio,evento,valor`
  (vía pandas+openpyxl).
- `multas.json`: lista de objetos `codigo,motivo,monto`, UTF-8,
  `ensure_ascii=False`, indentado 2.
- `contribuyentes.db`: SQLite, tabla `contribuyentes (codigo TEXT PRIMARY
  KEY, nombre TEXT NOT NULL, giro TEXT NOT NULL)`, 10 INSERT, commit.
- **Idempotente por ESTADO FINAL (v1.1, H-04):** por defecto regenera **solo
  las fuentes que falten** (así, con las cuatro presentes es un no-op y no
  reescribe el `.xlsx`, que no es determinista byte a byte). Con `--force`
  reconstruye las cuatro desde cero. La cura de una fuente corrupta-pero-presente
  es **borrarla + regenerar**; el recuperador (§8.3) lo hace automáticamente. Es
  la ÚNICA herramienta autorizada a escribir en `datos/fuentes/`.

## 6. Contratos de código
Rigen **C1–C10**. Agregados:
- **C11:** toda conexión sqlite3 se maneja con context manager o
  try/finally con `close()` garantizado; ninguna conexión queda abierta.
- **C12:** las rutas a `datos/fuentes/*` se construyen con `pathlib`
  relativas a la raíz del lab; los lectores reciben la ruta como parámetro
  (funciones testeables — el verificador les pasará SUS PROPIOS archivos
  sorpresa).

## 7. El programa del lab — `fuentes.py`

### 7.1 Solución (`soluciones/fuentes.py`)
Funciones obligatorias (todas reciben rutas como parámetro — C12):
`cargar_pagos`, `cargar_permisos` (`sheet_name="Permisos"`),
`cargar_multas` (json.load stdlib + DataFrame), `cargar_contribuyentes`
(sqlite3 + read_sql, cierre C11), `registrar_pago` (corazón transaccional:
valida existencia del código; si no existe → rollback + False; si existe →
INSERT + commit + True; sin prints), `resumen_ingresos` (dict pagos/
permisos/multas/total, ints, total==2_072_500), `exportar_resumen`
(resumen.csv index=False, resumen.xlsx, resumen.json, to_sql resumen_mensual
en gestion.db), `construir_informe` (título, `=`×58, renglones con `:,`,
TOTAL $2,072,500, sección Registro transaccional), `main` (carga las 4,
registra un pago válido y uno inválido, imprime informe, escribe
salidas/informe_fuentes.txt, exporta).

### 7.2 Plantilla — TODO 1..6
TODO 1 cargar_pagos · TODO 2 cargar_permisos · TODO 3 cargar_multas ·
TODO 4 registrar_pago (el grande, try/commit/except/rollback) · TODO 5
resumen_ingresos · TODO 6 exportar_resumen. Corre con TODOs pendientes.

## 8. Verificadores

### 8.1 `verificar_entorno.py`
Checks estándar + imports tolerantes de numpy/pandas/**openpyxl** con
versiones pineadas + **existencia de las 4 fuentes** en `datos/fuentes/`
(pista si faltan: `uv run python bin/generar_fuentes.py`).

### 8.2 `bin/verificar.py` — checks (en orden)
Referencia propia + **fuentes sorpresa** en directorio temporal (tempfile):
csv/xlsx/json/db pequeños y aleatorios pasados a las funciones del alumno
(gracias a C12). Checks: existe · importa (anti-cuelgue C8) · 8 funciones ·
las 4 cargas oficiales con shapes y columnas exactas · resumen oficial ==
{677500, 1000000, 395000, 2072500} · cargas + resumen con fuentes sorpresa ==
referencia · **transaccional** sobre COPIA temporal (válido→True/fila queda;
inválido→False/tabla NO crece) · salidas con informe (2,072,500) + 4
exportados legibles · RESPUESTAS sin marcadores.

### 8.3 `recuperar_lab.py`
Estándar + PASO NUEVO (v1.1, H-04): primero **detecta y elimina las fuentes
ilegibles** (corruptas o dañadas) y luego invoca `generar_fuentes.py` (modo
solo-faltantes) para reponer lo que falte —incluyendo lo recién borrado—; después
solución → raíz → ejecutar → interrogatorio intacto/pendiente. Así las fuentes
sanas no se reescriben (git limpio) y las dañadas se reponen.

## 9. Guías (redacción de mocito; convenciones y cápsulas de siempre)

- **01-contexto.md** — la convocatoria; entorno; `generar_fuentes.py` (la
  imprenta del lab); tour por `datos/fuentes/` abriendo cada archivo con
  herramientas humanas (💥 xlsx/db en crudo = binario; "un archivo es bytes
  con formato"); regla de oro fuentes de solo lectura → salidas/.
- **02-csv-y-excel.md** — `read_csv` (encoding; 🔮 dtype de monto; sep/
  decimal/thousands); ritual head/info/dtypes; `read_excel` + sheet_name
  (💥 hoja "permisos" minúscula → error); sumas por fuente; el $1.000.000
  redondo → describe() (sana paranoia).
- **03-json.md** — anatomía; DOS caminos (json.load stdlib vs read_json);
  cuándo cada uno; 🔮 tipo que devuelve json.load; 💥 coma extra en COPIA →
  JSONDecodeError con línea/columna.
- **04-base-de-datos.md** — sqlite3 + read_sql; transacciones con analogía
  caja municipal; demos INSERT sin commit (no persiste), commit (persiste),
  duplicado PRIMARY KEY → IntegrityError → rollback; patrón with; 🤖 ACID.
- **05-consolidado.md** — bifurcación; construir/ejecutar fuentes.py
  (cifras + pago rechazado); exportación (4 to_*); modificación P5;
  interrogatorio; verificación; desafío quinta fuente (sep=";", decimal=",").
  Checkpoint + teaser Lab 05.

## 10. Troubleshooting (agregados del lab)
Heredados + nuevos: `ImportError: Missing optional dependency 'openpyxl'`
(fuera de uv run) · xlsx/db "basura" con editor (binario: normal) ·
`database is locked` (conexión abierta; C11) · Excel bloquea el xlsx abierto
en Windows · `UnicodeDecodeError` (perilla `encoding=`) · JSONDecodeError
línea/columna.

## 11. Interrogatorio — 5 preguntas (marcador estándar; H-02 vigente)

1. **La boleta sin timbre:** qué pasó con la fila insertada SIN commit al
   reabrir la BD; explicar con la caja qué protege.
2. **El rollback real:** qué retornó `registrar_pago` con `PS-9999-X`;
   filas antes/después; qué línea evita la "media boleta".
3. **Los dos caminos del JSON:** qué tipo devolvió `json.load`; cuándo
   preferirlo sobre `read_json`.
4. **El dtype del dinero:** con qué dtype llegó `monto` del CSV; y si fuera
   "45.000" con punto de miles, qué perilla lo arregla.
5. **Modifica y explica (Explorador):** cambiar el pago válido por un código
   inexistente; qué cambia en informe y en `pagos_registrados`; revertir.

## 12. Guion de pruebas 🎭 (clon limpio, en orden, evidencia por escenario)

- **E01 — Flujo feliz Explorador:** preparar (descarga openpyxl) → 4 fuentes
  presentes → solución → ejecutar → informe `$2,072,500` + pago True/False →
  salidas con 4 exportados → verificador N-1/N → responder → N/N exit 0.
- **E02 — Artesano a medio camino:** plantilla → pistas → SOLO TODO 1 →
  check CSV pasa, resto no.
- **E03 — Tramposo:** hardcodear retornos → fuentes sorpresa lo cazan ×3.
- **E04 — Perdido:** copiar solución a guia/, ejecutar desde ahí → error de
  ruta documentado con cura; limpiar.
- **E05 — Rompe cosas:** borrar `multas.json` → entorno lo detecta con pista
  del generador → regenerar → verde · corromper JSON (coma extra) → carga
  reporta JSONDecodeError legible → regenerar · SyntaxError y breakpoint()
  estándar · **transaccional:** fuentes.py dos veces → sin duplicar efectos
  descontroladamente (documentar y validar).
- **E06 — Rezagado:** recuperador (incluye regenerar fuentes) → N-1/N.
- **E07 — Idempotencia:** preparador ×3 sin re-descargas; generador ×2 →
  fuentes idénticas (comparar checksums; documentar qué se compara).
- **E08 — Higiene:** `git status` limpio (`labs/*/fuentes.py` +
  `labs/*/salidas/` ignorados; `datos/fuentes/` SÍ versionado).
- **E09 — Regresión:** verificadores de Labs 01, 02 y 03 → todos en verde;
  `git diff` limpio fuera del Lab 04 y portada.

## 13. Cambios en archivos existentes (únicas excepciones)
Portada: Lab 04 ✅ Disponible · `.gitignore`: artefacto de alumno del lab
(`labs/*/fuentes.py`).

## 14. Flujo Git, certificación y DoD
Commits convencionales (`feat: Lab 04 — Las cuatro fuentes` · `docs: spec
SPEC-005` · `test: certificación del Lab 04 como alumno` + fixes) ·
reporte `docs/certificacion-lab-04.md` (tabla E01–E09, Hallazgos,
veredicto) · CERTIFICADO limpio → tag `lab-04-v1.0.0` + push · observación
abierta → detener y consultar (protocolo H-01/H-03).

**DoD:** lab conforme §3–§11 · fuentes generadas y versionadas con su
generador · portada/.gitignore al día · E01–E09 CERTIFICADO · commits +
tag pusheados · hallazgos reportados.

---

*Firmado: El Arquitecto de Puerto Siracusa.*
*"Cuatro dialectos, un analista — y el informe vuelve a cada oficina en su
propio idioma."* 🏛️📐
