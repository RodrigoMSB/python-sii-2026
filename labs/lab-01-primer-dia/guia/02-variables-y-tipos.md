# Guía 2 — Variables y tipos de datos

> **Objetivo:** guardar datos en variables, distinguir sus tipos y hacer las
> primeras operaciones. Y romper algo a propósito para aprender a leer un error.

Abre el REPL para acompañar la guía (`uv run python`) y ve escribiendo lo que
aparezca en los bloques.

## Variables: etiquetas, no cajas

Una **variable** es un nombre que le pegas a un dato, como una **etiqueta**
adhesiva sobre una carpeta. No es una caja que "contiene" el dato; es una
etiqueta que **apunta** a él. (Esta distinción parece fina hoy, pero en la Guía 4
te va a salvar de un error clásico.)

```python
>>> nombre = "Café La Palanca"
>>> deuda = 45000
>>> nombre
'Café La Palanca'
>>> deuda
45000
```

El signo `=` no significa "igual" como en matemáticas; significa **"asígnale
esta etiqueta a este dato"**. Se lee de derecha a izquierda: *toma 45000 y
ponle la etiqueta `deuda`*.

## Los cuatro tipos que usarás hoy

Todo dato en Python tiene un **tipo**. Estos cuatro te bastan para el lab:

| Tipo | Qué es | Ejemplo del municipio |
|------|--------|------------------------|
| `str` | texto (*string*) | `"PS-1006-G"`, `"Café La Palanca"` |
| `int` | número entero | `45000` (pesos), `24` (patentes) |
| `float` | número con decimales | `293750.0` (un promedio) |
| `bool` | verdadero / falso | `True`, `False` (¿está vigente?) |

Pregúntale a Python el tipo de algo con `type()`:

```python
>>> type("PS-1006-G")
<class 'str'>
>>> type(45000)
<class 'int'>
>>> type(True)
<class 'bool'>
```

### 🔮 Predice antes de ejecutar

Antes de correr esto, **anota tu predicción**: ¿qué tipo crees que devuelve
`deuda / 2`?

```python
>>> deuda / 2
>>> type(deuda / 2)
```

<details>
<summary>Ver respuesta</summary>

Da `22500.0` y su tipo es `float`. Aunque `deuda` era un entero, **la división
`/` siempre devuelve `float`** (con punto decimal), incluso si el resultado es
exacto. Lo viste en la Guía 1 con `2350000 / 8`. Guarda este dato: en Rentas, un
"22500.0" donde esperabas "22500" muchas veces es solo esto.
</details>

## Operaciones

### Aritméticas

```python
>>> 185000 + 92000      # suma
277000
>>> 520000 - 45000      # resta
475000
>>> 3 * 45000           # multiplicación
135000
>>> 2350000 / 8         # división (siempre float)
293750.0
>>> 2350000 // 8        # división ENTERA (descarta decimales)
293750
>>> 2350001 % 8         # resto de la división (módulo)
1
>>> 10 ** 2             # potencia (10 al cuadrado)
100
```

`//` (entera) y `%` (resto) parecen raros hoy, pero son útiles: `%` te dice, por
ejemplo, si un número es par (`n % 2 == 0`).

### De comparación (devuelven `bool`)

```python
>>> deuda > 0
True
>>> deuda == 0
False
>>> "VIGENTE" == "vigente"
False
```

¡Ojo con la última! Para Python `"VIGENTE"` y `"vigente"` son **distintas**: las
mayúsculas importan. Esto será crucial cuando filtres por estado.

### Lógicas y la "zona gris" del Café La Palanca

Los operadores `and`, `or`, `not` combinan condiciones. Mira este caso real del
cuaderno:

```python
>>> estado = "VIGENTE"
>>> deuda = 45000
>>> estado == "VIGENTE"
True
>>> deuda > 0
True
>>> estado == "VIGENTE" and deuda > 0
True
```

El **Café La Palanca** está **VIGENTE** *pero* debe $45.000. Su patente está al
día, y aun así arrastra deuda. En el mundo real las categorías no son limpias:
"vigente" no es lo mismo que "sin deuda". Ten presente esta zona gris; vuelve en
la Guía 5 y en el interrogatorio.

## 💥 Rómpelo a propósito

Intenta pegar un texto con un número directamente:

**Comando que ejecutas:**

```python
>>> "La deuda es: " + 45000
```

**Salida esperada (un error):**

```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "int") to str
```

No entres en pánico. **Lee el traceback de abajo hacia arriba**: la **última
línea** es la que importa. Dice `TypeError` (error de tipo) y explica: *solo
puedo concatenar `str` con `str`, no un `int`*. Es decir: Python no mezcla texto
con número usando `+`, porque no sabe si quieres pegar (`"4" + "5" = "45"`) o
sumar. Ante la duda, se planta.

Dos formas de arreglarlo:

```python
>>> "La deuda es: " + str(45000)     # 1) convertir el número a texto
'La deuda es: 45000'
>>> f"La deuda es: {45000}"          # 2) f-string (lo veremos en la Guía 3)
'La deuda es: 45000'
```

> 📝 **Esto alimenta la Pregunta 1** del interrogatorio: copia la **última
> línea** de ESTE error tal como salió en tu terminal. La necesitarás.

### 🤖 Pregúntale a la IA

Si quieres entenderlo más a fondo, un buen prompt es:

> *"En Python, ¿por qué `"texto" + 5` lanza TypeError en vez de convertir el
> número automáticamente como hacen otros lenguajes? Explícamelo con una analogía
> simple."*

Recuerda: la IA te explica, pero la Pregunta 1 la respondes tú con tus palabras.

## ✅ Checkpoint

- [ ] Creaste variables y consultaste su `type()`.
- [ ] Confirmaste que `deuda / 2` es un `float`.
- [ ] Viste que `"VIGENTE" == "vigente"` es `False`.
- [ ] Provocaste el `TypeError` y copiaste su última línea para la Pregunta 1.

Cuando esté todo ✔, sigue con **[Guía 3 — Cadenas](03-cadenas.md)**.
