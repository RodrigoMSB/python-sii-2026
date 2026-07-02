# Guía 5 — El pipeline

> **Objetivo:** encadenar todo en `limpiar.py`, producir el censo limpio y un
> informe donde CADA fila descartada quede contada y justificada.

## Elige tu ruta

El programa se llama `limpiar.py`. Copia el archivo a la raíz del lab.

### 🛠️ Ruta Artesano — completas los TODO

```bash
cp plantillas/limpiar.py limpiar.py          # macOS/Linux
```
```powershell
Copy-Item plantillas\limpiar.py limpiar.py   # Windows
```
Completa los **6 TODO** en orden (homogeneizar, deduplicar, filtrar, imputar, IQR,
y la regla de consenso). Cada uno es una de las operaciones de las guías. ¿Trabado?
Mira SOLO esa función en `soluciones/limpiar.py`.

### 🔎 Ruta Explorador — ejecutas y experimentas

```bash
cp soluciones/limpiar.py limpiar.py          # macOS/Linux
```
```powershell
Copy-Item soluciones\limpiar.py limpiar.py   # Windows
```
Obligatorio: harás la modificación de la **Pregunta 5** (bajar el umbral del z-score).

## Ejecuta el pipeline

Desde la raíz del lab:

```bash
uv run python limpiar.py
```

**Salida esperada (puede variar levemente):**

```
INFORME DE LIMPIEZA — Censo de Patentes de Puerto Siracusa
==========================================================
Embudo de filas:
  Censo bruto              : 30
  Tras quitar duplicados   : 28  (-2 exactos)
  Tras filtrar códigos     : 26  (-2 malformados: PS-999, XX-1050-G)
  Deudas imputadas (= 0)   : 3
  Tras apartar outliers    : 25  (-1)

Outliers de deuda (los métodos proponen, el analista dispone):
  PS-1022-T (Buceo Fondo Claro, $520,000): CONSERVADO
      → señalado solo por IQR; el z-score no lo marca. Negocio real
        (deuda conocida desde el Lab 01): se conserva, con nota.
  PS-1046-C (Distribuidora El Quintal, $9,999,999): APARTADO
      → señalado por IQR y z-score (consenso). Error de digitación: se aparta.

Censo limpio : 25 filas — Deuda total : $3,107,500 CLP
```

## El embudo, contado (contrato C14)

Mira el embudo: **30 → 28 → 26 → 25**. Cada salto tiene nombre y número:

- **30 → 28:** −2 filas **exactamente duplicadas** (el copy-paste del practicante).
- **28 → 26:** −2 **códigos malformados** (`PS-999`, `XX-1050-G`).
- (imputación: 3 deudas faltantes → 0; **no cambia** el número de filas, pero SÍ se
  cuenta.)
- **26 → 25:** −1 **outlier de digitación** (`PS-1046-C`), apartado por consenso.

**Nada se descartó sin quedar contado y justificado.** Ese es el corazón del lab:
un censo limpio en el que puedes rendir cuentas de cada fila que no llegó al final.

También se exportó el resultado: `salidas/censo_limpio.csv` y
`salidas/censo_limpio.xlsx` (25 filas), listos para el Concejo.

## 🔧 La modificación obligatoria (Pregunta 5)

`limpiar_censo` recibe un parámetro `umbral_z` (por defecto `3.0`). Bájalo a `2.0`:

```python
    limpio, reporte = limpiar_censo(CENSO, umbral_z=2.0)
```
(edita esa llamada en `main`, o llama a `limpiar_censo` con `umbral_z=2.0`).

Re-ejecuta y observa: ¿cambió la lista de `outliers_z`? ¿Cambió el **consenso**
(los apartados) y por tanto el censo final? Explica qué implica bajar el umbral
—¿el método se vuelve más o menos estricto?— y **revierte** a `3.0`.

## Responde el interrogatorio y verifica

```bash
cp plantillas/RESPUESTAS.md RESPUESTAS.md          # macOS/Linux
```
```powershell
Copy-Item plantillas\RESPUESTAS.md RESPUESTAS.md   # Windows
```

Responde las 5 preguntas (varias piden lo que viste en TU terminal: las variantes,
el embudo, el desacuerdo de los métodos). Luego:

```bash
uv run python bin/verificar.py
```

Meta: `✔ 14/14 verificaciones correctas`. El verificador prueba tu pipeline con el
censo oficial y con un **censo sorpresa** (mugre aleatoria en un archivo temporal):
si copiaste cifras fijas, el sorpresa te delata.

## 🏅 Desafío extra (opcional): el certificado de calidad

Escribe una función que reciba el censo **bruto** y devuelva un mini-informe de
calidad: % de completitud por columna (deuda: 90 %), variantes crudas de `estado`
(10) y candidatos a duplicado por código. La solución está en
[`../soluciones/desafio-certificado-calidad.md`](../soluciones/desafio-certificado-calidad.md).

## ✅ Checkpoint final del Lab 05

- [ ] Entendiste homogeneización, duplicados, filtrado, imputación y outliers.
- [ ] Copiaste `limpiar.py` a la raíz por tu ruta (🛠️ o 🔎).
- [ ] El informe muestra el embudo `30→28→26→25` y `$3,107,500`.
- [ ] Hiciste el experimento del umbral z=2.0 (Pregunta 5) y lo revertiste.
- [ ] Respondiste las 5 preguntas y el verificador dice `✔ 14/14`.

---

🎉 **¡Limpiaste el censo del practicante!** Homogeneizaste texto, deduplicaste,
filtraste con regex, imputaste con una regla explícita y decidiste los outliers
con criterio — dejando **rastro escrito de cada decisión**. Ahora eres tú quien
deja los datos limpios para el siguiente.

> **Teaser — Lab 06:** el censo limpio ya no estará solo. En el Módulo 3
> aprenderás a **transformar y combinar**: cruzar el censo con los pagos, los
> permisos y las multas del Lab 04, con `merge`. Las piezas del puerto, por fin,
> juntas. Nos vemos en el mesón. ⚓
