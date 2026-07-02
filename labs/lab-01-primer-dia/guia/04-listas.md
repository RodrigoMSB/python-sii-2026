# Guía 4 — Listas

> **Objetivo:** manejar la estructura estrella del lab. El cuaderno de patentes
> ES una lista de listas; aprender a recorrerla y consultarla es el corazón de
> todo lo que viene.

## Abre el cuaderno desde el REPL

Párate en la **raíz del lab** (`labs/lab-01-primer-dia/`) y abre el REPL:

```bash
uv run python
```

Ahora trae el cuaderno oficial a tu sesión:

```python
>>> from datos.cuaderno import PATENTES
>>> len(PATENTES)
24
```

`len()` cuenta cuántos elementos tiene una lista: 24 patentes. Cada patente es, a
su vez, **otra lista** de 4 posiciones `[codigo, nombre, estado, deuda]`. Es una
tabla antes de ser una tabla.

## Indexación (simple y doble)

```python
>>> PATENTES[0]
['PS-1001-G', 'Pescadería La Miríada', 'VIGENTE', 0]
>>> PATENTES[0][1]      # de la primera patente, la posición 1 (el nombre)
'Pescadería La Miríada'
```

`PATENTES[0]` te da la primera **fila**; `PATENTES[0][1]` baja un nivel y toma la
**columna** 1 de esa fila. Doble indexación = fila, luego columna.

### 🔮 Predice antes de ejecutar

Anota tu predicción: ¿qué crees que devuelve `PATENTES[2][2]`?

```python
>>> PATENTES[2][2]
```

<details>
<summary>Ver respuesta</summary>

Devuelve `'VENCIDA'`. `PATENTES[2]` es la **tercera** patente (Cocinería Doña
Eureka; recuerda: se cuenta desde 0), y `[2]` de esa fila es la posición del
**estado**. ¿Acertaste con el "tercera" y no "segunda"? Ese desfase de 1 es el
que hay que domar.
</details>

## Slicing de listas

Igual que con el texto, `[desde:hasta]` saca un trozo (hasta excluyente):

```python
>>> PATENTES[0:3]        # las tres primeras patentes
[['PS-1001-G', ...], ['PS-1002-C', ...], ['PS-1003-G', ...]]
```

## Construir tu propia lista con `append`

Las listas crecen por el final con `.append(...)`. Vas a armar una **bandeja** de
códigos a mano:

```python
>>> bandeja = []                     # una lista vacía
>>> bandeja.append("PS-1003-G")
>>> bandeja.append("PS-1005-C")
>>> bandeja
['PS-1003-G', 'PS-1005-C']
```

Este patrón —empezar con `[]` y `append` dentro de un recorrido— es exactamente
lo que hará tu función `codigos_vencidas` en la Guía 5.

## Ordenar: `sort()` vs `sorted()`

Dos formas de ordenar, y la diferencia importa:

```python
>>> numeros = [310000, 45000, 127500]
>>> sorted(numeros)          # DEVUELVE una lista nueva ordenada
[45000, 127500, 310000]
>>> numeros                  # ...y deja la original intacta
[310000, 45000, 127500]
>>> numeros.sort()           # ordena LA MISMA lista (in-place), no devuelve nada
>>> numeros
[45000, 127500, 310000]
```

- `sorted(x)` → te da una **copia** ordenada; `x` no cambia.
- `x.sort()` → cambia **`x` mismo** y devuelve `None`.

## Herramientas de resumen

```python
>>> deudas = [185000, 92000, 127500]
>>> sum(deudas)
404500
>>> max(deudas)
185000
>>> deudas.reverse()      # da vuelta la lista (in-place)
>>> deudas
[127500, 92000, 185000]
```

## Pertenencia: `in` y `not in`

Preguntar si algo está en una lista es directísimo:

```python
>>> "PS-1003-G" in bandeja
True
>>> "PS-1099-Z" in bandeja
False
>>> "PS-1099-Z" not in bandeja
True
```

### 🔮 El ejercicio de la Pregunta 4

Arma a mano la lista de **vencidas** (cópiala tal cual) y luego **predice** el
resultado antes de ejecutar la última línea:

```python
>>> vencidas = ["PS-1003-G", "PS-1005-C", "PS-1009-G", "PS-1011-T",
...             "PS-1015-T", "PS-1018-C", "PS-1020-G", "PS-1024-C"]
>>> "PS-1013-C" in vencidas          # <- predice: ¿True o False?
```

<details>
<summary>Ver respuesta</summary>

Da `False`. La Botillería La Sirena (`PS-1013-C`) está **SUSPENDIDA**, no
**VENCIDA**, así que no está en la lista de vencidas. Si predijiste `True`
porque "debe plata", caíste justo en la zona gris: suspendida ≠ vencida.
</details>

> 📝 **Anota tu predicción y el resultado**: son la materia prima de la
> Pregunta 4.

## 💥 La trampa del alias (el error que un día te costará horas)

Recuerda de la Guía 2: una variable es una **etiqueta**, no una caja. Mira qué
pasa si le pones **dos etiquetas al mismo dato**:

```python
>>> original = ["PS-1003-G", "PS-1005-C"]
>>> copia = original            # ¿copia... o segunda etiqueta?
>>> copia.append("PS-9999-X")
>>> copia
['PS-1003-G', 'PS-1005-C', 'PS-9999-X']
>>> original
['PS-1003-G', 'PS-1005-C', 'PS-9999-X']    # 😱 ¡también cambió!
```

`copia = original` **no** copió la lista: le puso una **segunda llave a la misma
bodega**. Cualquiera de las dos llaves abre —y desordena— la misma bodega. Para
tener una bodega **aparte** usa `.copy()`:

```python
>>> original = ["PS-1003-G", "PS-1005-C"]
>>> copia = original.copy()     # bodega nueva, contenido igual
>>> copia.append("PS-9999-X")
>>> original
['PS-1003-G', 'PS-1005-C']      # 😌 intacta
```

### 🤖 Pregúntale a la IA

> *"Dibújame con texto un diagrama de memoria que muestre la diferencia entre
> `copia = original` y `copia = original.copy()` en Python, con dos etiquetas
> apuntando a listas."*

## ✅ Checkpoint

- [ ] Importaste `PATENTES` y usaste `len`, indexación simple y doble.
- [ ] Predijiste `PATENTES[2][2]` y armaste una `bandeja` con `append`.
- [ ] Distinguiste `sort()` (in-place) de `sorted()` (copia).
- [ ] Probaste `in`/`not in` y anotaste la predicción de la Pregunta 4.
- [ ] Reprodujiste la trampa del alias y la arreglaste con `.copy()`.

Cuando esté todo ✔, sigue con **[Guía 5 — El triaje](05-triaje.md)**.
