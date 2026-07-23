# Troubleshooting — Capstone El Arenario 🩺

> El capstone integra los 6 labs, así que hereda todos sus síntomas. Aquí los más
> probables. Busca, cura, sigue contando.

## La técnica universal

Lee el traceback **de abajo hacia arriba**: la última línea dice el tipo de error.

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

## Síntomas del capstone

### Mi censo depurado NO tiene 27 filas

Repasa las reglas oficiales (ESCENARIO.md): dedup exacto (gana el primero), filtrar
solo `PS-####-Y`, imputar faltantes a 0, y apartar outliers **solo por consenso**
(IQR ∩ z-score, no la unión). Si apartas por IQR solo, botas a Buceo Fondo Claro y
te queda 26. Si no apartas nada, te quedan 28.

### La columna `deuda` quedó como texto / hay filas raras

El censo trae faltantes escritos de **tres** formas: vacío, `S/I` y **`s/d`**
(minúscula). `s/d` NO es un marcador NA por defecto de pandas: decláralos todos en
`na_values=["", "S/I", "s/d"]`. (Doctrina H-05: el marcador desconocido es `s/d`.)

### Solo leo una parte de los pagos

El Excel tiene **dos hojas**: `S1` y `S2`. Con `read_excel(ruta)` sin más, lees solo
la primera. Usa `sheet_name=None` (te da un dict con todas) o `sheet_name=["S1","S2"]`,
y apílalas con `concat`.

### `MergeError: Merge keys are not unique`

El `validate="1:1"` haciendo su trabajo: estás uniendo con pagos/multas **sin
agrupar** por código. Agrupa primero (`groupby("codigo")["monto"].sum()`) para tener
una fila por contribuyente, y luego une.

### El saldo no me da $990.000

El saldo del año incluye las **multas**: `saldo = deuda + multas − pagado` (no solo
deuda − pagado). Y las multas/pagos huérfanos NO entran al tablero (sus códigos no
están en el censo depurado).

### Me salen saldos negativos — ¿está mal?

**No.** Es el hallazgo del año. Hay dos causas: sobrepagos (pagaron en ambos
semestres) y la imputación a 0 (a quien tenía deuda `S/I` se le imputó 0 y su pago
lo dejó en negativo). Detéctalos, explícalos en la sección "Hallazgos" del informe y
en la BITÁCORA. El examen premia verlos, no esconderlos.

### El PNG pesa 0 bytes o el script "se cuelga" al graficar

`matplotlib.use("Agg")` ANTES de importar pyplot; guarda con `savefig`; `close`
siempre; nunca `plt.show()` en el script (C16). El PNG debe pesar > 5 KB y empezar
con la firma `PNG`.

### Falta una fuente / alteré un CSV / se corrompió el xlsx

- CSV/JSON (texto, versionados): `git checkout -- datos/censo_anual.csv datos/multas.json`.
- xlsx/db (binarios, generados): `uv run python bin/generar_fuentes.py` (repone lo
  que falte). Si uno está **corrupto pero presente**, bórralo y regenera (H-04).

### `FileNotFoundError` de una fuente

Ejecuta tu script parado en la **raíz del capstone** (busca `datos/` relativo al
script). Si lo corriste desde otra carpeta, vuelve a la raíz.

### `breakpoint()` olvidado

Escribe `c` o `q` y Enter, y bórralo. El verificador (que mide productos) no lo
ejecuta, pero tu script sí se cuelga.

---

## Si nada calza

Copia la última línea del error y pídele ayuda a una IA o al relator con ese texto
exacto. Y recuerda las pistas graduadas en `pistas/`.
