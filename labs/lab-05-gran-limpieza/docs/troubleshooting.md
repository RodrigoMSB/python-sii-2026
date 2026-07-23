# Troubleshooting — Lab 05 🩺

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

## Síntomas específicos de este lab

### "Mi filtro no encuentra las filas que debería"

Casi siempre es **texto sin homogeneizar**: `vigente`, `Vigente` y `vigente ` no
son `"VIGENTE"` para pandas. **Cura:** homogeneiza **primero**
(`.str.strip().str.upper()`) y **después** filtra. Un espacio o una mayúscula
hacen que un filtro cuente mal **sin avisar**.

### `deuda` quedó como texto (dtype `object`/`str`), no como número

Olvidaste `na_values`. Los faltantes venían como `S/I`, `sin dato` o celda vacía;
si pandas los lee como texto, mezcla números y strings y la columna deja de ser
numérica. **Cura:**
```python
pd.read_csv(ruta, na_values=["", "S/I", "sin dato"])
```
Así los tres marcadores se vuelven `NaN` y `deuda` queda `float64`.

### El `9999999` "desapareció" del `describe` después de imputar

No desapareció: `describe` muestra media y cuartiles, y con un solo valor gigante
el promedio te puede despistar. **Míralo directo:** `df["deuda"].max()` sigue
mostrando 9.999.999. La imputación rellena los **faltantes**, no toca los outliers.

### Mi regex "no calza" lo que esperaba

Recuerda la diferencia (Guía 3):
- `str.fullmatch(patrón)` exige que calce **todo** el string (para validar formato).
- `str.contains(patrón)` calza si el patrón aparece **en alguna parte** (para buscar).
Si validas formato con `contains`, se te cuelan códigos con basura extra. Usa
`fullmatch` para validar.

### Alteré el censo sin querer / el verificador dice que no tiene 30 filas

El censo es texto **versionado**: git es la fuente de verdad. **Cura:** restáuralo
```bash
git checkout -- datos/censo_patentes.csv
```
o corre `uv run python bin/recuperar_lab.py`, que lo restaura por ti.

### Veo un `FutureWarning` o algo sobre "copy" / vistas de pandas

pandas 3 usa **Copy-on-Write**: las "vistas" ya no mutan el DataFrame original de
forma sorpresiva (por eso en el lab cada función hace `df = df.copy()` — contrato
C13, y se siente natural). Si un tutorial viejo te muestra un
`SettingWithCopyWarning`, es de la era anterior; con la API moderna del lab no
deberías toparte con él.

---

## Síntomas de siempre

### `FileNotFoundError: ... datos/censo_patentes.csv`

Ejecutaste `limpiar.py` desde/ubicado en la carpeta equivocada (busca el censo
relativo al script). Corre el de la **raíz del lab**, parado en la raíz:
```bash
cp soluciones/limpiar.py guia/limpiar.py && cd guia && uv run python limpiar.py
#   FileNotFoundError: ... guia/datos/censo_patentes.csv
cd .. && rm guia/limpiar.py && uv run python limpiar.py   # cura
```

### El verificador dice que falta `limpiar.py`

Cópialo a la raíz: `cp plantillas/limpiar.py limpiar.py` (Artesano) o
`cp soluciones/limpiar.py limpiar.py` (Explorador).

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
