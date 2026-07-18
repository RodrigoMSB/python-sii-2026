# Guía 2 — Diccionarios

> **Objetivo:** conocer la estructura estrella del lab. El diccionario resuelve
> un dolor concreto: buscar rápido y guardar datos con nombre en vez de por
> posición.

Ten el REPL abierto (`bash bin/repl.sh`).

## El dolor: buscar en una lista de listas

En el Lab 01, el cuaderno era una **lista de listas**. Para encontrar una patente
por su código, no había otra que **recorrer todo** hasta dar con ella:

```python
>>> from datos.cuaderno import PATENTES
>>> buscado = "PS-1013-C"
>>> encontrada = None
>>> for patente in PATENTES:
...     if patente[0] == buscado:
...         encontrada = patente
...         break
...
>>> encontrada
['PS-1013-C', 'Botillería La Sirena', 'SUSPENDIDA', 405000]
```

Cinco líneas para una búsqueda. Y si el cuaderno tuviera 10.000 patentes, Python
tendría que mirarlas una por una. Ilegible y lento. Tiene que haber algo mejor.

## El diccionario: un fichero con pestañas

Un **diccionario** (`dict`) guarda pares **clave → valor**. En vez de acordarte
de que "la posición 2 es el estado", le pones **nombre** a cada dato. Y en vez de
recorrer para buscar, vas directo por la clave, como quien abre la pestaña
correcta de un fichero.

```python
>>> ficha = {"codigo": "PS-1013-C", "estado": "SUSPENDIDA", "deuda": 405000}
>>> ficha["estado"]        # vas DIRECTO por el nombre, sin recorrer nada
'SUSPENDIDA'
>>> ficha["deuda"]
405000
```

Se lee soloo: `ficha["estado"]` es "de la ficha, el estado". Comparado con
`patente[2]`, no hay que recordar qué era el 2.

## Leer: corchetes `[]` vs `.get()`

Hay dos formas de leer un valor, y la diferencia importa cuando la clave **no
existe**.

### 💥 Rómpelo: pide una clave que no está

```python
>>> ficha["telefono"]
```
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
KeyError: 'telefono'
```

Última línea: `KeyError: 'telefono'`. Con corchetes, si la clave no existe,
Python **revienta**. A veces es lo que quieres (que falle fuerte). Pero muchas
veces prefieres un valor por defecto sin drama, y para eso está `.get()`:

```python
>>> ficha.get("telefono")           # no existe -> devuelve None, sin reventar
>>> ficha.get("telefono", "s/d")    # ...o el valor por defecto que tú digas
's/d'
>>> ficha.get("estado", "s/d")      # sí existe -> devuelve el valor real
'SUSPENDIDA'
```

> 📝 **Esto alimenta la Pregunta 1:** copia la última línea del `KeyError` y
> explica qué habría devuelto `.get()` en el mismo caso.

Este `.get(clave, valor_por_defecto)` es exactamente el truco que usarás en
`deuda_por_rubro` para sumar sin que la primera vez explote.

## Escribir, preguntar y recorrer

```python
>>> ficha["deuda"] = 0              # cambia un valor
>>> ficha["rubro"] = "C"           # agrega una clave nueva
>>> "codigo" in ficha              # 'in' sobre un dict pregunta por las CLAVES
True
>>> "Botillería" in ficha          # ojo: pregunta por CLAVES, no por valores
False
>>> ficha.keys()
dict_keys(['codigo', 'estado', 'deuda', 'rubro'])
>>> ficha.values()
dict_values(['PS-1013-C', 'SUSPENDIDA', 0, 'C'])
```

Recorrer clave y valor a la vez, con `.items()`:

```python
>>> for clave, valor in ficha.items():
...     print(f"{clave}: {valor}")
...
codigo: PS-1013-C
estado: SUSPENDIDA
deuda: 0
rubro: C
```

Recuerda de la Guía 1: `"codigo" in ficha` es lo mismo que te dirá si un código
**ya fue guardado** en el fichero. Justo lo que necesitas para detectar
duplicados.

## Construye una ficha a mano

Así se verá cada ficha de tu fichero consolidado. Ármala tú:

```python
>>> nueva = {
...     "codigo": "PS-1030-T",
...     "nombre": "Miradores del Istmo",
...     "estado": "SUSPENDIDA",
...     "deuda": 290000,
...     "rubro": "T",
... }
>>> nueva["rubro"], nueva["deuda"]
('T', 290000)
```

Y el **fichero** completo será un dict de dicts: `{codigo: ficha}`. Buscar la
patente `"PS-1030-T"` será tan simple como `fichero["PS-1030-T"]`. Adiós al bucle
de búsqueda.

### 🤖 Pregúntale a la IA

> *"¿Cuándo conviene usar una lista y cuándo un diccionario en Python? Dame 3
> señales de que un dato pide dict en vez de lista, con ejemplos simples."*

## ✅ Checkpoint

- [ ] Comparaste el bucle de búsqueda (lista) con el acceso directo (dict).
- [ ] Provocaste el `KeyError` con `[]` y viste qué hace `.get()` en su lugar.
- [ ] Usaste `in`, `keys/values/items` e iteraste con `for clave, valor in ...`.
- [ ] Construiste una ficha a mano.

Cuando esté todo ✔, sigue con **[Guía 3 — Funciones](03-funciones.md)**.
