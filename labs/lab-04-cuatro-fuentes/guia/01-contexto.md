# Guía 1 — Cuatro oficinas, cuatro dialectos

> **Objetivo:** montar el entorno, conocer las cuatro fuentes y aprender la
> lección del día: **un archivo es bytes con un formato**.

## El encargo

Don Arquímedes convocó a las oficinas a entregar sus datos del mes. Cada una
respondió en su propio idioma:

- **Tesorería** exportó un **CSV** de su sistema (`pagos.csv`).
- La **Oficina de Turismo** armó un **Excel** a mano (`permisos_eventos.xlsx`).
- El **sistema antiguo de multas** solo sabe escupir **JSON** (`multas.json`).
- El **registro de contribuyentes** vive en una **base SQLite**
  (`contribuyentes.db`) que nadie se atreve a tocar "porque una vez se borró algo".

> «Cuatro oficinas, cuatro formatos, un solo analista. Dame un lector para cada
> dialecto y moveré el informe mensual.» — Don Arquímedes

Hasta ahora los datos te llegaban cómodos, como módulos de Python. **En la vida
real llegan en archivos.** Este es el rito de paso.

## Montar el taller (descarga openpyxl la primera vez)

**macOS/Linux:**
```bash
cd labs/lab-04-cuatro-fuentes
bash bin/00-preparar.sh
```
**Windows:**
```powershell
cd labs\lab-04-cuatro-fuentes
powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
```

**Salida esperada (la primera vez descarga openpyxl):**
```
[OK] numpy 2.5.0 (correcto).
[OK] pandas 3.0.3 (correcto).
[OK] openpyxl 3.1.5 (correcto).
[OK] Las cuatro fuentes están en datos/fuentes/ (csv, xlsx, json, db).
✔ 9/9 verificaciones correctas
```

## La imprenta del lab: `generar_fuentes.py`

Los cuatro archivos de `datos/fuentes/` ya vienen listos en el repositorio, pero
también se pueden **reconstruir** desde su única fuente de verdad
(`datos/fuentes_semilla.py`) con:

```bash
uv run python bin/generar_fuentes.py
```

Piénsalo como **la imprenta del lab**: si un archivo se corrompe, la imprenta lo
vuelve a tirar, idéntico. (El recuperador la usa por dentro.)

> 🔒 **Regla de oro:** `datos/fuentes/` es de **SOLO LECTURA**. Nunca escribas ahí.
> Todo lo que TÚ produzcas —informe, exportaciones, copia de la BD— va a
> `salidas/`. Tratar las fuentes como intocables es un hábito profesional: los
> datos originales son sagrados.

## Un archivo es bytes con formato

Abre las cuatro fuentes con "herramientas humanas" y observa la diferencia.

**Las de texto se leen a ojo.** Ábrelas con tu editor, o desde la terminal:
```bash
cat datos/fuentes/pagos.csv        # 🍎/🐧  (Windows: type datos\fuentes\pagos.csv)
cat datos/fuentes/multas.json
```
Verás texto legible: comas y saltos de línea en el CSV, llaves y corchetes en el
JSON. **Son texto plano con reglas.**

### 💥 Rómpelo: mira un binario a los ojos

El `.xlsx` y el `.db` **no** son texto. Míralos igual y observa el desastre:
```bash
head -c 200 datos/fuentes/permisos_eventos.xlsx    # 🍎/🐧
head -c 200 datos/fuentes/contribuyentes.db
```
```powershell
Get-Content datos\fuentes\permisos_eventos.xlsx -TotalCount 1   # 🪟
```
Verás **basura**: símbolos raros, `PK...`, bytes ilegibles. No está roto: es que
un `.xlsx` es en realidad un **ZIP** de XML, y un `.db` es un formato **binario**
de SQLite. Un editor de texto no sabe leerlos; se necesita la herramienta
correcta (pandas/openpyxl para el xlsx, sqlite3 para el db).

**Esa es la lección del día:** un archivo es **bytes con un formato**. Elegir el
lector correcto para cada formato es, literalmente, el trabajo de este lab.

## ✅ Checkpoint

- [ ] El preparador terminó en `✔ 9/9` (incluye openpyxl y las 4 fuentes).
- [ ] Reconstruiste las fuentes con `generar_fuentes.py` (opcional).
- [ ] Abriste el CSV y el JSON como texto y los leíste.
- [ ] Miraste el xlsx/db "en crudo" y viste que son binarios.

Cuando esté todo ✔, sigue con **[Guía 2 — CSV y Excel](02-csv-y-excel.md)**.
