# Lab 03 — Los números del puerto ⚓

> Módulo 2 (primera mitad) · ~2,0 horas · **primer lab con bibliotecas
> externas** (numpy, pandas) · requiere Internet la primera vez.

## El encargo

El Concejo Municipal le pidió a Don Arquímedes el **panorama anual de
recaudación** del puerto: 12 meses × 3 rubros, "con totales por donde se mire".
Hacerlo con listas y bucles (Labs 01–02) se vuelve un enredo. Es hora de la
herramienta profesional: **NumPy** para los números en bloque y **pandas** para
las tablas con nombre.

> «Doce meses, tres rubros, y lo quieren con totales por donde se mire.» — Don
> Arquímedes

Construirás `panorama.py`: totales por mes y por rubro, mes récord, meses flojos
y una proyección de reajuste (NumPy), más un resumen de morosidad del cuaderno de
patentes del Lab 01 (pandas).

## Qué vas a aprender

**NumPy:** `ndarray`, `shape`/`dtype`, indexación y slicing 2D, vectorización y
**broadcasting**, agregaciones con `axis`, `argmax`, **máscaras booleanas**.
**pandas:** `Series` y `DataFrame`, `head`/`info`/`dtypes`, `loc`/`iloc`,
filtrado booleano, columnas derivadas, `value_counts` y `describe`.

## Dos rutas, un mismo verificador

| Ruta | Para quién | Qué haces |
|------|------------|-----------|
| 🛠️ **Artesano** | Quiero escribir el código | Completas los 6 `TODO` de `plantillas/panorama.py`. |
| 🔎 **Explorador** | Quiero entender leyendo y probando | Ejecutas `soluciones/panorama.py`, con predicción y modificación obligatorias (Pregunta 5). |

## La regla de la casa (sobre la IA) 🤖

La IA está **invitada**: úsala para que te explique el `axis`, el broadcasting o
un error. Pero el interrogatorio pregunta por lo que pasó en **TU** terminal (tu
máscara, tu `ValueError`, tu `iloc[6]`): eso se entiende, no se copia.

## Prerrequisitos

- **`uv`** (trae Python 3.13). Instalación:
  [`../../docs/setup-alumno.md`](../../docs/setup-alumno.md).
- **Internet** la primera vez (el preparador descarga numpy y pandas).
- Se recomienda haber hecho los Labs 01 y 02.

Problemas de red/proxy/antivirus en la descarga:
[`docs/troubleshooting.md`](docs/troubleshooting.md).

## Mapa de las guías

1. **[Guía 1 — La planilla del Concejo](guia/01-contexto.md)** — entorno (con
   descarga de bibliotecas) y el porqué de NumPy (vectorización).
2. **[Guía 2 — Arrays](guia/02-arrays.md)** — `shape`, indexación 2D, `axis` (el
   eje que colapsa), `argmax`.
3. **[Guía 3 — Vectorización](guia/03-vectorizacion.md)** — broadcasting,
   máscaras booleanas y el `ValueError` "truth value ambiguous".
4. **[Guía 4 — DataFrames](guia/04-dataframes.md)** — pandas, el cuaderno del Lab
   01 como tabla, `loc`/`iloc`, filtrado.
5. **[Guía 5 — El panorama](guia/05-panorama.md)** — construir/ejecutar
   `panorama.py` y verificación final.

## Convención de bloques y cápsulas

**Comando que ejecutas** vs **Salida esperada (puede variar levemente)**;
🔮 **Predice** · 💥 **Rómpelo** · 🤖 **Pregúntale a la IA**.

## Verifica tu trabajo

Desde la raíz del lab (`labs/lab-03-numeros-del-puerto/`):

```bash
uv run python bin/verificar.py
```

Meta: `✔ 13/13 verificaciones correctas`. El verificador es de **solo lectura**,
prueba con datos **oficiales y sorpresa** (matriz y cuaderno aleatorios), compara
floats con tolerancia y neutraliza cualquier `breakpoint()` olvidado.

## Para el instructor 🧑‍🏫

- **Recuperar a un rezagado:** `uv run python bin/recuperar_lab.py` (repone
  `panorama.py` y `salidas/`, interrogatorio en blanco).
- **Cifras de control:** total anual **$90.680.000** · por rubro C=$48.480.000,
  G=$34.090.000, T=$8.110.000 · mes récord Diciembre ($9.140.000) · meses bajo
  $6.500.000: Junio, Julio · reajuste 4 % → $94.307.200 · morosidad del cuaderno:
  8 vencidas, $976.000.
- **Dependencias pineadas:** `numpy==2.5.0`, `pandas==3.0.3` (`uv.lock`
  versionado). Nota: pandas 3.0.4 fue *yanked* de PyPI (segfaults en datetime,
  no usado aquí); se fijó la 3.0.3. Ver `docs/troubleshooting.md`.
- `bin/` solo lectura (salvo `recuperar_lab.py`); sin `breakpoint()` en
  soluciones/plantillas/bin (C8).
