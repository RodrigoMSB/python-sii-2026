# Lab 02 — El cuaderno crece ⚓

> Módulo 1 (segunda mitad) · ~2,5 horas · continúa el Lab 01 · 100 % biblioteca
> estándar (no instalarás ninguna librería).

## El encargo

Apareció el **archivador antiguo** de la Dirección de Rentas: patentes que nunca
se digitalizaron, transcritas a la carrera. Vienen sucias —deudas escritas como
texto con puntos, registros "S/I", una patente pegada dos veces— y Don Arquímedes
te pide consolidarlas en un fichero limpio **sin que el programa se caiga** con el
primer dato malo.

> «Lo que sirve, adentro; lo que no, afuera pero anotado. Así se ordena un
> archivo.» — Don Arquímedes

Construirás `consolidar.py`: normaliza deudas, rechaza lo ilegible y lo duplicado,
consolida los válidos en un diccionario y arma el informe de consolidación.

## Qué vas a aprender

Tuplas, sets y **diccionarios** (el fichero indexado por código) · `while`,
`break`, `continue`, `range` · **comprensiones** de lista · **funciones** de
verdad (parámetros por defecto, `*args`/`**kwargs`, lambdas, funciones como
objetos, scope) · **excepciones** (`try/except/else/finally`, tu propia
`RegistroInvalido`) · depuración con **pdb** vía `breakpoint()`.

## Dos rutas, un mismo verificador

| Ruta | Para quién | Qué haces |
|------|------------|-----------|
| 🛠️ **Artesano** | Quiero escribir el código | Completas los 6 `TODO` de `plantillas/consolidar.py`. |
| 🔎 **Explorador** | Quiero entender leyendo y probando | Ejecutas `soluciones/consolidar.py`, pero **predices, depuras con pdb y modificas** (Pregunta 5). |

## La regla de la casa (sobre la IA) 🤖

La IA está **invitada**, no prohibida: úsala para que te explique conceptos. Pero
el interrogatorio (`RESPUESTAS.md`) pregunta por lo que pasó en **TU** terminal
(tu `KeyError`, tu sesión de pdb, tus números): eso se entiende, no se copia.

## Prerrequisitos

Solo **`uv`** (trae Python 3.13; no instalas Python). Instalación en
[`../../docs/setup-alumno.md`](../../docs/setup-alumno.md); problemas en
[`docs/troubleshooting.md`](docs/troubleshooting.md). Se recomienda haber hecho el
Lab 01.

## Mapa de las guías

1. **[Guía 1 — El archivador antiguo](guia/01-contexto.md)** — entorno, **tuplas**
   (inmutables) y **sets** (unicidad).
2. **[Guía 2 — Diccionarios](guia/02-diccionarios.md)** — el dolor de buscar en
   listas → el dict como fichero; `[]` vs `.get()` y el `KeyError`.
3. **[Guía 3 — Funciones](guia/03-funciones.md)** — `def`, defaults, `*args`,
   lambdas, funciones como objetos, scope.
4. **[Guía 4 — Excepciones](guia/04-excepciones.md)** — datos sucios,
   `try/except/else/finally` y tu propia `RegistroInvalido`.
5. **[Guía 5 — La consolidación](guia/05-consolidacion.md)** — `while`,
   comprensiones, construir/ejecutar `consolidar.py`, **sesión de pdb** y
   verificación final.

## Convención de bloques y cápsulas

- **Comando que ejecutas** vs **Salida esperada (puede variar levemente)**.
- 🔮 **Predice** antes de ejecutar · 💥 **Rómpelo** (error a propósito) ·
  🤖 **Pregúntale a la IA**.

## Verifica tu trabajo

Desde la raíz del lab (`labs/lab-02-cuaderno-crece/`):

```bash
uv run python bin/verificar.py
```

Meta: `✔ 11/11 verificaciones correctas`. El verificador es de **solo lectura**,
usa un **archivador sorpresa aleatorio** (con datos sucios y un duplicado) además
del oficial, y **neutraliza** cualquier `breakpoint()` olvidado sin colgarse.

## Para el instructor 🧑‍🏫

- **Recuperar a un rezagado** (repone `consolidar.py` y `salidas/`, copia el
  interrogatorio en blanco sin responder):
  ```bash
  uv run python bin/recuperar_lab.py
  ```
- **Cifras de control:** 18 registros brutos → 15 fichas · 3 rechazos (2 deuda no
  numérica: PS-1029-C, PS-1036-T; 1 duplicado: PS-1026-C, gana el primero) · deuda
  total **$1.042.000** · por rubro C=$338.000 / G=$260.000 / T=$444.000 · top
  deudor *Miradores del Istmo* ($290.000).
- Todo `bin/` es **solo lectura** sobre el trabajo del alumno (salvo
  `recuperar_lab.py`) y 100 % stdlib. Ningún `breakpoint()` en soluciones,
  plantillas ni bin (C8).
