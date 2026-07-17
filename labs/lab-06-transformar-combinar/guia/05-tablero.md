# Guía 5 — El tablero

> **Objetivo:** encadenar todo en `tablero.py`, dibujar el gráfico del Concejo con
> matplotlib y pasar el verificador.

## Matplotlib mínimo viable (y headless)

Un gráfico de barras en cinco líneas:

```python
import matplotlib
matplotlib.use("Agg")            # ⚠️ ANTES de importar pyplot
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4.5))    # una figura y sus ejes
ax.bar(["Comercio", "Gastronomía", "Turismo"], [601000, 99000, 1325000])
ax.set_title("Saldo por rubro — Puerto Siracusa")
ax.set_xlabel("Rubro"); ax.set_ylabel("Saldo pendiente (CLP)")
fig.tight_layout()               # que no se corten las etiquetas
from pathlib import Path
Path("salidas").mkdir(exist_ok=True)   # la carpeta puede no existir aún
fig.savefig("salidas/saldo_por_rubro.png", dpi=150)
plt.close(fig)                    # cerrar SIEMPRE
```

> 🖥️ **Contrato C16 — por qué `Agg` y jamás `plt.show()` en un script.**
> `matplotlib.use("Agg")` elige un backend **sin ventanas** (headless): dibuja a un
> archivo, no a pantalla. En un script (o en el verificador, o en un servidor sin
> monitor) `plt.show()` intentaría **abrir una ventana** — y ahí se cuelga, o falla,
> o abre algo que nadie ve. La regla: en un script, el gráfico **se guarda con
> `savefig`**; `plt.show()` es solo para explorar en vivo (un Jupyter). Y `close`
> siempre, para no acumular figuras en memoria.

## Elige tu ruta

El programa se llama `tablero.py`. Copia el archivo a la raíz del lab.

### 🛠️ Ruta Artesano
```bash
cp plantillas/tablero.py tablero.py          # macOS/Linux
```
```powershell
Copy-Item plantillas\tablero.py tablero.py   # Windows
```
Completa los **6 TODO** (rubro, tramo, concat, merge, transform, gráfico). ¿Trabado?
Mira SOLO esa función en `soluciones/tablero.py`.

### 🔎 Ruta Explorador
```bash
cp soluciones/tablero.py tablero.py          # macOS/Linux
```
```powershell
Copy-Item soluciones\tablero.py tablero.py   # Windows
```
Obligatorio: la modificación de la **Pregunta 5** (merge left → inner).

## Ejecuta el tablero

```bash
uv run python tablero.py
```

**Salida esperada (puede variar levemente):**

```
TABLERO DEL CONCEJO — Dirección de Rentas de Puerto Siracusa
==========================================================
Deuda total         : $3,107,500 CLP
Pagado total        : $1,082,500 CLP
Saldo pendiente     : $2,025,000 CLP
Sin pago alguno     : 9 contribuyentes

Contribuyentes por tramo de deuda:
  Sin deuda : 4
  Baja      : 11
  Media     : 7
  Alta      : 3

Saldo por rubro:
  Comercio    : deuda $881,000  pagado $280,000  saldo $601,000
  Gastronomía : deuda $697,500  pagado $598,500  saldo $99,000
  Turismo     : deuda $1,529,000  pagado $204,000  saldo $1,325,000

Pagos huérfanos (a investigar — pagaron pero no están en el censo):
  PS-1032-C: $83,000
  PS-1040-G: $47,500
  Total huérfano: $130,500 CLP

[INFO] Tablero, informe y gráfico en: .../salidas
```

## Mira tu trabajo

En `salidas/` quedaron cuatro cosas — ¡ábrelas!

```bash
ls salidas/
#   informe_tablero.txt  tablero.csv  tablero.xlsx  saldo_por_rubro.png
```

- `tablero.csv` / `tablero.xlsx` → el cuadro completo (25 filas con rubro, tramo,
  pagado, saldo).
- **`saldo_por_rubro.png`** → ábrelo con tu visor de imágenes. Ahí está el gráfico
  que el Concejo aprobará con los ojos. La satisfacción de **ver** tu trabajo.

## 🔧 La modificación obligatoria (Pregunta 5)

En `construir_tablero`, cambia el merge:

```python
    tablero = censo.merge(pagado, on="codigo", how="inner", validate="1:1")  # era "left"
```

Re-ejecuta y observa: ¿bajó el número de filas? ¿Qué pasó con el **saldo total** y
con los **contribuyentes sin pago**? (con `inner` desaparecen los 9 que no pagaron —
¡y con ellos, su deuda impaga!). Explica por qué `left` es lo correcto para un
tablero de **cobranza** (no puedes olvidarte de quien NO ha pagado) y **revierte**.

## Responde el interrogatorio y verifica

```bash
cp plantillas/RESPUESTAS.md RESPUESTAS.md          # macOS/Linux
```
```powershell
Copy-Item plantillas\RESPUESTAS.md RESPUESTAS.md   # Windows
```

Responde las 5 preguntas (varias piden lo que viste: el borde del tramo, las tres
uniones, los huérfanos). Luego:

```bash
uv run python bin/verificar.py
```

Meta: `✔ 14/14 verificaciones correctas`. El verificador prueba tu pipeline con
datos oficiales y **sorpresa**, y comprueba que el PNG existe y es válido.

## 🏅 Desafío extra (opcional): el gráfico del Concejo

Haz barras **apiladas** de la deuda por rubro y estado, usando el pivote
(`piv.plot(kind="bar", stacked=True)`). Solución en
[`../soluciones/desafio-grafico-concejo.md`](../soluciones/desafio-grafico-concejo.md).

## ✅ Checkpoint final del Lab 06

- [ ] Entendiste transformar (map/cut/dummies), combinar (concat/merge), agregar
      (groupby/transform/crosstab/pivot) y graficar (matplotlib Agg).
- [ ] Copiaste `tablero.py` a la raíz por tu ruta (🛠️ o 🔎).
- [ ] El informe muestra `$2,025,000` de saldo y los huérfanos ($130.500).
- [ ] Abriste el PNG y viste tu gráfico.
- [ ] Hiciste el experimento merge left→inner (Pregunta 5) y lo revertiste.
- [ ] Respondiste las 5 preguntas y el verificador dice `✔ 14/14`.

---

🎉 **¡Armaste el tablero del Concejo!** Transformaste, combinaste, agregaste y
graficaste: el pipeline completo de un analista de datos. Cruzaste lo que se debe
con lo que se pagó, encontraste plata huérfana y le diste al Concejo un gráfico que
no admite discusión.

> **Se acerca el capstone 🏖️:** el Concejo aprobó el tablero. Ahora Don Arquímedes
> quiere **TODO junto** — el informe anual del puerto, de cabo a rabo, con todo lo
> que aprendiste en seis labs. Se acerca **El Arenario**. Nos vemos en el mesón. ⚓
