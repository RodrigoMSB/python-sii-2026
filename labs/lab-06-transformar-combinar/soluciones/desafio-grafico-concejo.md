# Desafío extra — El gráfico del Concejo (barras apiladas)

> Opcional. No lo revisa el verificador; es para que le des al Concejo un gráfico
> que cuente DOS dimensiones a la vez.

El gráfico del tablero muestra el saldo por rubro (una barra por rubro). Don
Arquímedes quiere algo más rico para la presentación: **la deuda por rubro,
desglosada por estado**, en barras **apiladas** — así se ve, de un vistazo, cuánto
de la deuda de cada rubro es de patentes vigentes, vencidas o suspendidas.

## La idea: pandas grafica directo desde un pivote

Ya tienes el pivote (`pivote_deuda`): rubro en las filas, estado en las columnas.
pandas puede graficarlo con un `.plot(kind="bar", stacked=True)`:

```python
import matplotlib
matplotlib.use("Agg")            # C16: headless, siempre
import matplotlib.pyplot as plt
import pandas as pd

# pivote deuda: filas=rubro, columnas=estado
piv = tablero.pivot_table(values="deuda", index="rubro", columns="estado",
                          aggfunc="sum", fill_value=0)

ax = piv.plot(kind="bar", stacked=True)         # una barra por rubro, apilada por estado
ax.set_title("Deuda por rubro y estado — Puerto Siracusa")
ax.set_xlabel("Rubro")
ax.set_ylabel("Deuda (CLP)")
ax.legend(title="Estado")                        # la leyenda explica los colores
ax.figure.tight_layout()
ax.figure.savefig("salidas/deuda_apilada.png", dpi=150)
plt.close(ax.figure)
```

## Lo que produces

Tres barras (Comercio, Gastronomía, Turismo), cada una dividida en segmentos de
color por estado (SUSPENDIDA / VENCIDA / VIGENTE). El **alto total** de cada barra
es la deuda del rubro; los **segmentos** muestran su composición. La leyenda
(`legend`) traduce cada color.

## Notas

- **Colores por estado:** al apilar, pandas asigna un color por columna (estado).
  Puedes fijarlos con `color=[...]` si quieres, por ejemplo, rojo para VENCIDA;
  para el Concejo, lo importante es que la **leyenda** esté clara.
- **`stacked=True` vs `False`:** con `False`, las barras van lado a lado
  (comparas estados entre rubros); con `True`, se apilan (ves la composición de
  cada rubro). Elige según la pregunta que quieras responder.
- **La lección:** un pivote bien armado se convierte en gráfico casi solo. La
  transformación (Guía 4) y la visualización (Guía 5) son dos caras de lo mismo:
  llevar los números a una forma que **se entienda de un vistazo**.
