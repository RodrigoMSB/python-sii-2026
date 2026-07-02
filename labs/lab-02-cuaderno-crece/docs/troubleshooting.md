# Troubleshooting — Lab 02 🩺

> Guía de urgencias. Busca tu síntoma, aplica la cura, vuelve al trabajo.
> Carriles 🍎 (macOS/Linux) y 🪟 (Windows) para lo específico de cada sistema.

## La técnica universal (léela primero)

Cuando algo falle, Python imprime un **traceback**. **Léelo de abajo hacia
arriba**: la **última línea** dice el tipo de error y el mensaje. Casi siempre
esa línea te dice qué arreglar.

---

## Instalar `uv`

### 🍎 macOS / Linux
```bash
brew install uv
# o, sin Homebrew:
curl -LsSf https://astral.sh/uv/install.sh | sh
```
Cierra y reabre la terminal. Verifica con `uv --version`.

### 🪟 Windows (PowerShell)
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Cierra y reabre PowerShell. Verifica con `uv --version`.

---

## Síntomas frecuentes

### El programa se quedó "pegado" y no responde — un `breakpoint()` olvidado

Si ejecutaste `consolidar.py` (o el verificador) y quedó detenido mostrando un
prompt `(Pdb)` o simplemente sin volver, casi seguro dejaste un `breakpoint()` de
la sesión de la Guía 5.

- Si ves el prompt `(Pdb)`: escribe **`c`** (continuar) y Enter hasta que termine,
  o **`q`** (quitar) y Enter para abortar.
- Luego **borra la línea `breakpoint()`** de tu `consolidar.py` (contrato C8).
- El verificador NO se cuelga si detecta un breakpoint (lo neutraliza y te avisa),
  pero igual debes quitarlo antes de entregar.

### `ModuleNotFoundError: No module named 'datos'`

Estás ejecutando `consolidar.py` desde —o ubicado en— la **carpeta equivocada**.
Python busca `datos/` junto al script que ejecuta; si el `consolidar.py` que corres
no está en la **raíz del lab**, no lo encuentra.

**Reproducir el síntoma:**
```bash
cp soluciones/consolidar.py guia/consolidar.py
cd guia
uv run python consolidar.py
#   ModuleNotFoundError: No module named 'datos'
```
**Cura:** ejecuta el `consolidar.py` de la **raíz**, parado en la raíz:
```bash
cd ..                          # volver a la raíz del lab
rm guia/consolidar.py          # borra la copia mal ubicada (🪟 Remove-Item guia\consolidar.py)
uv run python consolidar.py    # datos/ está justo al lado
```

### `KeyError: '...'`

Pediste una clave que no existe en un diccionario usando corchetes `[]`. **Cura:**
usa `.get(clave)` (devuelve `None`) o `.get(clave, valor_por_defecto)` cuando la
ausencia de la clave sea algo esperable, no un error.

### `ValueError: invalid literal for int() ...`

Intentaste `int()` sobre algo que no es número (p. ej. `"S/I"` o una deuda con
puntos sin limpiar). **Cura:** quita los puntos con `.replace(".", "")` antes de
`int()`, y envuelve la conversión en `try/except` para relanzar como
`RegistroInvalido` los casos ilegibles (Guía 4).

### El verificador dice que falta `consolidar.py`

Aún no lo copiaste a la raíz:
```bash
cp plantillas/consolidar.py consolidar.py    # 🛠️ Artesano   (🪟 Copy-Item plantillas\consolidar.py consolidar.py)
cp soluciones/consolidar.py consolidar.py    # 🔎 Explorador  (🪟 Copy-Item soluciones\consolidar.py consolidar.py)
```

### El informe está "desactualizado" (deuda incorrecta)

`salidas/informe_consolidacion.txt` quedó de una corrida anterior. **Cura:**
```bash
uv run python consolidar.py
```

### `SyntaxError` que "apunta una línea de más"

Suele señalar la línea **siguiente** a la del problema. Mira también la anterior:
casi siempre falta un **`:`** al final de un `def`/`if`/`for`/`try`, o un
paréntesis/comilla sin cerrar.

### `IndentationError`

Sangrías mezcladas o bloque sin indentar. Usa siempre **4 espacios** (no tabs).

### 🍎 `zsh: command not found: uv` tras instalar

Recarga el PATH: cierra y reabre la terminal, o `source ~/.zshrc`.

### 🪟 `... la ejecución de scripts está deshabilitada`

ExecutionPolicy bloqueando el `.ps1`. **Cura:**
```powershell
powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
```

### 🪟 `uv : El término 'uv' no se reconoce...`

PowerShell no ve `uv`. Cierra y reabre PowerShell (o reinicia sesión). Usa Windows
Terminal / PowerShell 7.

### 🪟 Acentos rotos (`Ã±`, cuadraditos)

Consola sin UTF-8. Usa **Windows Terminal**, o `chcp 65001` antes de ejecutar.

### El antivirus "retiene" `uv` o el entorno

Vuelve a correr el preparador; si insiste, pide una excepción para la carpeta del
curso y avisa al instructor.

---

## Si nada de esto calza

Copia la **última línea** del error y pídele ayuda a una IA o al instructor con
ese texto exacto. De abajo hacia arriba, siempre.
