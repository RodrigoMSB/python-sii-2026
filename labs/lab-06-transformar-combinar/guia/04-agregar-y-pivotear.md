# Guía 4 — Agregar y pivotear

> **Objetivo:** sacar totales por grupo (`groupby`), el porcentaje de cada uno
> dentro de su grupo (`transform`) y los cuadros cruzados (`crosstab`,
> `pivot_table`) que forman el tablero.

REPL abierto; ten el `tablero` armado (censo con rubro + saldo, de la Guía 3).

## `groupby`: partir, aplicar, combinar

`groupby` **parte** los datos por una columna, **aplica** una operación a cada
grupo y **combina** los resultados:

```python
>>> tablero.groupby("rubro")[["deuda", "pagado", "saldo"]].sum()
              deuda  pagado    saldo
rubro
Comercio     881000  280000   601000
Gastronomía  697500  598500    99000
Turismo     1529000  204000  1325000
```

> 🍽️ **Analogía obligatoria: las bandejas del mesón.** Imagina que separas las
> patentes en tres bandejas por rubro sobre el mesón, y sumas el contenido de cada
> bandeja. Eso es `groupby("rubro").sum()`: una fila de total por bandeja.

Turismo debe la mayor plata ($1,3M de saldo) con solo 6 patentes: el puerto vive
del turismo, pero también le debe.

## agg vs `transform`: la diferencia que hay que entender

`groupby(...).sum()` **colapsa**: 3 rubros → 3 filas. Pero a veces no quieres
colapsar, sino **repartir** el total del grupo de vuelta a cada fila — por ejemplo,
para calcular qué % de la deuda de su rubro representa cada contribuyente. Para eso
está **`transform`**:

```python
>>> total_rubro = tablero.groupby("rubro")["deuda"].transform("sum")
>>> total_rubro.shape          # ¡mismo largo que el tablero, no 3!
(25,)
>>> tablero["pct_rubro"] = (tablero["deuda"] / total_rubro * 100).round(1)
```

- **`agg`/`.sum()`** → una fila **por grupo** (3 filas). Para totales.
- **`transform`** → una serie **del mismo largo** que el df (25 filas), con el total
  del grupo repetido en cada fila. Para operar fila-a-fila con el total del grupo.

### 🔮 Predice: ¿qué % de la deuda de Turismo es de Buceo Fondo Claro?

Buceo Fondo Claro (`PS-1022-T`) debe $520.000. **Predice** su % dentro de Turismo
(deuda total de Turismo: $1.529.000) y comprueba:

```python
>>> tablero[tablero["codigo"] == "PS-1022-T"]["pct_rubro"].iloc[0]
```

<details>
<summary>Ver respuesta</summary>

**34,0 %.** Un solo contribuyente concentra un tercio de la deuda de todo su rubro.
Ese dato —imposible de ver en un total plano, evidente con `transform`— justifica
sola la existencia de la Dirección de Rentas 😄.
</details>

> 📝 **Pregunta 4:** ¿qué largo tiene la salida del agg y qué largo la del transform?

## `crosstab`: el conteo cruzado

`pd.crosstab` cuenta **cuántas filas** hay en cada combinación de dos categorías:

```python
>>> pd.crosstab(tablero["estado"], tablero["rubro"])
rubro       Comercio  Gastronomía  Turismo
estado
SUSPENDIDA         2            0        3
VENCIDA            4            4        2
VIGENTE            2            7        1
```

De un vistazo: la Gastronomía es mayormente VIGENTE (7); el Turismo concentra las
SUSPENDIDAS (3). `crosstab` cuenta; no suma valores.

## `pivot_table`: el cuadro final del Concejo

`pivot_table` es como `crosstab`, pero **agrega un valor** en vez de contar. Aquí,
la **deuda sumada** por rubro y estado:

```python
>>> tablero.pivot_table(values="deuda", index="rubro", columns="estado",
...                     aggfunc="sum", fill_value=0)
estado       SUSPENDIDA  VENCIDA  VIGENTE
rubro
Comercio         610000   221000    50000
Gastronomía           0   467000   230500
Turismo         1120000   409000        0
```

- **`values`** qué agregar (deuda), **`index`** las filas (rubro), **`columns`** las
  columnas (estado), **`aggfunc`** cómo agregar (sum).
- **`fill_value=0`**: donde no hay datos (Gastronomía SUSPENDIDA), pon 0 en vez de
  `NaN` — un cuadro para el Concejo no muestra celdas vacías.

**crosstab vs pivot_table:** crosstab **cuenta** (¿cuántas?); pivot_table **agrega
un valor** (¿cuánta deuda?). Misma forma de cuadro, distinta pregunta.

### 🤖 Pregúntale a la IA

> *"En pandas, ¿cuándo uso `groupby().agg()` y cuándo `groupby().transform()`?
> Explícame por qué transform devuelve una serie del mismo largo que el DataFrame
> y agg no, con un ejemplo de calcular el % de cada fila dentro de su grupo."*

## ✅ Checkpoint

- [ ] Sacaste totales por rubro con `groupby().sum()` (3 filas).
- [ ] Entendiste agg (colapsa) vs `transform` (mismo largo) y calculaste `pct_rubro`.
- [ ] Comprobaste que Buceo concentra el 34% de la deuda de Turismo.
- [ ] Armaste el `crosstab` (conteos) y el `pivot_table` (deuda, `fill_value=0`).

Cuando esté todo ✔, sigue con **[Guía 5 — El tablero](05-tablero.md)**.
