# Troubleshooting — Lab 03 🩺

> Busca tu síntoma, aplica la cura, vuelve al trabajo. Carriles 🍎 (macOS/Linux)
> y 🪟 (Windows) para lo específico de cada sistema.

## La técnica universal

Lee el traceback **de abajo hacia arriba**: la última línea dice el tipo de error
y el mensaje.

---

## Instalar `uv`

### 🍎 macOS / Linux
```bash
brew install uv
# o: curl -LsSf https://astral.sh/uv/install.sh | sh
```
### 🪟 Windows (PowerShell)
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Cierra y reabre la terminal. Verifica con `uv --version`.

---

## Síntomas específicos de este lab (numpy / pandas)

### `uv sync` va lento o falla la PRIMERA vez

Este lab descarga numpy y pandas (unos MB). La primera vez necesita **Internet**.
- **Lento:** es normal la primera vez; luego queda cacheado y es instantáneo.
- **Falla por red/proxy:** si estás tras un proxy corporativo, puede bloquear la
  descarga. Reintenta `bash bin/00-preparar.sh`; si insiste, pide a soporte
  acceso a `pypi.org` / `files.pythonhosted.org`.
- **Antivirus:** algunos antivirus "retienen" los archivos `.whl` recién bajados.
  Reintenta; si persiste, pide una excepción para la carpeta del curso.

### `ModuleNotFoundError: No module named 'numpy'` (o 'pandas')

Casi siempre significa que ejecutaste con el **Python del sistema** en vez del
entorno del lab. La cura es el mantra del curso: **antepón `uv run`**.
```bash
uv run python panorama.py          # ✅ usa el entorno con numpy/pandas
python panorama.py                 # ❌ usa el Python del sistema, sin numpy
```
Si aun con `uv run` falla, el entorno no se creó bien: corre `bash bin/00-preparar.sh`.

### `ValueError: The truth value of an array ... is ambiguous`

Usaste `and`/`or` entre dos arrays de NumPy. **Cura:** combina máscaras con
`&` (y), `|` (o), `~` (no), y **envuelve cada condición en paréntesis**:
```python
(turismo > 500_000) & (comercio > 4_000_000)     # ✅
(turismo > 500_000) and (comercio > 4_000_000)   # ❌ ambiguo
```

### Mi `dtypes` dice `str` pero el tutorial muestra `object`

No es un error. pandas 3.0 (el que usa este lab) muestra las columnas de texto
como `str`; los tutoriales de pandas 2 muestran `object`. Es el mismo texto, tipo
nuevo. Puedes ignorar la diferencia.

### `KeyError: 'Estado'` (u otra columna)

Escribiste mal el nombre de una columna. Las mayúsculas importan: la columna es
`estado`, no `Estado`. Revisa `df.columns` para ver los nombres exactos.

### El programa se quedó "pegado" — un `breakpoint()` olvidado

Si dejaste un `breakpoint()` de alguna prueba, el programa se detiene en `(Pdb)`.
Escribe `c` (continuar) o `q` (salir) y Enter, y **borra la línea**. El
verificador no se cuelga si detecta uno (lo neutraliza y avisa).

> 💾 Nota tranquilizadora: en este lab los datos son diminutos; **no** verás
> `Killed`/`MemoryError`. Los arreglos gigantes que llenan la RAM son cosa del
> curso avanzado. 😄

---

## Síntomas de siempre

### `ModuleNotFoundError: No module named 'datos'`

Ejecutaste `panorama.py` desde/ubicado en la carpeta equivocada. Corre el de la
**raíz del lab**, parado en la raíz:
```bash
cp soluciones/panorama.py guia/panorama.py && cd guia && uv run python panorama.py
#   ModuleNotFoundError: No module named 'datos'
cd .. && rm guia/panorama.py && uv run python panorama.py   # cura
```

### El verificador dice que falta `panorama.py`

Cópialo a la raíz: `cp plantillas/panorama.py panorama.py` (Artesano) o
`cp soluciones/panorama.py panorama.py` (Explorador).

### El informe está "desactualizado"

Reejecuta `uv run python panorama.py` para regenerar `salidas/informe_panorama.txt`.

### `SyntaxError` / `IndentationError`

El `SyntaxError` suele apuntar la línea siguiente al problema (revisa `:` y
paréntesis/comillas). Para la sangría, usa siempre 4 espacios (no tabs).

### 🪟 ExecutionPolicy / `uv` no reconocido / acentos rotos

- `... ejecución de scripts está deshabilitada` → usa
  `powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1`.
- `uv no se reconoce` → cierra y reabre PowerShell (o reinicia sesión).
- Acentos raros → usa Windows Terminal o `chcp 65001`.

---

## Nota del constructor (H-03)

La versión de pandas del lab es **3.0.3**, no 3.0.4. La 3.0.4 fue **retirada de
PyPI** (*yank*) por reportes de segfaults en funcionalidad de fechas —que este
lab no usa—, así que se fijó la 3.0.3, la última 3.0.x estable. Si ves tutoriales
que mencionan 3.0.4, no te preocupes: para lo que hacemos aquí son idénticas.

---

## Si nada calza

Copia la última línea del error y pídele ayuda a una IA o al instructor con ese
texto exacto. De abajo hacia arriba, siempre.
