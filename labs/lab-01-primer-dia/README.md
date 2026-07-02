# Lab 01 — El primer día en Rentas ⚓

> Módulo 1 del curso · ~2,5 horas · **sin conocimientos previos** · 100 %
> biblioteca estándar (no instalarás ninguna librería).

## El encargo

Eres el nuevo **Analista de Datos** de la **Dirección de Rentas de Puerto
Siracusa**. Don Arquímedes, treinta años en la oficina, te recibe con el cuaderno
de patentes del puerto y un encargo:

> «Dame una planilla limpia y un punto de apoyo, y moveré el presupuesto
> municipal. Pero primero necesito un **triaje**: de todas las patentes, dime
> cuántas están vigentes, cuáles están vencidas y cuánta plata se debe en total.»

Al terminar este lab habrás construido (o ejecutado y desarmado) el programa que
responde exactamente eso, y le habrás entregado a Don Arquímedes su informe.

## Qué vas a aprender

Variables y tipos (`str`, `int`, `float`, `bool`) · operaciones aritméticas, de
comparación y lógicas · cadenas: indexación, slicing, métodos y f-strings ·
listas: `append`, `sort`/`sorted`, `sum`/`max`, pertenencia (`in`) y la trampa
del alias · `if` y `for`: el patrón **recorrer-y-filtrar** que es la base de todo
lo que viene (incluido pandas en el Módulo 2).

## Dos rutas, un mismo verificador

Elige cómo recorrer el lab. Las dos terminan pasando el mismo `bin/verificar.py`.

| Ruta | Para quién | Qué haces |
|------|------------|-----------|
| 🛠️ **Artesano** | Quiero escribir el código | Completas los 5 `TODO` de `plantillas/triaje.py`. |
| 🔎 **Explorador** | Quiero entender leyendo y probando | Ejecutas `soluciones/triaje.py`, pero **predices y modificas** obligatoriamente (Pregunta 5). |

## La regla de la casa (sobre la IA) 🤖

La IA está **invitada**, no prohibida. Úsala para que te **explique** lo que no
entiendas: verás cápsulas 🤖 con prompts sugeridos. Pero la meta es **entender,
no repetir**: por eso el interrogatorio (`RESPUESTAS.md`) pregunta por lo que
pasó en **TU** terminal y por decisiones que **TÚ** tomaste. Ese pensamiento no
se puede copiar y pegar.

## Prerrequisitos

Solo **`uv`** (gestor de entorno y de Python). No necesitas instalar Python: uv
trae el 3.13 que usa el lab. Instalación en
[`../../docs/setup-alumno.md`](../../docs/setup-alumno.md) y, ante problemas,
[`docs/troubleshooting.md`](docs/troubleshooting.md).

## Mapa de las guías

Recórrelas en orden; cada una termina con un ✅ Checkpoint.

1. **[Guía 1 — Tu primer día en Rentas](guia/01-contexto.md)** — montar el
   entorno (`uv`), la regla de oro `uv run`, saludo al REPL.
2. **[Guía 2 — Variables y tipos](guia/02-variables-y-tipos.md)** — tipos,
   operadores, y tu primer error a propósito (`TypeError`).
3. **[Guía 3 — Cadenas](guia/03-cadenas.md)** — anatomía del código de patente,
   indexación, slicing, métodos, f-strings.
4. **[Guía 4 — Listas](guia/04-listas.md)** — el cuaderno como lista de listas,
   `append`, orden, pertenencia y la trampa del alias.
5. **[Guía 5 — El triaje](guia/05-triaje.md)** — `if` y `for`, eliges ruta,
   ejecutas y pasas el verificador.

## Convención de bloques y cápsulas

- **Comando que ejecutas** vs **Salida esperada (puede variar levemente)**:
  los primeros los escribes tú; la segunda es lo que deberías ver (pequeñas
  diferencias de formato son normales).
- 🔮 **Predice**: anota tu predicción *antes* de ejecutar; aprender es comparar.
- 💥 **Rómpelo**: provocamos un error a propósito para aprender a leerlo.
- 🤖 **Pregúntale a la IA**: prompt sugerido para profundizar.

## Verifica tu trabajo

Desde la raíz del lab (`labs/lab-01-primer-dia/`):

```bash
uv run python bin/verificar.py
```

La meta es `✔ 12/12 verificaciones correctas`. El verificador es de **solo
lectura** y usa un **cuaderno sorpresa aleatorio** además del oficial: si tu
código funciona de verdad, pasa con ambos; si copiaste los números, el sorpresa
te delata.

## Para el instructor 🧑‍🏫

- **Recuperar a un rezagado** (repone `triaje.py` y `salidas/`, copia el
  interrogatorio en blanco pero **no** lo responde):
  ```bash
  uv run python bin/recuperar_lab.py
  ```
  Tras recuperar, el lab queda en `11/12` a propósito: el interrogatorio se gana
  pensando.
- **Cifras de control** del cuaderno oficial: 24 patentes · 13 vigentes ·
  8 vencidas · 3 suspendidas · deuda total **$2.350.000** · mayor deudor
  *Buceo Fondo Claro* ($520.000).
- Todo `bin/` es **solo lectura** sobre el trabajo del alumno (salvo
  `recuperar_lab.py`) y 100 % stdlib.
