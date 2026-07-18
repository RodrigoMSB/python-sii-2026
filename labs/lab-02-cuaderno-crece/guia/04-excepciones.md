# Guía 4 — Excepciones

> **Objetivo:** que un dato sucio NO bote todo el programa. Aprenderás a atrapar
> errores, a distinguirlos y a crear el tuyo propio: `RegistroInvalido`.

REPL abierto (`bash bin/repl.sh`).

## El problema: la transcripción sucia

El archivador trae deudas como `"38.000"` (texto con puntos) y también `"S/I"`.
Para convertir a número, primero quitas los puntos y luego usas `int`:

```python
>>> int("38.000".replace(".", ""))
38000
```

Pero mira qué pasa con `"S/I"`:

### 💥 Rómpelo

```python
>>> int("S/I".replace(".", ""))
```
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: invalid literal for int() with base 10: 'S/I'
```

Última línea: `ValueError` — "literal inválido para int()". Python no sabe
convertir `"S/I"` a número, y **revienta**. Si esto ocurre en medio de un bucle
que procesa 18 registros, el programa muere en el registro malo y no termina.
Necesitamos **atraparlo**.

## `try` / `except`: la red de seguridad

```python
>>> texto = "S/I"
>>> try:
...     numero = int(texto.replace(".", ""))
... except ValueError:
...     numero = None
...     print(f"No pude convertir: {texto!r}")
...
No pude convertir: 'S/I'
>>> numero
```

El bloque `try` intenta; si adentro salta un `ValueError`, el `except` lo
**atrapa** y el programa **sigue vivo**. Esa es toda la idea.

## `else` y `finally`: el protocolo de la caja municipal

`try` puede llevar dos bloques más:

```python
>>> def registrar_pago(texto):
...     try:
...         monto = int(texto.replace(".", ""))
...     except ValueError:
...         print("  Rechazado: monto ilegible")
...     else:
...         print(f"  Timbrado: ${monto:,}")     # solo si NO hubo error
...     finally:
...         print("  Caja cerrada")               # SIEMPRE, pase lo que pase
...
>>> registrar_pago("38.000")
  Timbrado: $38,000
  Caja cerrada
>>> registrar_pago("S/I")
  Rechazado: monto ilegible
  Caja cerrada
```

> 🏛️ **Analogía obligatoria: la caja municipal.**
> - `try` es **atender el trámite**.
> - `except` es **qué haces si el trámite falla** (el cheque no tiene fondos).
> - `else` es **"si el trámite salió bien, timbra"** — solo corre si NO hubo error.
> - `finally` es **"pase lo que pase, cierra la caja"** — corre siempre, con
>   error o sin él. Perfecto para cerrar archivos o soltar recursos.

## Una familia de errores (que ya conoces)

Los errores tienen **tipos**, y ya te cruzaste con varios:

- `ValueError` — el valor no sirve (`int("S/I")`).
- `KeyError` — pediste una clave que no existe en un dict (Guía 2).
- `TypeError` — mezclaste tipos incompatibles (`"texto" + 5`, Lab 01).

Todos descienden de una gran familia (`Exception`). Puedes atrapar uno específico
—lo recomendable— o varios.

## Tu propio error: `RegistroInvalido`

Puedes crear tus propias excepciones. Basta heredar de una existente. Como un
registro ilegible es, en el fondo, un problema de **valor**, heredamos de
`ValueError`:

```python
>>> class RegistroInvalido(ValueError):
...     """Se lanza cuando un registro bruto no se puede convertir en ficha."""
...
>>> def normalizar(texto):
...     try:
...         return int(texto.replace(".", ""))
...     except ValueError:
...         raise RegistroInvalido(f"deuda no numérica ('{texto}')") from None
...
>>> normalizar("64.000")
64000
>>> normalizar("S/I")
```
```
RegistroInvalido: deuda no numérica ('S/I')
```

`raise` **lanza** una excepción. El `from None` evita arrastrar el traceback
interno del `ValueError` original, dejando un mensaje limpio. Tener NUESTRO tipo
nos deja luego atrapar **exactamente** este caso y no confundirlo con otros.

## ¿Por qué no un `except:` pelado?

Es tentador escribir `except:` a secas para "atrapar todo". No lo hagas: se
tragaría **cualquier** error —incluso un typo tuyo o un `Ctrl-C`— y te ocultaría
bugs de verdad. Atrapa lo **específico** que esperas:

```python
except RegistroInvalido:   # sé exactamente qué estoy manejando
    ...
```

> 📝 **Anota para el interrogatorio:** este `ValueError` de `int("S/I")` y cómo lo
> conviertes en `RegistroInvalido` es el centro del lab. En la Guía 5 lo verás
> ocurrir **en vivo** con pdb.

## ✅ Checkpoint

- [ ] Provocaste el `ValueError` de `int("S/I")` y lo leíste.
- [ ] Atrapaste un error con `try/except` y el programa siguió vivo.
- [ ] Usaste `else` y `finally` (el protocolo de la caja municipal).
- [ ] Creaste `RegistroInvalido(ValueError)` y la lanzaste con `raise`.
- [ ] Entendiste por qué se captura específico y no `except:` pelado.

Cuando esté todo ✔, sigue con **[Guía 5 — La consolidación](05-consolidacion.md)**.
