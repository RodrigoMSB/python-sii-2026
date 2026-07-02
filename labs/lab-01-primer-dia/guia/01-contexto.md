# Guía 1 — Tu primer día en Rentas

> **Objetivo:** montar tu taller de trabajo (el entorno) y saludar a Python por
> primera vez. Al terminar tendrás el lab listo y habrás ejecutado tus primeras
> instrucciones.

## El encargo

Son las 8:45 de la mañana. Llegas a la **Dirección de Rentas de Puerto
Siracusa**, un municipio costero de esos donde todos se conocen. Te reciben con
un café tibio y un escritorio que huele a papel viejo.

Detrás de una pila de carpetas aparece **Don Arquímedes**, treinta años en
Rentas, anteojos en la punta de la nariz:

> «Así que tú eres el nuevo analista de datos. Mira, yo con los números me
> defiendo, pero esto de los *computadores* me supera. Tengo aquí el cuaderno de
> patentes del puerto y necesito que le saques cuentas. Pero antes… ¿sabes
> siquiera prender esta cosa? Empecemos por el principio.»
>
> «Dame una planilla limpia y un punto de apoyo, y moveré el presupuesto
> municipal.»

Ese "empezar por el principio" es esta guía.

## El taller aislado (qué es el entorno virtual)

Antes de tocar los datos, montamos tu **taller**.

Imagina que en Rentas te asignan un **mesón de trabajo aislado**: tiene tus
herramientas, tu versión de las cosas, y nadie más las toca. Si el mesón del
vecino usa un martillo distinto, no te importa: el tuyo es tuyo. Cuando termines
el trabajo, guardas el mesón y el resto de la oficina quedó intacta.

Eso es un **entorno virtual**: una carpeta aislada (`.venv/`) con **su propia
versión de Python** y sus propias herramientas, separada del resto de tu
computador. Cada laboratorio tiene el suyo. Así, lo que instales para un
proyecto nunca rompe otro.

La herramienta que arma y administra ese mesón se llama **`uv`**. Si aún no la
tienes instalada, ve a [`../docs/setup-alumno.md`](../docs/setup-alumno.md) y
vuelve aquí.

## Montar el taller

Abre una terminal, entra a la carpeta del lab y corre el **preparador** según tu
sistema. Es idempotente: puedes correrlo las veces que quieras.

**Comando que ejecutas (macOS/Linux):**

```bash
cd labs/lab-01-primer-dia
bash bin/00-preparar.sh
```

**Comando que ejecutas (Windows / PowerShell):**

```powershell
cd labs\lab-01-primer-dia
powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
```

**Salida esperada (puede variar levemente):**

```
[OK] uv encontrado: /.../uv
[INFO] Sincronizando el entorno (uv se encarga de traer Python 3.13)…
[OK] Entorno .venv/ listo.

Verificación de entorno — Lab 01
════════════════════════════════
[OK] Python en ejecución: 3.13 (correcto).
[OK] uv disponible en el PATH (...).
[OK] El entorno virtual .venv/ existe.
[OK] La estructura de carpetas del lab está completa.
[OK] El cuaderno de datos (datos/cuaderno.py) está presente.

✔ 5/5 verificaciones correctas
```

¿Viste `✔ 5/5`? El taller está montado. ¿Algo en rojo? Ve a
[`../docs/troubleshooting.md`](../docs/troubleshooting.md); ahí está la cura.

## La regla de oro: `uv run`

De aquí en adelante, **todo** comando de Python del curso empieza con `uv run`:

```bash
uv run python triaje.py
```

¿Por qué? Porque `uv run` usa el Python de **tu taller** (el 3.13 aislado), no
el que ande dando vueltas por el sistema. Si algún día ves un error raro de
versión, lo primero que revisas es: *"¿le puse `uv run` adelante?"*.

> 🧭 **Siempre desde la raíz del lab.** Todos los comandos se ejecutan parado en
> `labs/lab-01-primer-dia/` (donde está `triaje.py` y la carpeta `datos/`). Si te
> paras en otra carpeta, Python no encontrará los datos. Lo veremos en carne
> propia más adelante.

## Saludo a Python (el REPL)

El **REPL** es una consola interactiva donde escribes una línea de Python y te
responde al toque. Es tu libreta de borrador. Ábrela así:

**Comando que ejecutas:**

```bash
uv run python
```

Verás un *prompt* con `>>>`. Prueba, línea por línea:

```python
>>> print("Hola, Puerto Siracusa")
Hola, Puerto Siracusa
>>> 45000 + 18000 + 76000
139000
>>> 2350000 / 8
293750.0
```

Fíjate en un detalle que retomaremos: `139000` (una suma de enteros) salió sin
punto decimal, pero `2350000 / 8` salió como `293750.0`, **con** punto. La
división en Python siempre entrega decimales. Guárdalo en la memoria.

**Para salir del REPL** escribe `exit()` y presiona Enter (o `Ctrl-D` en
macOS/Linux, `Ctrl-Z` y Enter en Windows).

## ✅ Checkpoint

Antes de pasar a la Guía 2, confirma que:

- [ ] El preparador terminó en `✔ 5/5 verificaciones correctas`.
- [ ] Entraste al REPL con `uv run python` y viste el `>>>`.
- [ ] Hiciste que Python imprimiera algo y sumara números.
- [ ] Supiste salir del REPL.

Cuando todo esté ✔, sigue con **[Guía 2 — Variables y tipos](02-variables-y-tipos.md)**.
