# Guía 1 — El archivador antiguo

> **Objetivo:** montar el taller del Lab 02 y conocer dos estructuras nuevas —
> **tuplas** y **sets**— con las que empezaremos a domar los datos sucios.

## El encargo

Don Arquímedes aparece cargando una caja de fierro llena de polvo:

> «¿Se acuerda del cuaderno que ordenamos? Bueno… apareció el **archivador
> antiguo**. Patentes que nunca se digitalizaron. Mandé a transcribirlas, pero el
> muchacho lo hizo a la rápida: hay deudas escritas como se les ocurrió —con
> puntos, algunas dicen "S/I"— y creo que una patente quedó pegada dos veces.
> Necesito que arme un fichero limpio: lo que sirve, adentro; lo que no, afuera
> pero anotado. Sin que se le caiga el programa a la primera de cambio.»

Ese fichero limpio es `consolidar.py`, y lo construirás en la Guía 5. Antes,
tres guías de herramientas nuevas.

## Montar el taller

Igual que en el Lab 01. Desde la carpeta del lab:

**macOS/Linux:**
```bash
cd labs/lab-02-cuaderno-crece
bash bin/00-preparar.sh
```
**Windows:**
```powershell
cd labs\lab-02-cuaderno-crece
powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
```

**Salida esperada (puede variar levemente):**
```
[OK] uv encontrado: /.../uv
[OK] Entorno .venv/ listo.
...
✔ 5/5 verificaciones correctas
```

Abre el REPL para acompañar la guía: `uv run python`.

## Tuplas: como una lista, pero timbrada

Una **tupla** se ve casi como una lista, pero con paréntesis, y tiene una
diferencia clave: **es inmutable**, no se puede modificar una vez creada.

```python
>>> punto = ("PS-1030-T", 290000)
>>> punto[0]
'PS-1030-T'
>>> punto[1]
290000
```

> 🏛️ **Analogía obligatoria: el folio timbrado.** Una lista es como un borrador a
> lápiz: lo corriges cuando quieras. Una tupla es como un **folio timbrado del
> archivo municipal**: una vez timbrado, no se corrige. Si algo cambió, no
> "rayas" el folio: emites **otro**. Por eso las tuplas sirven para datos que
> vienen de a pares y no deben mutar (un código y su deuda, una coordenada).

Míralo fallar a propósito:

```python
>>> punto[1] = 0
```
```
TypeError: 'tuple' object does not support item assignment
```

Última línea: `TypeError` — la tupla **no admite** que le reasignes una posición.
Es a propósito: te protege de cambiar sin querer algo que debía quedar fijo. En
este lab, `rechazos` será una lista de **tuplas** `(codigo, motivo)`.

## Sets: la bolsa de cosas únicas

Un **set** es una colección **sin orden** y **sin repetidos**. Su superpoder:
elimina duplicados solo.

```python
>>> rubros = {"C", "G", "T", "C", "G"}
>>> rubros
{'C', 'G', 'T'}
```

Metiste cinco elementos y quedaron tres: los repetidos se fusionan. Esa es la
gracia.

### 🔮 Predice antes de ejecutar

El asistente dejó códigos repetidos. ¿Cuántos códigos **únicos** hay aquí?
Anota tu predicción y luego ejecuta:

```python
>>> codigos = ["PS-1026-C", "PS-1027-T", "PS-1026-C", "PS-1030-T", "PS-1027-T"]
>>> len(codigos)
>>> len(set(codigos))
```

<details>
<summary>Ver respuesta</summary>

`len(codigos)` es `5` (la lista tal cual), pero `len(set(codigos))` es `3`:
al convertir a set, `PS-1026-C` y `PS-1027-T` repetidos colapsan. Convertir a set
y medir es la forma más rápida de contar "cuántos distintos hay".
</details>

## Un adelanto que da curiosidad

¿Cuántos códigos únicos hay en TODO el archivador? Se puede así:

```python
>>> from datos.archivador import REGISTROS_BRUTOS
>>> codigos = []
>>> for r in REGISTROS_BRUTOS:
...     codigos.append(r["codigo"])
...
>>> len(codigos)            # 18 registros...
18
>>> len(set(codigos))      # ...pero, ¿cuántos códigos distintos?
17
```

18 registros, 17 códigos únicos: **uno está repetido** (el famoso PS-1026-C).
Y esa misma cuenta se puede escribir en UNA sola línea mágica:

```python
>>> len({r["codigo"] for r in REGISTROS_BRUTOS})
17
```

Eso de `{... for ... in ...}` es una **comprensión**, "el for de una línea". Te
prometo explicarla en la Guía 5; por ahora quédate con que existe y es breve.

## ✅ Checkpoint

- [ ] El preparador terminó en `✔ 5/5`.
- [ ] Creaste una tupla y viste el `TypeError` al intentar modificarla.
- [ ] Creaste un set y confirmaste que elimina repetidos.
- [ ] Contaste códigos únicos del archivador con `set` (17 de 18).

Cuando esté todo ✔, sigue con **[Guía 2 — Diccionarios](02-diccionarios.md)**.
