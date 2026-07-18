# Guía 4 — Base de datos y transacciones

> **Objetivo:** leer la cuarta fuente (SQLite) y dominar el tema estrella del
> módulo: **las transacciones** (commit y rollback). Aquí se cura el miedo del
> municipio a la base de datos.

REPL abierto (`bash bin/repl.sh`). Trabajaremos SIEMPRE sobre una **copia** en
`salidas/`, nunca sobre la fuente original:

```python
>>> import shutil
>>> from pathlib import Path
>>> Path("salidas").mkdir(exist_ok=True)
>>> shutil.copyfile("datos/fuentes/contribuyentes.db", "salidas/practica.db")
```

## Leer la BD: `sqlite3` y luego `pd.read_sql`

`sqlite3` viene con Python (no se instala nada). Te conectas, pides un **cursor**
y ejecutas SQL:

```python
>>> import sqlite3
>>> con = sqlite3.connect("salidas/practica.db")
>>> cur = con.execute("SELECT codigo, nombre FROM contribuyentes LIMIT 3")
>>> cur.fetchall()
[('PS-1006-G', 'Café La Palanca'), ('PS-1007-T', 'Kayaks Bahía Serena'), ('PS-1013-C', 'Botillería La Sirena')]
>>> con.close()
```

Y el puente a pandas es directo con `pd.read_sql`:

```python
>>> import pandas as pd
>>> con = sqlite3.connect("salidas/practica.db")
>>> df = pd.read_sql("SELECT * FROM contribuyentes", con)
>>> con.close()
>>> df.shape
(10, 3)
```

> 🔌 **Cierra siempre la conexión** (contrato C11). Una conexión abierta deja la
> BD "tomada" — y en Windows, el próximo intento de escribir el archivo falla con
> `PermissionError: [WinError 32]`. Más abajo verás el patrón profesional… y una
> trampa muy famosa que **parece** cerrarla y no lo hace.

## El tema estrella: transacciones

Aquí está el "porque una vez se borró algo". Una **transacción** es un trámite
que ocurre **entero o nada**.

> 🏛️ **Analogía obligatoria: la caja municipal.**
> - Escribir una fila es **llenar la boleta**.
> - `commit()` es **el timbre**: hasta que no timbras, la boleta **no existe**
>   oficialmente.
> - `rollback()` es **anular el trámite**: si el cajero se equivoca a mitad de
>   camino, rompe la boleta y **no queda nada a medias**.

### Demo 1 — La boleta sin timbre (el aha! del lab)

Inserta una fila pero **NO** hagas commit; cierra y reabre:

```python
>>> con = sqlite3.connect("salidas/practica.db")
>>> con.execute("CREATE TABLE IF NOT EXISTS pagos (codigo TEXT, monto INTEGER)")
>>> con.execute("INSERT INTO pagos VALUES ('PS-1006-G', 45000)")
>>> con.close()                      # cerramos SIN commit
>>> # reabrimos y miramos:
>>> con = sqlite3.connect("salidas/practica.db")
>>> con.execute("SELECT COUNT(*) FROM pagos").fetchone()
(0,)
>>> con.close()
```

**Cero filas.** La boleta sin timbre nunca existió. Sin `commit`, tus cambios se
esfuman al cerrar. Esto no es un bug: es la **protección** que evita dejar datos
a medias si algo falla en la mitad.

> 📝 **Pregunta 1:** anota qué pasó con la fila sin commit.

### Demo 2 — El timbre (commit persiste)

```python
>>> con = sqlite3.connect("salidas/practica.db")
>>> con.execute("INSERT INTO pagos VALUES ('PS-1006-G', 45000)")
>>> con.commit()                     # ¡el timbre!
>>> con.close()
>>> con = sqlite3.connect("salidas/practica.db")
>>> con.execute("SELECT COUNT(*) FROM pagos").fetchone()
(1,)
>>> con.close()
```

Ahora sí: con `commit`, la fila **persiste** al reabrir.

### Demo 3 — El rollback ante un error (IntegrityError)

`contribuyentes` tiene `codigo` como **PRIMARY KEY**: no admite duplicados.
Intenta insertar uno que ya existe y observa:

```python
>>> con = sqlite3.connect("salidas/practica.db")
>>> try:
...     con.execute("INSERT INTO contribuyentes VALUES ('PS-1006-G', 'Otro', 'X')")
...     con.commit()
... except sqlite3.IntegrityError as e:
...     print("Rechazado:", e)
...     con.rollback()               # anulamos el trámite fallido
...
Rechazado: UNIQUE constraint failed: contribuyentes.codigo
>>> con.close()
```

`IntegrityError` — la BD se protegió sola de un duplicado. Y con `rollback`
dejamos todo como estaba, sin medias boletas. Esta es exactamente la lógica de
tu función `registrar_pago`: valida, y si algo no cuadra, **rollback y afuera**.

## 💥 Rómpelo: la trampa del `with` (el error que parece correcto)

Este es el error más peligroso del lab, porque **no lanza excepción**: parece que
funciona. Muchísimo código (y muchísimos tutoriales) escriben esto creyendo que
cierra la conexión:

```python
>>> with sqlite3.connect("salidas/practica.db") as con:
...     con.execute("INSERT INTO pagos VALUES ('PS-1017-G', 76000)")
...
```

Suena lógico: "el `with` abre y cierra solo". **Pero es falso.** Compruébalo tú
mismo, ahora, en tu terminal:

```python
>>> con.execute("SELECT COUNT(*) FROM pagos").fetchone()
```

**Salida esperada:** ¡funciona y te devuelve un número! Si la conexión estuviera
cerrada, esto lanzaría `ProgrammingError: Cannot operate on a closed database`.
No lo lanza: **la conexión sigue viva**.

Lo que hace `with sqlite3.connect(...)` es **commit al salir del bloque**, no
`close()`. Es un context manager **transaccional**, no de conexión. Y una
conexión viva mantiene el `.db` tomado: en Windows, el próximo intento de
reescribir ese archivo revienta con `PermissionError: [WinError 32]`.

> ⛔ **Contrato C11 (doctrina del curso):** `with sqlite3.connect(...)` está
> **prohibido** en este curso. Nunca confundas "se hizo commit" con "se cerró".

### El patrón profesional (el que usarás)

Se pueden tener las dos cosas — transacción automática **y** cierre garantizado:

```python
>>> con = sqlite3.connect("salidas/practica.db")
>>> try:
...     with con:                  # ✅ transacción: commit al salir, rollback si falla
...         con.execute("INSERT INTO pagos VALUES ('PS-1017-G', 76000)")
... finally:
...     con.close()                # ✅ C11: el cierre, SIEMPRE explícito
...
```

Léelo así: el `with con:` administra **el trámite** (timbra o anula); el
`finally: con.close()` **cierra la caja**. Son dos responsabilidades distintas y
cada una tiene su herramienta. Así lo hacen las soluciones del curso — ábrelas y
compruébalo.

> 📝 **Alimenta la Pregunta 1:** además del commit, anota qué te devolvió el
> `SELECT` después del bloque `with` y qué te dice eso sobre la conexión.

### 🤖 Pregúntale a la IA

> *"¿Qué es ACID en bases de datos? Explícamelo con la analogía de una caja
> registradora que timbra o anula boletas."*

## ✅ Checkpoint

- [ ] Leíste `contribuyentes` con `sqlite3` (cursor) y con `pd.read_sql`.
- [ ] Demo 1: la fila SIN commit **no** estaba al reabrir (Pregunta 1).
- [ ] Demo 2: con `commit`, la fila persistió.
- [ ] Demo 3: un duplicado lanzó `IntegrityError` y lo manejaste con `rollback`.
- [ ] Comprobaste la trampa: tras `with sqlite3.connect(...)` la conexión SIGUE
      viva (C11), y usaste el patrón correcto `try: with con: … finally: con.close()`.

Cuando esté todo ✔, sigue con **[Guía 5 — El consolidado](05-consolidado.md)**.
