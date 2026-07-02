# Guía 1 — El censo del practicante

> **Objetivo:** montar el entorno y hacer el **diagnóstico** del censo antes de
> tocar nada. Regla de oro del lab: primero se mira, después se opera.

## El encargo

El practicante de verano tuvo una idea "brillante": fusionó a mano TODAS las
planillas de patentes en un solo archivo —el **Censo de Patentes de Puerto
Siracusa**— y se fue de vacaciones. Don Arquímedes lo abre y palidece.

> «Este censo tiene más mugre que la sentina de un pesquero. Dame un pipeline de
> limpieza y moveré… bueno, primero déjame ver qué es real y qué es mugre.» — Don
> Arquímedes

Hasta ahora los datos venían limpios porque alguien los limpió antes. **Ese
alguien ahora eres tú.** Y la lección del lab es esta: **limpiar no es borrar —
es decidir con criterio y dejar rastro** de cada decisión.

## Montar el taller

```bash
cd labs/lab-05-gran-limpieza
bash bin/00-preparar.sh          # Windows: powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
```

Las dependencias (numpy, pandas, openpyxl) son las mismas del Lab 04, así que ya
están en caché: el preparador no debería descargar nada. Meta: `✔ 8/8` (incluye
"censo con 30 filas de datos").

## Primero el diagnóstico (no toques nada todavía)

> 🔧 **Analogía obligatoria: el elevador.** Ningún mecánico serio cambia una pieza
> sin **subir el auto al elevador** y mirar por debajo primero. Limpiar datos es
> igual: antes de transformar, **diagnosticas**. Si operas a ciegas, rompes cosas
> que estaban bien.

Abre el REPL (`uv run python`) y mira el censo con las cuatro herramientas del
diagnóstico:

```python
>>> import pandas as pd
>>> df = pd.read_csv("datos/censo_patentes.csv")
>>> df.head()
>>> df.info()
```

`info()` ya te grita cosas: mira el tipo de `deuda`. ¿Es número… o texto?

### 🔮 Predice: ¿cuántas formas de escribir "estado"?

El practicante escribió los estados a su antojo. Antes de mirar, **predice**:
¿cuántas variantes distintas de `estado` crees que hay? Luego:

```python
>>> df["estado"].value_counts()
```

<details>
<summary>Ver respuesta</summary>

**Diez.** `VIGENTE`, `vigente`, `Vigente`, `vigente ` (¡con espacio!), `VENCIDA`,
`vencida`, `Vencida`, ` VENCIDA ` (¡con espacios a los lados!), `SUSPENDIDA`,
`suspendida`. Para pandas son diez cosas distintas, aunque para ti sean tres. Ese
número siempre asusta — y es exactamente lo que homogeneizarás en la Guía 2.
</details>

## Los faltantes y el sospechoso

```python
>>> df.isna().sum()
```

Hmm… ¿dice que no falta nada en `deuda`? Es una trampa: los faltantes vienen
escritos como texto (`S/I`, `sin dato`, o celda vacía), así que pandas los cargó
como **texto**, no como "faltante". Por eso `deuda` no es numérica. Lo arreglarás
en la Guía 2 con `na_values`.

Ahora el radar de valores extremos:

```python
>>> pd.read_csv("datos/censo_patentes.csv",
...             na_values=["", "S/I", "sin dato"])["deuda"].describe()
```

Mira el **`max`**: `9999999`. Nueve millones novecientos noventa y nueve mil…
huele a dedo dormido sobre el teclado. Guárdalo: será el protagonista de la Guía 4.

## ✅ Checkpoint

- [ ] El preparador terminó en `✔ 8/8` (sin descargas nuevas).
- [ ] Hiciste `head`, `info`, `value_counts`, `isna().sum()`, `describe`.
- [ ] Confirmaste las **10** variantes crudas de `estado`.
- [ ] Viste que `deuda` llegó como texto y por qué; y el `max` de 9.999.999.

Cuando esté todo ✔, sigue con **[Guía 2 — Homogeneización](02-homogeneizacion.md)**.
