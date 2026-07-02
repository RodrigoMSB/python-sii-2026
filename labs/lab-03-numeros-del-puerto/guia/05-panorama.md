# Guía 5 — El panorama

> **Objetivo:** juntar NumPy y pandas para construir `panorama.py`, el informe
> que Don Arquímedes llevará al Concejo, y pasar el verificador.

## Elige tu ruta

El programa se llama `panorama.py`. Copia el archivo a la raíz del lab.

### 🛠️ Ruta Artesano — completas los TODO

```bash
cp plantillas/panorama.py panorama.py          # macOS/Linux
```
```powershell
Copy-Item plantillas\panorama.py panorama.py   # Windows
```
Completa los **6 TODO** en orden. Cada uno es una de las operaciones que ya
practicaste en las guías: `sum(axis=...)`, `argmax`, máscara booleana, filtrado
de DataFrame y f-strings. Tras cada TODO, ejecuta `uv run python panorama.py`.
¿Trabado? Mira SOLO esa función en `soluciones/panorama.py`.

### 🔎 Ruta Explorador — ejecutas y experimentas

```bash
cp soluciones/panorama.py panorama.py          # macOS/Linux
```
```powershell
Copy-Item soluciones\panorama.py panorama.py   # Windows
```
Obligatorio: harás la modificación de la **Pregunta 5** (cambiar el umbral).

## Ejecuta el panorama

Desde la raíz del lab:

```bash
uv run python panorama.py
```

**Salida esperada (puede variar levemente):**

```
PANORAMA ANUAL — Dirección de Rentas de Puerto Siracusa
==========================================================
Recaudación total anual  : $90,680,000 CLP
Mes récord               : Diciembre ($9,140,000)
Meses bajo umbral        : Junio, Julio

Recaudación por rubro:
  C (Comercio): $48,480,000 CLP
  G (Gastronomía): $34,090,000 CLP
  T (Turismo): $8,110,000 CLP

Morosidad del cuaderno:
  Patentes vencidas: 8
  Deuda vencida    : $976,000 CLP

[INFO] Informe archivado en: salidas/informe_panorama.txt
```

### La historia que cuentan los números

Mira el **Turismo**: $8.110.000 en el año, pero repartido de forma muy desigual.
Es el rubro chico… salvo en verano. El **mes récord** es Diciembre (arranca la
temporada alta) y los **meses flojos** son Junio y Julio (pleno invierno, el
puerto se vacía). Un buen analista no solo entrega el total: cuenta la historia
detrás. Eso es lo que hará que el Concejo confíe en Don Arquímedes.

## 🔧 La modificación obligatoria (Pregunta 5)

En `main`, cambia el umbral de `meses_bajo_umbral` de `6_500_000` a `7_000_000`:

```python
    informe = construir_informe(matriz, df, umbral=7_000_000)
```

Re-ejecuta `uv run python panorama.py` y observa qué meses aparecen **de más** en
"Meses bajo umbral". Piensa qué le dirías al Concejo con ese corte más alto (¿son
realmente "meses flojos" o solo "bajo un listón más exigente"?). Anótalo para la
Pregunta 5 y **revierte** el umbral a `6_500_000`.

## Responde el interrogatorio y verifica

```bash
cp plantillas/RESPUESTAS.md RESPUESTAS.md          # macOS/Linux
```
```powershell
Copy-Item plantillas\RESPUESTAS.md RESPUESTAS.md   # Windows
```

Responde las 5 preguntas con tus palabras (varias piden lo que viste en TU
terminal: el axis, la máscara, el ValueError, `iloc[6]`). Luego:

```bash
uv run python bin/verificar.py
```

Meta: `✔ 13/13 verificaciones correctas` y el mensaje de Don Arquímedes. El
verificador prueba tus funciones con datos **oficiales** y con datos **sorpresa**
(una matriz y un cuaderno aleatorios): si copiaste cifras fijas, el sorpresa te
delata.

## 🏅 Desafío extra (opcional): el rubro estrella

¿Qué rubro creció más, en porcentaje, entre Junio y Diciembre? Se responde con
UNA línea de NumPy: `(m[11] - m[5]) / m[5] * 100`. La solución comentada está en
[`../soluciones/desafio-rubro-estrella.md`](../soluciones/desafio-rubro-estrella.md)
(spoiler: el Turismo, con un +289,3 %).

## ✅ Checkpoint final del Lab 03

- [ ] Entendiste `axis`, broadcasting, máscaras y DataFrames.
- [ ] Copiaste `panorama.py` a la raíz por tu ruta (🛠️ o 🔎).
- [ ] El informe muestra `$90,680,000`, `Diciembre` y `Junio, Julio`.
- [ ] Hiciste el experimento del umbral $7.000.000 (Pregunta 5) y lo revertiste.
- [ ] Respondiste las 5 preguntas y el verificador dice `✔ 13/13`.

---

🎉 **¡Le diste al puerto sus números!** Con NumPy convertiste una planilla en
totales por donde se miren, y con pandas reencontraste el cuaderno del Lab 01
como una tabla de verdad. Vectorización, broadcasting, máscaras, DataFrames: el
kit del analista de datos.

> **Teaser — Lab 04:** hasta ahora los datos te llegaban cómodos, como módulos de
> Python que solo tenías que importar. Se acabó la comodidad: en el **Lab 04** los
> datos llegan en **archivos de verdad** —CSV, Excel, JSON— y hasta una base de
> datos. Las **cuatro fuentes** te esperan. Nos vemos en el mesón. ⚓
