# Desafío extra — ¿Quién es el mayor deudor? (sin usar `max()`)

> Opcional. Este desafío no lo revisa el verificador; es para que te lleves a
> casa el patrón más importante del lab.

Don Arquímedes entra con una duda: *"De todas las patentes, ¿cuál es la que más
debe? No me digas la lista, dime el nombre y el monto."*

Sería fácil con `max()`. Pero justamente por eso te pido que lo hagas **sin**
`max()`: quiero que entiendas el patrón que hay **debajo** de `max()`, porque es
el mismo que usarás miles de veces cuando lleguemos a pandas.

## La idea: "recordar el mayor visto hasta ahora"

Recorres la lista guardando en una variable la mejor patente que has visto
**hasta ese momento**. Cada vez que aparece una que debe más, actualizas el
recuerdo. Al terminar el recorrido, lo que recuerdas es el máximo.

```python
from datos.cuaderno import PATENTES

POS_NOMBRE = 1
POS_DEUDA = 3

def mayor_deudor(patentes):
    # Empezamos sin ningún candidato.
    mejor = None
    for patente in patentes:
        # Si no hay candidato todavía, o esta debe MÁS que el mejor recordado,
        # entonces esta patente pasa a ser el nuevo "mejor".
        if mejor is None or patente[POS_DEUDA] > mejor[POS_DEUDA]:
            mejor = patente
    return mejor

peor = mayor_deudor(PATENTES)
print(f"Mayor deudor: {peor[POS_NOMBRE]} (${peor[POS_DEUDA]} CLP)")
```

## Salida esperada

```
Mayor deudor: Buceo Fondo Claro ($520000 CLP)
```

(La Buceo Fondo Claro está `SUSPENDIDA` y arrastra la mayor deuda: $520.000.)

## Por qué este patrón importa

Este "recorrer recordando el mejor hasta ahora" es, literalmente, el abuelo de
lo que en el Módulo 2 escribirás como:

```python
df["deuda"].max()
```

pandas hace exactamente esto por dentro, solo que optimizado y en una línea.
Entender el bucle a mano hoy hace que mañana `.max()` no sea magia, sino un
atajo que ya sabes desarmar.

## Variante: ¿y si hay empate?

Con `>` (mayor estricto), si dos patentes deben lo mismo te quedas con la
**primera** que apareció, porque una deuda igual no supera a la ya recordada.
Si usaras `>=`, te quedarías con la **última**. Ninguna está "mal": es una
decisión de negocio (¿el empate lo gana el más antiguo o el más nuevo?). Cámbialo
y observa la diferencia; entender ese matiz es justo el tipo de detalle que en
Rentas evita errores caros.
