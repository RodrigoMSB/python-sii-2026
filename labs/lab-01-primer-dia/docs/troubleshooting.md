# Troubleshooting — Lab 01 🩺

> Guía de urgencias. Busca tu síntoma, aplica la cura, vuelve al trabajo.
> Los carriles 🍎 (macOS/Linux) y 🪟 (Windows) marcan lo específico de cada SO.

## La técnica universal (léela primero)

Cuando algo falle, Python imprime un **traceback**. **Léelo de abajo hacia
arriba**: la **última línea** dice el **tipo de error** y el mensaje; las de
arriba solo cuentan cómo se llegó ahí. El 90% de las veces, esa última línea te
dice exactamente qué arreglar.

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

### `invalid peer certificate: UnknownIssuer` al preparar el lab

Ocurre en redes corporativas que inspeccionan el tráfico HTTPS (es el caso de la
red del SII). `uv` no reconoce el certificado de la institución y aborta la
descarga de Python 3.13.

Los scripts del curso ya traen la cura aplicada. Si aun así lo ves —por ejemplo,
corriendo `uv` a mano fuera de los scripts—, activa la variable:

```bash
export UV_NATIVE_TLS=1          # 🍎 macOS / 🪟 Git Bash
```
```powershell
$env:UV_NATIVE_TLS = "1"        # 🪟 PowerShell
```

Para dejarlo permanente en Git Bash:
```bash
printf '\nexport UV_NATIVE_TLS=1\n' >> ~/.bashrc
source ~/.bashrc
```
> ⚠️ Ese `printf` se corre **en Git Bash, nunca en PowerShell**: PowerShell
> escribe el archivo en UTF-16 y lo corrompe, produciendo
> `bash: $'\377\376export': command not found`. Si ya ocurrió, borra el archivo
> (`rm ~/.bashrc`) y vuelve a escribirlo desde Git Bash.

---

## Síntomas frecuentes

### `ModuleNotFoundError: No module named 'datos'`

**Qué significa:** Python no encontró el paquete `datos/` (el cuaderno). Esto
pasa cuando ejecutas `triaje.py` desde —o ubicado en— la **carpeta equivocada**.
Python busca `datos/` junto al script que ejecuta; si el `triaje.py` que corres
no está en la **raíz del lab** (donde vive `datos/`), no lo encuentra.

Casos típicos:
- Copiaste o creaste `triaje.py` **dentro** de otra carpeta (por ejemplo `guia/`)
  y lo ejecutaste ahí. Como junto a `guia/` no hay ninguna carpeta `datos/`, falla.
- Estás corriendo el archivo desde un editor/IDE configurado con otra carpeta de
  trabajo.

**Reproducir el síntoma (para que lo reconozcas):**
```bash
# parado en la raíz del lab, "escondemos" una copia en guia/ y la corremos ahí
cp soluciones/triaje.py guia/triaje.py
cd guia
uv run python triaje.py
#   ...
#   ModuleNotFoundError: No module named 'datos'
```

**Cura:** ejecuta el triaje que está en la **raíz del lab**, parado en la raíz:
```bash
cd ..                       # volver a la raíz del lab (labs/lab-01-primer-dia/)
rm guia/triaje.py           # borra la copia mal ubicada (Windows: Remove-Item guia\triaje.py)
uv run python triaje.py     # ahora sí: datos/ está justo al lado
```
> 🧭 **Regla de oro:** `triaje.py` vive en la **raíz del lab**, y todos los
> comandos se corren desde ahí. Si dudas, `ls` (🍎) o `dir` (🪟) y confirma que
> ves `triaje.py` y la carpeta `datos/` juntos.

### El verificador dice que falta `triaje.py`

Aún no lo copiaste a la raíz. Elige tu ruta:
```bash
cp plantillas/triaje.py triaje.py    # 🛠️ Artesano   (🪟 Copy-Item plantillas\triaje.py triaje.py)
cp soluciones/triaje.py triaje.py    # 🔎 Explorador  (🪟 Copy-Item soluciones\triaje.py triaje.py)
```

### El informe está "desactualizado" (deuda incorrecta)

El verificador lee `salidas/informe_triaje.txt`, que se generó en una ejecución
**anterior** (quizá con un bug ya corregido). **Cura:** vuelve a ejecutar el
triaje para regenerarlo:
```bash
uv run python triaje.py
```

### `SyntaxError` que "apunta una línea de más"

Un `SyntaxError` suele señalar la línea **siguiente** a la del problema real. Si
te marca la línea 34, mira también la **33**: casi siempre falta ahí un **`:`**
al final de un `if`/`for`/`def`, o un paréntesis/comilla sin cerrar.

### `IndentationError`

Mezclaste sangrías o te faltó indentar el bloque de un `if`/`for`. En Python la
indentación es sintaxis. **Cura:** usa siempre **4 espacios** (no tabs) y asegura
que todo lo que va "dentro" de un `if`/`for` esté sangrado de forma pareja. Si tu
editor mezcla tabs y espacios, actívale "mostrar espacios en blanco".

### 🍎 `zsh: command not found: uv` justo después de instalar

La terminal no ha recargado el PATH. **Cura:** cierra y reabre la terminal, o
```bash
source ~/.zshrc
```
Si persiste, confirma que el instalador dejó `uv` en `~/.local/bin` y que esa
ruta está en tu PATH.

### 🪟 `... no se puede cargar porque la ejecución de scripts está deshabilitada`

Es la **ExecutionPolicy** de PowerShell bloqueando el `.ps1`. **Cura:** invoca el
preparador saltándola solo para esa ejecución:
```powershell
powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
```

### 🪟 `uv : El término 'uv' no se reconoce...`

PowerShell no ve `uv` en el PATH (común tras instalar en una sesión vieja).
**Cura:** cierra y reabre PowerShell. Si sigue, reinicia sesión de Windows. Usa
una terminal moderna (Windows Terminal / PowerShell 7), no una ventana abierta
desde antes de instalar.

### 🪟 Acentos rotos (`Ã±`, `?`, cuadraditos) en la consola

La consola no está en UTF-8. **Cura:** usa **Windows Terminal** (ya viene en
UTF-8), o en `cmd`/PowerShell fuerza la página de códigos antes de ejecutar:
```powershell
chcp 65001
```

### El antivirus "retiene" o borra `uv`/el entorno

Algunos antivirus corporativos ponen en cuarentena binarios recién descargados o
bloquean la creación de `.venv/`. **Cura:** vuelve a correr el preparador; si
insiste, pide a soporte que agregue una excepción para la carpeta del curso y
para `uv`. Anótalo y avísale al instructor.

---

## Si nada de esto calza

Copia la **última línea** del error y pídele ayuda a una IA o al instructor con
ese texto exacto. Recuerda: abajo hacia arriba, siempre.
