# Guía 5 — La consolidación

> **Objetivo:** juntar todo (diccionarios, funciones, excepciones) para construir
> `consolidar.py`, ejecutarlo, espiarlo con el depurador y pasar el verificador.

## Dos piezas de control que faltan: `while` y las comprensiones

### `while`, `break`, `continue`, `range()`

El `for` recorre una colección entera. El `while` repite **mientras** una
condición sea verdadera, y a veces quieres **parar antes** con `break`:

> 🔍 **Método nuevo:** `.isdigit()` es un método de las cadenas que responde
> `True` si el texto está formado **solo por dígitos** (`"200000".isdigit()` →
> `True`; `"200.000".isdigit()` → `False`, por el punto). Por eso primero se
> limpian los puntos con `.replace(".", "")` y recién después se pregunta si lo
> que queda es un número.

```python
>>> from datos.archivador import REGISTROS_BRUTOS
>>> i = 0
>>> while i < len(REGISTROS_BRUTOS):
...     registro = REGISTROS_BRUTOS[i]
...     if registro["deuda"].replace(".", "").isdigit() and int(registro["deuda"].replace(".", "")) > 200000:
...         print(f"Primera deuda grande: {registro['codigo']}")
...         break                      # encontrada: paramos de una
...     i = i + 1
...
Primera deuda grande: PS-1030-T
```

- `break` corta el bucle inmediatamente.
- `continue` salta al siguiente ciclo sin ejecutar lo que queda.
- `range(n)` genera números `0..n-1`, muy usado con `for`: `for i in range(3)`.

### Comprensiones de listas: el `for` de una línea

Prometido en la Guía 1. Una **comprensión** construye una lista en una sola línea.
Compara el bucle de siempre con su versión comprimida:

```python
>>> # El bucle clásico:
>>> codigos = []
>>> for r in REGISTROS_BRUTOS:
...     codigos.append(r["codigo"])
...
>>> # La comprensión equivalente:
>>> codigos = [r["codigo"] for r in REGISTROS_BRUTOS]
>>> len(codigos)
18
```

Se lee: *"`r["codigo"]` por cada `r` en los registros"*. Y admite filtro con `if`:

```python
>>> vigentes = [r["codigo"] for r in REGISTROS_BRUTOS if r["estado"] == "VIGENTE"]
>>> len(vigentes)
10
```

> ✋ **Regla de estilo:** si la comprensión no cabe **legible en una línea**, usa
> un `for` normal. La comprensión es para simplificar, no para lucirse.

### Y con llaves: la comprensión de **set**

Si cambias los corchetes `[...]` por llaves `{...}`, obtienes un **set** — o sea,
la misma comprensión pero **sin repetidos**:

```python
>>> len([r["codigo"] for r in REGISTROS_BRUTOS])   # lista: los 18, con el repetido
18
>>> len({r["codigo"] for r in REGISTROS_BRUTOS})   # set: solo los únicos
17
```

Es exactamente la línea que viste en la **Guía 1** y te prometí explicar aquí:
`{r["codigo"] for r in REGISTROS_BRUTOS}` recorre los registros, saca el código de
cada uno y **descarta los repetidos** en un solo gesto (18 → 17: `PS-1026-C`
estaba dos veces).

## Elige tu ruta

El programa se llama `consolidar.py`. Copia primero el archivo a la raíz del lab.

### 🛠️ Ruta Artesano — completas los TODO

```bash
cp plantillas/consolidar.py consolidar.py          # macOS/Linux
```
```powershell
Copy-Item plantillas\consolidar.py consolidar.py   # Windows
```
Completa los **6 TODO** en orden. Tras cada uno, ejecuta `uv run python
consolidar.py`. Ojo: al terminar el TODO 1, el programa **fallará** a propósito
con un registro "S/I" — esa es tu señal de que necesitas el `try/except` del
TODO 4. ¿Trabado >10 min? Mira SOLO esa función en `soluciones/consolidar.py`.

### 🔎 Ruta Explorador — ejecutas y experimentas

```bash
cp soluciones/consolidar.py consolidar.py          # macOS/Linux
```
```powershell
Copy-Item soluciones\consolidar.py consolidar.py   # Windows
```
Obligatorio: harás el experimento de la **Pregunta 5** (cambiar la regla de
duplicados) y la **sesión de pdb** de más abajo.

## Ejecuta la consolidación

Desde la raíz del lab:

```bash
uv run python consolidar.py
```

**Salida esperada (puede variar levemente):**

```
INFORME DE CONSOLIDACIÓN — Dirección de Rentas de Puerto Siracusa
==============================================================
Registros del archivador : 18
Fichas consolidadas      : 15
Registros rechazados     : 3
Deuda total consolidada  : $1,042,000 CLP

Deuda por rubro:
  C: $338,000 CLP
  G: $260,000 CLP
  T: $444,000 CLP

Rechazados (código → motivo):
  - PS-1029-C: deuda no numérica ('S/I')
  - PS-1026-C: código duplicado
  - PS-1036-T: deuda no numérica ('no informado')

[INFO] Informe archivado en: salidas/informe_consolidacion.txt
```

18 registros entraron; 15 quedaron como fichas y 3 fueron rechazados (2 por deuda
ilegible, 1 por código repetido). La deuda total suma **todas** las fichas
válidas, incluidas las **SUSPENDIDAS** (Miradores del Istmo y Tornería El Eje):
suspendida no significa "sin deuda". Guárdalo para la Pregunta 3.

## 🔎 Sesión guiada de pdb (el interrogatorio al programa)

Cuando algo "funciona pero no sabes por qué da eso", el depurador te deja
**congelar el tiempo** y mirar adentro. Vas a espiar el momento exacto en que un
registro sucio es rechazado.

1. En tu `consolidar.py`, dentro de la función `consolidar`, como **primera línea
   dentro del `for`**, agrega:
   ```python
       breakpoint()
   ```
2. Ejecuta `uv run python consolidar.py`. El programa se **detiene** y aparece el
   prompt `(Pdb)`.
3. Recorre con estos comandos:

   | Comando | Qué hace |
   |---------|----------|
   | `p registro` | imprime el registro actual del bucle |
   | `p registro["deuda"]` | imprime solo su deuda (la sospechosa) |
   | `n` | ejecuta la línea siguiente (*next*) |
   | `c` | continúa hasta el próximo `breakpoint()` (siguiente vuelta) |
   | `q` | sale del depurador |

4. Ve dando `c` y `p registro` en cada parada hasta llegar al registro
   **`PS-1029-C`**, cuya `deuda` es `"S/I"`. Ahí da `n` un par de veces y observa
   cómo el flujo entra al `except` y ese código va a `rechazos`. Ese es el momento
   exacto del rechazo.
5. Cuando termines, `q` para salir.

> ⚠️ **Quita el `breakpoint()`** apenas termines (contrato C8). Un `breakpoint()`
> olvidado deja el programa colgado esperando en el depurador. El verificador te
> avisará si detecta uno, pero mejor no dejarlo.

> 📝 **Pregunta 4** del interrogatorio: anota en qué registro estabas al entrar al
> `except` y qué comando de pdb usaste para inspeccionarlo.

## 🔧 La modificación obligatoria (Pregunta 5)

En `consolidar`, la regla actual hace ganar al **primero** (rechaza el duplicado
con `if codigo in fichero: ...`). Cámbiala para que gane el **último**: elimina
esa comprobación y deja que `fichero[codigo] = ficha` **sobrescriba** siempre.
Re-ejecuta y observa qué cambia en el informe (¿sigue habiendo un rechazo por
duplicado?). Piensa qué versión de la patente repetida queda registrada y por qué
importa en el municipio. Anótalo para la Pregunta 5 y **revierte**.

## Responde el interrogatorio y verifica

```bash
cp plantillas/RESPUESTAS.md RESPUESTAS.md          # macOS/Linux
```
```powershell
Copy-Item plantillas\RESPUESTAS.md RESPUESTAS.md   # Windows
```

Responde las 5 preguntas con tus palabras y luego:

```bash
uv run python bin/verificar.py
```

Meta: `✔ 11/11 verificaciones correctas` y el mensaje de Don Arquímedes. Si algo
falla, la pista te dice dónde mirar. (Si dejaste el `breakpoint()`, el verificador
no se cuelga, pero te lo recordará.)

## 🏅 Desafío extra (opcional): el podio de deudores

Arma el **top 3** de patentes que más deben del fichero consolidado, usando
`sorted` + `lambda` + slicing (Guía 3). La solución comentada está en
[`../soluciones/desafio-top-deudores.md`](../soluciones/desafio-top-deudores.md)
(el podio: Miradores del Istmo $290.000, Tornería El Eje $205.000, Paseos
Corriente Austral $154.000).

## ✅ Checkpoint final del Lab 02

- [ ] Entendiste `while`/`break`/`continue` y las comprensiones de lista.
- [ ] Copiaste `consolidar.py` a la raíz por tu ruta (🛠️ o 🔎).
- [ ] El informe muestra `15` fichas, `3` rechazados y `$1,042,000`.
- [ ] Hiciste la sesión de pdb y viste el rechazo del registro "S/I" en vivo.
- [ ] Hiciste el experimento de duplicados (Pregunta 5) y lo revertiste.
- [ ] Respondiste las 5 preguntas y el verificador dice `✔ 11/11`.

---

🎉 **¡El cuaderno creció y tú con él!** Manejaste diccionarios, tuplas y sets;
escribiste funciones de verdad; domaste datos sucios con excepciones e incluso tu
propio `RegistroInvalido`; y espiaste tu programa con pdb.

> **Teaser — Lab 03:** el puerto ya no quiere solo listas ordenadas: quiere
> **estadísticas** —promedios, máximos, percentiles de deuda sobre miles de
> patentes— y las quiere rápido. Ahí entra **NumPy**, y los números empiezan a
> volar. Nos vemos en el mesón. ⚓
