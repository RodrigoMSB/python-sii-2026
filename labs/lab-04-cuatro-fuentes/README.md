# Lab 04 — Las cuatro fuentes ⚓

> Módulo 2 (cierre) · ~2,0 horas · lee datos de **archivos reales** (CSV, Excel,
> JSON) y una **base de datos** SQLite · requiere Internet la primera vez.

## El encargo

Don Arquímedes convocó a las oficinas del municipio a entregar sus datos del mes,
y cada una respondió en su propio dialecto: **Tesorería** un CSV, la **Oficina de
Turismo** un Excel, el **sistema de multas** un JSON, y el **registro de
contribuyentes** una base SQLite "que nadie se atreve a tocar".

> «Cuatro oficinas, cuatro formatos, un solo analista. Dame un lector para cada
> dialecto y moveré el informe mensual.» — Don Arquímedes

Construirás `fuentes.py`: lee las cuatro fuentes, registra un pago en la BD de
forma **transaccional** (commit/rollback), consolida los ingresos y los **exporta**
de vuelta en los cuatro formatos.

## Qué vas a aprender

Lectura con pandas: `read_csv` (y sus perillas `sep`/`decimal`/`thousands`),
`read_excel` (`sheet_name`, motor openpyxl), JSON por dos caminos (`json.load`
stdlib vs `pd.read_json`), `sqlite3` + `pd.read_sql` · **transacciones**:
`commit`, `rollback`, `IntegrityError`, patrón `with` · **exportación**:
`to_csv`/`to_excel`/`to_json`/`to_sql`.

## Dos rutas, un mismo verificador

| Ruta | Para quién | Qué haces |
|------|------------|-----------|
| 🛠️ **Artesano** | Quiero escribir el código | Completas los 6 `TODO` de `plantillas/fuentes.py`. |
| 🔎 **Explorador** | Quiero entender leyendo y probando | Ejecutas `soluciones/fuentes.py`, con las demos de la Guía 4 y la modificación de la Pregunta 5. |

## La regla de la casa (sobre la IA) 🤖

La IA está **invitada**: que te explique las transacciones o ACID. Pero el
interrogatorio pregunta por lo que pasó en **TU** terminal (tu boleta sin timbre,
tu rollback, tu `json.load`): eso se entiende, no se copia.

## Regla de oro de este lab

🔒 **`datos/fuentes/` es de SOLO LECTURA.** Nunca escribas ahí. Todo lo que
produzcas va a `salidas/` (incluida la copia de trabajo de la BD). Los datos
originales son sagrados.

## Prerrequisitos

- **`uv`** (trae Python 3.13). Instalación:
  [`../../docs/setup-alumno.md`](../../docs/setup-alumno.md).
- **Internet** la primera vez (el preparador descarga openpyxl).
- Se recomienda haber hecho los Labs 01–03.

Problemas de dependencias/binarios/BD:
[`docs/troubleshooting.md`](docs/troubleshooting.md).

## Mapa de las guías

1. **[Guía 1 — Cuatro dialectos](guia/01-contexto.md)** — entorno, las 4 fuentes,
   "un archivo es bytes con formato".
2. **[Guía 2 — CSV y Excel](guia/02-csv-y-excel.md)** — `read_csv`, el ritual de
   inspección, `read_excel` + `sheet_name`.
3. **[Guía 3 — JSON](guia/03-json.md)** — los dos caminos (`json.load` vs
   `read_json`) y el `JSONDecodeError`.
4. **[Guía 4 — Base de datos](guia/04-base-de-datos.md)** — `sqlite3`,
   `read_sql` y el tema estrella: **transacciones** (commit/rollback).
5. **[Guía 5 — El consolidado](guia/05-consolidado.md)** — construir/ejecutar
   `fuentes.py`, exportar y verificar.

## Verifica tu trabajo

Desde la raíz del lab (`labs/lab-04-cuatro-fuentes/`):

```bash
uv run python bin/verificar.py
```

Meta: `✔ 12/12 verificaciones correctas`. El verificador es de **solo lectura**
(trabaja sobre COPIAS, jamás sobre `datos/fuentes/`), prueba con **fuentes
sorpresa** en un directorio temporal, valida la transacción de verdad (rollback
incluido) y neutraliza cualquier `breakpoint()` olvidado.

## Para el instructor 🧑‍🏫

- **Reconstruir las fuentes** (determinista, bytes idénticos):
  `uv run python bin/generar_fuentes.py`.
- **Recuperar a un rezagado:** `uv run python bin/recuperar_lab.py` (regenera
  fuentes + repone `fuentes.py` y `salidas/`, interrogatorio en blanco).
- **Cifras de control:** pagos 12/$677.500 · permisos 8/$1.000.000 · multas
  10/$395.000 · contribuyentes 10 · **gran total $2.072.500**.
- **Dependencias:** `numpy==2.5.0`, `pandas==3.0.3`, `openpyxl==3.1.5`
  (`uv.lock` versionado). SQLite es stdlib.
- `datos/fuentes/` se versiona (bytes deterministas). `bin/generar_fuentes.py`
  es la única herramienta que escribe ahí; para el alumno son solo lectura.
- `bin/` solo lectura sobre el trabajo del alumno (salvo `recuperar_lab.py` y
  `generar_fuentes.py`); sin `breakpoint()` en soluciones/plantillas/bin (C8).
