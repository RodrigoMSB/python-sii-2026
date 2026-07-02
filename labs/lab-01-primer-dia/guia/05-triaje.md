# Guía 5 — El triaje

> **Objetivo:** juntar todo lo aprendido para responderle a Don Arquímedes.
> Aquí eliges tu ruta (🛠️ Artesano o 🔎 Explorador), ejecutas el triaje y pasas
> el verificador. Es el día que el lab cobra sentido.

## Las dos piezas que faltan: `if` y `for`

### `if` — tomar decisiones (y la indentación como ley)

Un `if` ejecuta algo **solo si** una condición es verdadera:

```python
>>> estado = "VENCIDA"
>>> if estado == "VENCIDA":
...     print("¡A cobrar!")
...
¡A cobrar!
```

Fíjate en los **espacios** antes de `print`: eso es **indentación**, y en Python
**no es decoración, es sintaxis**. La sangría es la que dice "esto está *dentro*
del if". Piensa en el reglamento de tránsito: *"SI el semáforo está en rojo,
entonces detente"* — y todo lo que va "debajo del entonces" (con sangría) es lo
que haces cuando se cumple. Si te equivocas en la sangría, Python te reclama con
un `IndentationError`.

### `for` — recorrer, el gesto más importante del curso

Un `for` repite algo para **cada** elemento de una lista:

```python
>>> for patente in PATENTES:
...     print(patente[0])
...
PS-1001-G
PS-1002-C
... (y así las 24)
```

Combina `for` + `if` + una variable acumuladora y tienes el patrón
**recorrer-y-filtrar**, que es el 80% de este oficio:

```python
>>> total = 0
>>> for patente in PATENTES:
...     if patente[2] == "VIGENTE":
...         total = total + 1
...
>>> total
13
```

> 🌉 **Puente al Módulo 2:** esto que escribiste a mano —recorrer y filtrar— es
> exactamente lo que en pandas será `df[df["estado"] == "VIGENTE"]`. Hoy lo haces
> con `for` e `if`; mañana con una línea. Pero por dentro, es lo mismo. Por eso
> importa entenderlo ahora.

## Elige tu ruta

El programa que vas a completar/ejecutar se llama `triaje.py`. Cualquiera sea tu
ruta, primero **copia** el archivo a la raíz del lab.

### 🛠️ Ruta Artesano — tú escribes el código

Copia la **plantilla** (viene con 5 TODO para completar):

```bash
# macOS/Linux
cp plantillas/triaje.py triaje.py
```
```powershell
# Windows
Copy-Item plantillas\triaje.py triaje.py
```

Abre `triaje.py` y completa los TODO **en orden** (1 → 5). Tras cada uno puedes
ejecutar `uv run python triaje.py` y ver cómo el informe se corrige de a poco.
Las pistas están junto a cada TODO.

> ⏱️ **Regla de los 10 minutos.** ¿Trabado en una función más de 10 minutos? Abre
> `soluciones/triaje.py`, mira **SOLO esa función**, ciérrala y escríbela de
> memoria en tu archivo. No copies el archivo entero: recuperar el código es
> gratis; recuperar la comprensión, jamás.

### 🔎 Ruta Explorador — ejecutas y experimentas

Copia la **solución** ya hecha:

```bash
# macOS/Linux
cp soluciones/triaje.py triaje.py
```
```powershell
# Windows
Copy-Item soluciones\triaje.py triaje.py
```

Pero explorar **no es solo mirar**: es obligatorio que **modifiques y observes**.
Tu tarea mínima es la de la **Pregunta 5** (más abajo). Antes de cada ejecución,
predice qué va a pasar; luego compáralo con lo que salió.

## Ejecuta el triaje

Desde la raíz del lab:

```bash
uv run python triaje.py
```

**Salida esperada (Ruta Explorador, o Artesano ya completo):**

```
INFORME DE TRIAJE — Dirección de Rentas de Puerto Siracusa
==========================================================
Patentes registradas : 24
Patentes vigentes    : 13
Patentes vencidas    : 8
Deuda total          : $2350000 CLP

Detalle de patentes vencidas:
  - PS-1003-G
  - PS-1005-C
  - PS-1009-G
  - PS-1011-T
  - PS-1015-T
  - PS-1018-C
  - PS-1020-G
  - PS-1024-C

[INFO] Informe archivado en: salidas/informe_triaje.txt
```

Se creó también el archivo `salidas/informe_triaje.txt` con ese mismo informe.

### La zona gris, ahora con números

Mira el informe: **13 vigentes**, **8 vencidas**… y sin embargo hay **24**
patentes. Faltan 3: son las **SUSPENDIDAS** (Kayaks Bahía Serena, Botillería La
Sirena, Buceo Fondo Claro). No son vigentes ni vencidas: un tercer estado.

Y la **deuda total ($2.350.000)** suma la deuda de **todas**, incluidas las
vigentes que igual deben (como el Café La Palanca, $45.000). "Vigente" no
significa "sin deuda". Guarda esto para la Pregunta 3.

## 🔧 La modificación obligatoria (Pregunta 5)

En tu `triaje.py`, dentro de `codigos_vencidas`, cambia la condición:

```python
if patente[POS_ESTADO] == "VENCIDA":     # original
```
por
```python
if patente[POS_ESTADO] != "VIGENTE":     # experimento
```

Vuelve a ejecutar `uv run python triaje.py`. Observa cuántas patentes vencidas
reporta ahora y qué códigos aparecen **de más**. Piensa qué significan en
términos del municipio. Anótalo para la **Pregunta 5** y después **revierte** el
cambio (vuelve a dejar `== "VENCIDA"`) para que tu código quede correcto.

## Responde el interrogatorio

Copia el interrogatorio a la raíz y respóndelo con tus palabras:

```bash
# macOS/Linux
cp plantillas/RESPUESTAS.md RESPUESTAS.md
```
```powershell
# Windows
Copy-Item plantillas\RESPUESTAS.md RESPUESTAS.md
```

Abre `RESPUESTAS.md` y reemplaza cada `(escribe aquí tu respuesta)` por tu
explicación. Son 5 preguntas y todas dependen de lo que TÚ hiciste en tu
terminal.

## Verificación final

Con `triaje.py` funcionando, el informe generado y `RESPUESTAS.md` completo:

```bash
uv run python bin/verificar.py
```

**Meta:** `✔ 12/12 verificaciones correctas` y el mensaje de Don Arquímedes
archivando tu informe. Si te dice `11/12` por el interrogatorio, te faltó
responder algún marcador. Si falla algún cálculo, la pista te dice dónde mirar.

## 🏅 Desafío extra (opcional): el mayor deudor

¿Quieres más? Don Arquímedes pregunta cuál es la patente que **más debe**, y te
pide hacerlo **sin `max()`**, para que entiendas el patrón que hay debajo. La
solución comentada está en
[`../soluciones/desafio-mayor-deudor.md`](../soluciones/desafio-mayor-deudor.md).
(Pista: recorre recordando "el mayor visto hasta ahora".)

## ✅ Checkpoint final del Lab 01

- [ ] Entendiste `if` (con su indentación) y el patrón `for` + filtrar.
- [ ] Copiaste `triaje.py` a la raíz por tu ruta (🛠️ o 🔎).
- [ ] El triaje imprime `13` vigentes y `$2350000` de deuda total.
- [ ] Hiciste el experimento `!= "VIGENTE"` y lo revertiste (Pregunta 5).
- [ ] Respondiste las 5 preguntas de `RESPUESTAS.md`.
- [ ] El verificador dice `✔ 12/12`.

---

🎉 **¡Terminaste tu primer día en Rentas!** Aprendiste variables, tipos, cadenas,
listas y el patrón recorrer-y-filtrar; rompiste tres errores a propósito y
aprendiste a leerlos; y le entregaste a Don Arquímedes un informe de verdad.

> **Teaser — Lab 02:** el municipio digitalizó el padrón y ahora son **miles** de
> patentes en una planilla `.csv`. Cambiaremos las listas por **pandas**… pero el
> "recorrer y filtrar" de hoy será, palabra por palabra, lo mismo que harás allá.
> Nos vemos en el mesón. ⚓
