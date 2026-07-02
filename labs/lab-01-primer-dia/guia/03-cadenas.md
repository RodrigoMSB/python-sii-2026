# Guía 3 — Cadenas de texto

> **Objetivo:** manejar texto como un profesional: leer partes de un código,
> limpiarlo, transformarlo y formatearlo. El código de patente será tu conejillo
> de indias.

Ten el REPL abierto (`uv run python`).

## Anatomía de un código de patente

Todos los códigos del puerto tienen la forma `PS-####-Y`. Miremos `PS-1007-T`
con lupa. Una cadena es una **fila de casilleros**, y cada casillero tiene un
número de posición (un **índice**):

```
   P    S    -    1    0    0    7    -    T
   0    1    2    3    4    5    6    7    8      <- índice desde el inicio
  -9   -8   -7   -6   -5   -4   -3   -2   -1      <- índice desde el final
```

Dos ideas clave:

- **Se cuenta desde 0**, no desde 1. La primera letra es la posición `0`.
- Los **índices negativos** cuentan desde el final: `-1` es la última.

```python
>>> codigo = "PS-1007-T"
>>> codigo[0]
'P'
>>> codigo[8]
'T'
>>> codigo[-1]      # la última, sin contar cuántas hay
'T'
```

### 💥 Rómpelo: pídele una posición que no existe

`PS-1007-T` tiene 9 casilleros (del 0 al 8). ¿Qué pasa si pides el 9?

**Comando que ejecutas:**

```python
>>> codigo[9]
```

**Salida esperada (un error):**

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: string index out of range
```

Última línea: `IndexError` — "índice fuera de rango". Le pediste el casillero 9
a algo que llega hasta el 8. Es el error más común al contar desde 1 por
costumbre. Cuenta desde 0 y no te pasará.

## Slicing: cortar un pedazo

Para sacar un **trozo** usas `[desde:hasta]`. Regla de oro: el `desde` **se
incluye**, el `hasta` **NO** (es excluyente).

```python
>>> codigo[0:2]     # del 0 al 1 (el 2 queda afuera)
'PS'
>>> codigo[3:7]     # del 3 al 6 -> el número de rol
'1007'
>>> codigo[-1]      # la letra de rubro
'T'
```

Ese `[3:7]` te da `'1007'`: el `7` marca dónde **cortar sin incluir**. Y para la
letra de rubro, `codigo[-1]` es más robusto que `codigo[8]`, porque funciona sin
importar el largo del código.

> 📝 **Esto alimenta la Pregunta 2:** cómo extraes la letra de rubro y por qué
> `codigo[-1]` también sirve.

## Métodos: acciones que el texto sabe hacer

Un **método** es una acción que le pides a un dato con un punto: `dato.accion()`.
Los datos "sucios" del mundo real (con espacios, mayúsculas raras) se limpian
así:

```python
>>> sucio = "  cocinería doña eureka  "
>>> sucio.strip()            # saca espacios de los extremos
'cocinería doña eureka'
>>> sucio.strip().title()    # ...y pone Mayúscula Inicial A Cada Palabra
'Cocinería Doña Eureka'
```

Ese `sucio.strip().title()` es tu **primer pipeline**: el resultado de `strip()`
pasa directo a `title()`, como una cinta transportadora donde cada máquina hace
su parte. Se lee de izquierda a derecha: *limpia, luego capitaliza*.

Otros métodos útiles hoy:

```python
>>> codigo.startswith("PS")        # ¿empieza con "PS"?
True
>>> codigo.replace("-", "/")       # reemplaza guiones por barras
'PS/1007/T'
>>> codigo.split("-")              # parte por el guion -> ¡devuelve una LISTA!
['PS', '1007', 'T']
```

Fíjate en `split`: no devuelve texto, devuelve una **lista** (`['PS','1007','T']`).
Las listas son el tema de la Guía 4; por ahora solo nota que un método puede
transformar un texto en varios pedazos.

## f-strings: armar texto con datos adentro

En la Guía 2 sufriste con `"texto" + numero`. Los **f-strings** son la forma
cómoda: una cadena que empieza con `f` y donde metes variables entre llaves `{}`.

```python
>>> nombre = "Café La Palanca"
>>> deuda = 45000
>>> f"{nombre} debe ${deuda} CLP"
'Café La Palanca debe $45000 CLP'
```

Y un lujo para números grandes: `:,` agrupa de a miles.

```python
>>> f"Deuda total: ${2350000:,} CLP"
'Deuda total: $2,350,000 CLP'
```

> 💡 Ese formato usa coma como separador de miles (estilo inglés). En Chile
> escribiríamos `2.350.000`, pero para el informe del lab dejaremos el número tal
> cual (`$2350000 CLP`). Lo importante hoy es que **sepas que el formateo
> existe**.

### 🤖 Pregúntale a la IA

> *"Dame 3 mini-ejemplos de formato dentro de f-strings en Python (separador de
> miles, decimales fijos y ancho mínimo) explicados para principiante."*

## ✅ Checkpoint

- [ ] Extrajiste `'PS'`, `'1007'` y `'T'` de `"PS-1007-T"` con slicing/índices.
- [ ] Provocaste el `IndexError` con `codigo[9]`.
- [ ] Encadenaste `.strip().title()` y usaste `split("-")` (¡da una lista!).
- [ ] Armaste un f-string con una variable y probaste `:,`.

Cuando esté todo ✔, sigue con **[Guía 4 — Listas](04-listas.md)**.
