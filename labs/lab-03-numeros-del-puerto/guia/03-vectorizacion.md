# Guía 3 — Vectorización y máscaras

> **Objetivo:** operar sobre toda la matriz de un golpe (broadcasting) y
> seleccionar datos con máscaras booleanas. Aquí vive el error más googleado de
> NumPy.

REPL abierto, `import numpy as np`, `m = np.array(RECAUDACION)`.

## Broadcasting: un escalar toca cada celda

El Concejo aprobó un **reajuste del 4 %** para el próximo año. ¿Cómo proyectas
toda la planilla? Sin bucles:

```python
>>> m * 1.04
array([[4284800., 3515200., 1196000.],
       ...
       [4669600., 3702400., 1133600.]])
```

`m * 1.04` multiplicó **cada una de las 36 celdas** por 1.04, de una vez. A eso
—que un solo número (escalar) se "reparta" sobre todo el array— se le llama
**broadcasting**. No hiciste un `for`; NumPy lo aplicó a todo el bloque.

```python
>>> (m * 1.04).sum()      # el total anual reajustado
94307200.0
```

Ese es el TODO... bueno, es `proyectar_reajuste(m, 0.04)`. Una línea.

## Máscaras booleanas: preguntar a todo el array

Una comparación sobre un array devuelve **otro array**, de `True`/`False`, uno
por elemento:

```python
>>> por_mes = m.sum(axis=1)
>>> por_mes < 6_500_000
array([False, False, False, False, False,  True,  True, False,
       False, False, False, False])
```

Esa fila de `True`/`False` es una **máscara**. Cada posición responde "¿este mes
recaudó menos que el umbral?".

### 🔮 Predice antes de ejecutar

Antes de usar la máscara para sacar los nombres, **predice**: ¿qué meses crees
que quedarán por debajo de $6.500.000? Anótalo. Luego:

```python
>>> from datos.recaudacion import MESES
>>> [MESES[i] for i, bajo in enumerate(por_mes < 6_500_000) if bajo]
['Junio', 'Julio']
```

<details>
<summary>Ver respuesta</summary>

Junio ($6.150.000) y Julio ($6.350.000): los dos meses de pleno invierno, cuando
el Turismo casi desaparece. ¿Acertaste tu predicción? Guárdala: es la Pregunta 2
del interrogatorio.
</details>

> 💡 La máscara también se puede usar directo para filtrar el array:
> `por_mes[por_mes < 6_500_000]` te da los **valores** (no los nombres) de esos meses.

## Combinar condiciones: `&` y `|` (¡con paréntesis!)

Para "esto Y aquello" sobre arrays se usa `&` (y), `|` (o), `~` (no) — **no** las
palabras `and`/`or`. Y cada condición va **entre paréntesis**:

```python
>>> turismo = m[:, 2]
>>> comercio = m[:, 0]
>>> (turismo > 500_000) & (comercio > 4_000_000)
array([ True, False,  True, False, False, False, False, False,
        True,  True,  True,  True])
```

Meses con Turismo alto **y** Comercio alto: casi todos los del segundo semestre
(y el arranque del año). Fíjate en Febrero (`False`): tiene buen Turismo, pero su
Comercio ($3.950.000) quedó justo por debajo del corte de $4.000.000. Las dos
condiciones deben cumplirse **a la vez**.

## 💥 Rómpelo: el error MÁS googleado de NumPy

¿Qué pasa si usas `and` en vez de `&`?

```python
>>> (turismo > 500_000) and (comercio > 4_000_000)
```
```
ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
```

Léelo con calma. `and` necesita decidir si algo es **verdadero o falso** como un
todo. Pero acá le diste un **array de 12 valores** (unos `True`, otros `False`):
¿el conjunto es "verdadero"? ¿Si TODOS lo son? ¿Si ALGUNO lo es? NumPy no
adivina: es **ambiguo**, y por eso se planta y te dice "usa `.any()` o `.all()`".
La solución para combinar máscaras es `&`/`|` con paréntesis, que operan
elemento a elemento.

> 📝 **Pregunta 3** del interrogatorio: copia la última línea de ESTE error y
> explica por qué NumPy no puede decidir solo.

## Bonus: `np.where`

`np.where(condición, a, b)` elige `a` donde la condición es `True` y `b` donde es
`False` — un "if vectorizado":

```python
>>> np.where(por_mes < 6_500_000, "FLOJO", "OK")
array(['OK', 'OK', 'OK', 'OK', 'OK', 'FLOJO', 'FLOJO', 'OK', 'OK',
       'OK', 'OK', 'OK'], dtype='<U5')
```

### 🤖 Pregúntale a la IA

> *"En NumPy, ¿qué reglas exactas sigue el broadcasting para decidir si dos arrays
> de formas distintas se pueden operar? Dame un caso que funciona y uno que lanza
> ValueError, con la explicación de por qué."*

## ✅ Checkpoint

- [ ] Aplicaste el reajuste con `m * 1.04` (broadcasting, sin bucle).
- [ ] Construiste una máscara `por_mes < 6_500_000` y sacaste los nombres.
- [ ] Predijiste los meses bajo umbral (Pregunta 2).
- [ ] Combinaste condiciones con `&` y paréntesis.
- [ ] Provocaste el `ValueError` "truth value ambiguous" y lo entendiste.

Cuando esté todo ✔, sigue con **[Guía 4 — DataFrames](04-dataframes.md)**.
