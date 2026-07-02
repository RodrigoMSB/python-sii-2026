# Troubleshooting — Lab 04 🩺

> Busca tu síntoma, aplica la cura, vuelve al trabajo. Carriles 🍎 (macOS/Linux)
> y 🪟 (Windows) para lo específico de cada sistema.

## La técnica universal

Lee el traceback **de abajo hacia arriba**: la última línea dice el tipo de error
y el mensaje.

---

## Instalar `uv`

### 🍎 macOS / Linux
```bash
brew install uv      # o: curl -LsSf https://astral.sh/uv/install.sh | sh
```
### 🪟 Windows (PowerShell)
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Cierra y reabre la terminal. Verifica con `uv --version`.

---

## Síntomas específicos de este lab

### `ImportError: Missing optional dependency 'openpyxl'`

pandas necesita openpyxl para leer/escribir `.xlsx`, y no lo encontró: casi
siempre porque corriste con el Python del sistema. **Cura:** antepón `uv run`:
```bash
uv run python fuentes.py     # ✅   (no: python fuentes.py)
```
Si con `uv run` sigue, corre el preparador: `bash bin/00-preparar.sh`.

### Abrí el `.xlsx` o el `.db` con un editor y veo "basura"

Es lo esperado: **no son texto**. Un `.xlsx` es un ZIP de XML; un `.db` es un
binario de SQLite. Ábrelos con la herramienta correcta: pandas/openpyxl para el
Excel, `sqlite3` (o `pd.read_sql`) para la base. Verlos como bytes es la lección
de la Guía 1, no un error.

### `sqlite3.OperationalError: database is locked`

Quedó una conexión abierta (un REPL o script colgado sujetando la BD). **Cura:**
cierra ese REPL/terminal, o asegúrate de llamar `con.close()` (o usar
`with sqlite3.connect(...)`). El contrato C11 existe justo por esto: nunca dejes
una conexión abierta.

### 🪟 No puedo re-ejecutar: el `.xlsx` está "en uso"

Si tienes `salidas/resumen.xlsx` **abierto en Excel** y vuelves a correr
`fuentes.py`, Windows bloquea el archivo y la exportación falla (`Permission
denied`). **Cura:** cierra el Excel antes de re-ejecutar.

### `json.decoder.JSONDecodeError: Expecting ...`

El JSON tiene un error de sintaxis (una coma de más, una llave sin cerrar). El
mensaje te da **línea y columna** exactas: ve ahí y corrige. Si rompiste una
copia en `salidas/`, puedes regenerar la fuente original con
`uv run python bin/generar_fuentes.py` (aunque la original no se tocó).

### `UnicodeDecodeError` al leer un CSV

El CSV no está en la codificación que pandas asumió. Los nuestros son UTF-8
(`encoding="utf-8"`); un CSV ajeno podría venir en otra (p. ej. `latin-1`).
**Cura:** prueba la perilla `encoding=`: `pd.read_csv(ruta, encoding="latin-1")`.

### Falta una fuente (`datos/fuentes/...`)

El verificador de entorno te lo dirá. **Cura:** reconstrúyelas con la imprenta:
```bash
uv run python bin/generar_fuentes.py
```
Es determinista: reconstruye las cuatro idénticas a las originales.

---

## Síntomas de siempre

### `ModuleNotFoundError: No module named 'datos'` / no encuentra las fuentes

Ejecutaste `fuentes.py` desde/ubicado en la carpeta equivocada. Corre el de la
**raíz del lab**, parado en la raíz:
```bash
cp soluciones/fuentes.py guia/fuentes.py && cd guia && uv run python fuentes.py
#   error: no encuentra datos/fuentes/...
cd .. && rm guia/fuentes.py && uv run python fuentes.py   # cura
```

### El verificador dice que falta `fuentes.py`

Cópialo a la raíz: `cp plantillas/fuentes.py fuentes.py` (Artesano) o
`cp soluciones/fuentes.py fuentes.py` (Explorador).

### `SyntaxError` / `IndentationError`

El `SyntaxError` suele apuntar la línea siguiente al problema (revisa `:`,
paréntesis, comillas). Sangría: 4 espacios, no tabs.

### El programa se quedó "pegado" — un `breakpoint()` olvidado

Escribe `c` o `q` y Enter, y borra la línea. El verificador no se cuelga si
detecta uno (lo neutraliza y avisa).

### 🪟 ExecutionPolicy / `uv` no reconocido / acentos rotos

- `... ejecución de scripts está deshabilitada` →
  `powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1`.
- `uv no se reconoce` → cierra y reabre PowerShell.
- Acentos raros → Windows Terminal o `chcp 65001`.

---

## Si nada calza

Copia la última línea del error y pídele ayuda a una IA o al instructor con ese
texto exacto. De abajo hacia arriba, siempre.
