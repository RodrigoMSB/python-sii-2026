# Guía 3 — Funciones

> **Objetivo:** dejar de escribir scripts sueltos y empezar a fabricar
> **herramientas** reutilizables. El triaje se hace cada semana; una función se
> escribe una vez y se usa siempre.

REPL abierto (`uv run python`).

## `def`: una herramienta con nombre

Una **función** empaqueta un trozo de trabajo bajo un nombre, recibe **datos de
entrada** (parámetros) y **devuelve** un resultado con `return`.

```python
>>> def formatear_pesos(monto):
...     return f"${monto:,} CLP"
...
>>> formatear_pesos(290000)
'$290,000 CLP'
```

`monto` es el parámetro (lo que entra); `return` entrega lo que sale. Una vez
definida, la llamas cuantas veces quieras sin reescribir nada.

## Valores por defecto

Un parámetro puede traer un **valor por defecto**: si no lo pasas, usa ese.

```python
>>> def formatear_pesos(monto, simbolo="$"):
...     return f"{simbolo}{monto:,} CLP"
...
>>> formatear_pesos(290000)          # usa el "$" por defecto
'$290,000 CLP'
>>> formatear_pesos(290000, "US$")   # ...o el que le pases
'US$290,000 CLP'
```

Los parámetros con valor por defecto van **siempre al final**.

## `*args` y `**kwargs` (en dosis pequeña)

A veces no sabes cuántos argumentos llegarán. `*args` los junta en una **tupla**:

```python
>>> def sumar_deudas(*montos):
...     return sum(montos)
...
>>> sumar_deudas(154000, 83000, 290000)
527000
>>> sumar_deudas(12000)
12000
```

Y `**kwargs` junta pares clave=valor en un **diccionario** — útil para armar una
ficha flexible:

```python
>>> def crear_ficha_flexible(**datos):
...     return datos
...
>>> crear_ficha_flexible(codigo="PS-1030-T", deuda=290000)
{'codigo': 'PS-1030-T', 'deuda': 290000}
```

No abuses de ellos hoy; solo reconócelos cuando los veas.

## Lambdas: mini-funciones de una línea

Una **lambda** es una función anónima y cortita. Brilla junto a `sorted`, para
decir "ordena usando ESTE criterio":

```python
>>> fichas = [
...     {"codigo": "PS-1027-T", "deuda": 154000},
...     {"codigo": "PS-1030-T", "deuda": 290000},
...     {"codigo": "PS-1041-C", "deuda": 12000},
... ]
>>> sorted(fichas, key=lambda ficha: ficha["deuda"], reverse=True)
[{'codigo': 'PS-1030-T', 'deuda': 290000}, {'codigo': 'PS-1027-T', 'deuda': 154000}, {'codigo': 'PS-1041-C', 'deuda': 12000}]
```

`key=lambda ficha: ficha["deuda"]` significa "para comparar, mira la deuda de
cada ficha". Con `reverse=True`, de mayor a menor. (Este es justo el corazón del
desafío extra del final del lab.)

## Las funciones son objetos de primera clase

En Python, una función es un valor como cualquier otro: puedes guardarla en una
variable o **pasarla a otra función**.

```python
>>> def aplicar(func, valor):
...     return func(valor)
...
>>> aplicar(formatear_pesos, 64000)
'$64,000 CLP'
```

Le pasamos `formatear_pesos` **sin paréntesis** (no la llamamos, se la
entregamos) y `aplicar` la usa por dentro. Suena abstracto, pero es exactamente
lo que hace `sorted` con tu `lambda`.

## 💥 Scope: local vs global

Las variables creadas **dentro** de una función viven solo ahí (son **locales**).
Mira este clásico que confunde a todos:

```python
>>> total = 0
>>> def acumular(monto):
...     total = total + monto      # 💥
...     return total
...
>>> acumular(1000)
```
```
UnboundLocalError: cannot access local variable 'total' where it is not associated with a value
```

¿Qué pasó? Al **asignar** `total` dentro de la función, Python la trata como una
variable **local** nueva… pero la usas (`total + monto`) antes de darle valor.
De ahí el error. Sin dramatismo: la regla es que cada función tiene su propio
"escritorio" y no escribe en el de afuera salvo que se lo pidas explícitamente.

La forma correcta y limpia (la que usarás en el lab) es **no depender de
globales**: pasa lo que necesitas como parámetro y devuelve el resultado.

```python
>>> def acumular(total, monto):
...     return total + monto
...
>>> acumular(0, 1000)
1000
```

## ✅ Checkpoint

- [ ] Definiste funciones con `return` y con un parámetro por defecto.
- [ ] Probaste `*args` (suma variable) y reconociste `**kwargs`.
- [ ] Ordenaste una lista de fichas con `sorted` + `lambda`.
- [ ] Pasaste una función como argumento a otra.
- [ ] Provocaste el `UnboundLocalError` y entendiste el porqué del scope.

Cuando esté todo ✔, sigue con **[Guía 4 — Excepciones](04-excepciones.md)**.
