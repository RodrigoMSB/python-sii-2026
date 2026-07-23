# Troubleshooting — Lab 06 🩺

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

## Síntomas específicos de este lab (matplotlib y combinación)

### `uv sync` va lento la primera vez

matplotlib es la biblioteca más pesada del curso (arrastra fuentes y otras
dependencias). La primera sincronización tarda unos segundos más; luego queda en
caché. Es normal, ten paciencia.

### El script "se queda pegado" al graficar

Casi seguro usaste `plt.show()` en el script. `show()` intenta abrir una **ventana**
y, en una terminal sin interfaz gráfica, se cuelga (o en Windows abre algo que
nadie ve). **Cura (contrato C16):** en un script, elige el backend headless y guarda
a archivo, nunca muestres:
```python
import matplotlib
matplotlib.use("Agg")        # ANTES de importar pyplot
import matplotlib.pyplot as plt
...
fig.savefig("salidas/grafico.png", dpi=150)
plt.close(fig)               # jamás plt.show() en un script
```

### El PNG pesa 0 bytes o sale vacío

Dos causas comunes: llamaste `savefig` **después** de `plt.close()` (ya no hay
figura), o graficaste sobre unos ejes vacíos. **Cura:** el orden es `bar/plot →
set_title/labels → tight_layout → savefig → close`, en ese orden.

### Warnings de "glyph"/fuentes en el PNG

Si ves un `UserWarning` sobre un carácter que la fuente no tiene (algún acento o
símbolo raro), es **cosmético**: el PNG se genera igual. Usa los textos provistos
en la solución y no te preocupes por esos avisos.

### `MergeError: Merge keys are not unique ...`

Es el `validate="1:1"` haciendo su trabajo: intentaste unir con una tabla que tiene
códigos repetidos (p. ej. pagos sin agrupar, donde alguien pagó en junio y julio).
**Cura:** agrupa los pagos por código **antes** de unir
(`groupby("codigo")["monto"].sum()`), así queda una fila por contribuyente y el
merge es 1:1.

### Después de `cut`, algunas filas quedan en tramo `NaN`

Un valor cayó **fuera** de los bins. Revisa que el bin más bajo cubra el mínimo
(por eso usamos `-1` como primer borde, para incluir el 0) y el más alto cubra el
máximo. Un `NaN` en `tramo` = un valor sin clasificar.

### Los tramos de `cut` "no se ordenan" como quiero

Las categorías de `cut` son **categóricas ordenadas**: usa `.value_counts().sort_index()`
para verlas en el orden Sin deuda → Baja → Media → Alta (y no por frecuencia).

---

## Síntomas de siempre

### `FileNotFoundError: ... datos/...csv`

Ejecutaste `tablero.py` desde/ubicado en la carpeta equivocada. Corre el de la
**raíz del lab**, parado en la raíz:
```bash
cp soluciones/tablero.py guia/tablero.py && cd guia && uv run python tablero.py
#   FileNotFoundError: ... guia/datos/censo_limpio.csv
cd .. && rm guia/tablero.py && uv run python tablero.py   # cura
```

### El verificador dice que falta `tablero.py`

Cópialo a la raíz: `cp plantillas/tablero.py tablero.py` (Artesano) o
`cp soluciones/tablero.py tablero.py` (Explorador).

### Alteré un CSV / el verificador dice que no tiene las filas correctas

Los CSV son texto versionado: git es la fuente de verdad.
```bash
git checkout -- datos/censo_limpio.csv datos/pagos_junio.csv datos/pagos_julio.csv
```
o corre `uv run python bin/recuperar_lab.py`.

### `SyntaxError` / `IndentationError` / `breakpoint()` olvidado

El `SyntaxError` suele apuntar la línea siguiente al problema. El `breakpoint()`:
escribe `c` o `q` y Enter, y bórralo (el verificador no se cuelga si lo detecta).

### 🪟 ExecutionPolicy / `uv` no reconocido / acentos rotos

- `... ejecución de scripts está deshabilitada` →
  `powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1`.
- `uv no se reconoce` → cierra y reabre PowerShell.
- Acentos raros → Windows Terminal o `chcp 65001`.

---

## Si nada calza

Copia la última línea del error y pídele ayuda a una IA o al instructor con ese
texto exacto. De abajo hacia arriba, siempre.
