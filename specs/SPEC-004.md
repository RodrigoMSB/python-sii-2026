# SPEC-004 — Lab 03: "Los números del puerto"

> **Proyecto:** Curso Programación en Python — SII 2026 · "Puerto Siracusa"
> **Emitido por:** El Arquitecto (Claude) · **Aprobado por:** Rodrigo Silva Bravo (PO)
> **Ejecutor:** mocito (Claude Code) — dueño del repositorio y único constructor
> **Fecha:** 2026-07-02 · **Versión:** 1.0
> **Dependencias:** repo con tags `lab-01-v1.0.0` y `lab-02-v1.0.0` (SPEC-002/003 completados)

> **⚠️ Nota del ejecutor (mocito) — Hallazgo H-03, pendiente de ratificación del Arquitecto:**
> El pin `pandas==3.0.4` de este spec resultó estar **YANKED en PyPI** al momento de
> construir (motivo: "Reported segfaults with datetime-related functionality"). El lab NO
> usa datetime y funciona idéntico, pero se fijó `pandas==3.0.3` (última 3.0.x estable, misma
> API moderna) para no emitir a los alumnos una dependencia retirada con warning. `numpy==2.5.0`
> se mantiene. Detalle en `labs/lab-03-numeros-del-puerto/docs/certificacion-lab-03.md`. El texto
> del Arquitecto se conserva verbatim más abajo (dice 3.0.4).

---

## ⚠️ 0. Verificación del Arquitecto (leer PRIMERO)

**Premisas verificadas por el Arquitecto:**
- ✅ **Versiones a pinear, verificadas contra PyPI el 2026-07-02:**
  `numpy==2.5.0` (liberada 2026-06-21, soporta Python 3.13) y
  `pandas==3.0.4` (liberada 2026-06-28, serie 3.0 soporta Python ≥3.11).
  **Nota mayor:** pandas 3.0 es la nueva major (2026-01) — trae string dtype
  por defecto y Copy-on-Write activado. El lab enseña la API moderna; nada
  de patrones legacy (`inplace=True` se evita, encadenamiento con CoW en
  mente).
- ✅ **Cifras de control computadas y validadas** con la matriz §5.1:
  total anual $90.680.000 · por rubro C=$48.480.000, G=$34.090.000,
  T=$8.110.000 · mes récord: Diciembre ($9.140.000) · mes mínimo: Junio
  ($6.150.000) · meses bajo umbral $6.500.000: Junio y Julio · reajuste 4 %
  del total anual: $94.307.200. Y con el cuaderno del Lab 01 (§5.2):
  vencidas = 8 patentes, deuda vencida total = $976.000.
- ✅ Spec autosuficiente: sin artefactos externos.
- ✅ Alcance cruzado contra el temario: primera mitad del **Módulo 2**
  (NumPy matricial + introducción a Pandas/DataFrames). La carga de
  archivos/BD y exportación quedan para el Lab 04, como corresponde.

**Supuestos a validar por el PO o mocito ANTES de ejecutar:**
1. Repo en `main`, limpio y sincronizado; Labs 01 y 02 certificados intactos.
2. **Conexión a Internet disponible** durante `uv sync` de este lab (primera
   vez descarga numpy/pandas). En la máquina del PO ya hubo red; para las
   máquinas de alumnos, el troubleshooting cubre proxys/antivirus (§10).
3. `uv`, `git`, `gh` operativos (sin cambios desde SPEC-003).

---

## 1. Contexto y narrativa del lab

Don Arquímedes vuelve del Concejo Municipal con una planilla y cara de
urgencia: le pidieron el **panorama anual de recaudación** del puerto —
12 meses × 3 rubros — y lo necesita "con totales por donde se mire".

El dolor pedagógico: intentar esos totales con listas de listas y bucles
(lo aprendido en Labs 01–02) funciona... pero duele. Ahí entra **NumPy**:
la recaudación como **matriz**, y los totales como operaciones de UNA
línea. Después, el puente natural: "¿y si las filas tuvieran nombre?" →
**pandas DataFrame**, reencontrándose con el viejo cuaderno de patentes
del Lab 01, ahora como tabla con esteroides.

Misión: construir `panorama.py` — el programa que entrega el panorama
anual (NumPy) y el resumen de morosidad del cuaderno (pandas), y lo deja
por escrito para el Concejo.

## 2. Datos duros

| Ítem | Valor |
|------|-------|
| Carpeta del lab | `labs/lab-03-numeros-del-puerto/` |
| Duración objetivo | ~2,0 horas (Módulo 2, 1ª mitad; presupuesto: 7 labs / 20 hrs) |
| Python | 3.13 pineado con `uv` |
| **Dependencias (NOVEDAD)** | `numpy==2.5.0` · `pandas==3.0.4` — pineadas EXACTAS en `pyproject.toml`, `uv.lock` versionado |
| Tag al certificar | `lab-03-v1.0.0` |

## 3. Estructura del lab

Anatomía estándar del curso (idéntica a Labs 01–02), con:

```
labs/lab-03-numeros-del-puerto/
├── README.md · pyproject.toml · .python-version
├── bin/ (00-preparar.sh/.ps1 · lib_comunes.py · verificar_entorno.py ·
│         verificar.py · recuperar_lab.py)
├── datos/
│   ├── recaudacion.py           ← dataset nuevo (§5.1, VERBATIM)
│   └── cuaderno.py              ← COPIA EXACTA del Lab 01 (SPEC-002 §5)
├── guia/ (01-contexto.md · 02-arrays.md · 03-vectorizacion.md ·
│          04-dataframes.md · 05-panorama.md)
├── plantillas/ (panorama.py con TODO 1..6 · RESPUESTAS.md)
├── soluciones/ (panorama.py · desafio-rubro-estrella.md)
└── docs/troubleshooting.md
```

## 4. Alcance pedagógico (temario Módulo 2, 1ª mitad)

**Cubre:** qué es NumPy y por qué existe (vectorización vs bucles) ·
`ndarray`: creación desde listas, `shape`, `dtype`, `ndim` · indexación y
slicing 2D · operaciones vectorizadas y **broadcasting** (escalar y
elemento a elemento) · agregaciones con `axis` (`sum`, `mean`, `max`,
`argmax`) · máscaras booleanas · introducción a pandas: `Series` y
`DataFrame` (creación desde listas/dicts), `head`, `info`, `dtypes`,
`shape` · selección `loc`/`iloc` · filtrado booleano · columnas derivadas ·
`value_counts` y `describe`.

**Fuera de alcance (Lab 04):** lectura/escritura de CSV, Excel, JSON,
bases de datos y transacciones; `groupby`/merge (Módulo 3). Los datos
siguen llegando como módulos Python — el archivo externo es el clímax del
Lab 04.

## 5. Datasets (VERBATIM, son contrato)

### 5.1 `datos/recaudacion.py`

Docstring narrativo (planilla del Concejo) + tres constantes:

```python
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

RUBROS = ["C", "G", "T"]  # Comercio, Gastronomía, Turismo

# Recaudación mensual en pesos (filas = meses, columnas = rubros C, G, T)
RECAUDACION = [
    [4_120_000, 3_380_000, 1_150_000],  # Enero
    [3_950_000, 3_610_000, 1_240_000],  # Febrero
    [4_310_000, 2_890_000,   760_000],  # Marzo
    [4_050_000, 2_540_000,   410_000],  # Abril
    [3_880_000, 2_360_000,   330_000],  # Mayo
    [3_720_000, 2_150_000,   280_000],  # Junio
    [3_690_000, 2_310_000,   350_000],  # Julio
    [3_810_000, 2_480_000,   390_000],  # Agosto
    [4_020_000, 2_720_000,   540_000],  # Septiembre
    [4_180_000, 2_950_000,   690_000],  # Octubre
    [4_260_000, 3_140_000,   880_000],  # Noviembre
    [4_490_000, 3_560_000, 1_090_000],  # Diciembre
]
```

(Los separadores `_` en los literales son intencionales: se comentan en la
Guía 2 como truco de legibilidad de Python.)

**Cifras de control:** las de §0. Detalle estacional a comentar en guías:
Turismo se dispara en verano y muere en invierno — los datos cuentan la
historia del puerto.

### 5.2 `datos/cuaderno.py`
Copia EXACTA del Lab 01 (SPEC-002 §5). Cifras: 24 patentes, 13 vigentes,
8 vencidas (deuda vencida total **$976.000**), deuda total $2.350.000.

## 6. Contratos de código

Rigen **C1–C8** (SPEC-002 §6 + SPEC-003 §6). Ajustes y agregados:

- **C1 (ajuste único):** los scripts de `bin/` siguen siendo de solo
  lectura, pero en este lab `verificar.py` y `recuperar_lab.py` PUEDEN
  importar numpy/pandas (corren bajo `uv run` dentro del entorno del lab).
  `verificar_entorno.py` debe ejecutarse ANTES de `uv sync` sin morir:
  la importación de numpy/pandas se chequea de forma tolerante (§8.2).
- **C9 (nuevo):** API moderna únicamente — pandas 3.x idiomático: nada de
  `inplace=True`, nada de encadenar indexaciones para asignar
  (`df[a][b] = ...`); asignación con `loc` o columnas nuevas directas.
  NumPy 2.x idiomático (sin APIs removidas en 2.0).
- **C10 (nuevo):** los floats se comparan con tolerancia
  (`np.allclose`/`math.isclose`), nunca con `==`, tanto en verificadores
  como en guías donde aplique.

## 7. El programa del lab — `panorama.py`

### 7.1 Solución (`soluciones/panorama.py`)

Imports: `numpy as np`, `pandas as pd`, datasets. Funciones obligatorias:

- `construir_matriz() -> np.ndarray` — `np.array(RECAUDACION)` (12×3, int).
- `recaudacion_por_mes(matriz) -> np.ndarray` — `matriz.sum(axis=1)` (12,).
- `recaudacion_por_rubro(matriz) -> np.ndarray` — `matriz.sum(axis=0)` (3,).
- `mes_record(matriz) -> str` — nombre del mes con mayor total mensual
  (`argmax` sobre por-mes → indexar `MESES`).
- `meses_bajo_umbral(matriz, umbral) -> list[str]` — máscara booleana sobre
  totales mensuales; retorna nombres (esperado con 6_500_000: Junio, Julio).
- `proyectar_reajuste(matriz, tasa) -> np.ndarray` — `matriz * (1 + tasa)`
  (broadcasting; float).
- `cuaderno_a_dataframe() -> pd.DataFrame` — desde `PATENTES` con columnas
  `["codigo", "nombre", "estado", "deuda"]`.
- `resumen_vencidas(df) -> tuple[int, int]` — filtrado booleano
  `df[df["estado"] == "VENCIDA"]`; retorna `(cantidad, deuda_total)`
  como ints nativos (esperado: `(8, 976000)`).
- `construir_informe(...) -> str` — f-strings con `:,`; secciones: título
  `PANORAMA ANUAL — Dirección de Rentas de Puerto Siracusa`, `=`×58;
  `Recaudación total anual  : $90,680,000 CLP`; `Mes récord               :
  Diciembre ($9,140,000)`; `Meses bajo umbral        : Junio, Julio`;
  `Recaudación por rubro:` con línea por rubro; `Morosidad del cuaderno:`
  con `Patentes vencidas: 8` y `Deuda vencida    : $976,000 CLP`.
- `main()` — imprime informe y escribe `salidas/informe_panorama.txt`
  (UTF-8, pathlib).

### 7.2 Plantilla — TODO 1..6 con pistas
TODO 1 → `recaudacion_por_mes` (pista: `axis=1` suma "a lo ancho", por
fila) · TODO 2 → `recaudacion_por_rubro` (pista: `axis=0`) · TODO 3 →
`mes_record` (pista: `np.argmax` da la POSICIÓN, no el valor) · TODO 4 →
`meses_bajo_umbral` (pista: una comparación sobre un array devuelve un
array de True/False; combinar con un bucle o `np.where`) · TODO 5 →
`resumen_vencidas` (pista: `df[df["estado"] == ...]` filtra filas; `int()`
al retornar) · TODO 6 → renglones del informe. La plantilla corre con
TODOs pendientes (retornos neutros) sin excepciones.

## 8. Verificadores

### 8.1 Preparadores y `lib_comunes.py`
Contratos de siempre. `uv sync` ahora descarga numpy/pandas — los
preparadores deben avisarlo (`[INFO] Descargando las bibliotecas del lab
(solo la primera vez, requiere Internet)...`).

### 8.2 `bin/verificar_entorno.py`
Checks del Lab 01 **+** verificación tolerante de bibliotecas: intentar
`import numpy` / `import pandas` y comparar `__version__` contra las
pineadas (2.5.0 / 3.0.4). Si el import falla → `[ERROR]` con pista de
correr el preparador (no traceback crudo). Versión distinta → `[ERROR]`
con pista `uv sync`.

### 8.3 `bin/verificar.py` — checks (en orden)
Referencia propia + **datasets sorpresa**: (a) matriz aleatoria 12×3 de
ints (rangos realistas) generada con `random.Random()` sin semilla —
verifica por-mes, por-rubro, mes récord, umbral sorteado y reajuste
(`np.allclose`); (b) mini-cuaderno sorpresa (6–10 patentes estilo Lab 01)
convertido a DataFrame por el VERIFICADOR para probar `resumen_vencidas`.

1. `panorama.py` en la raíz (pista → Guía 5).
2. Importa sin excepciones (manejo elegante; anti-cuelgue C8).
3. Existen las 8 funciones (§7.1) y son callables.
4. `construir_matriz()`: shape (12, 3) y dtype entero.
5. Oficial: por-mes y por-rubro == referencia (`np.array_equal`);
   `mes_record` == "Diciembre"; `meses_bajo_umbral(m, 6_500_000)` ==
   ["Junio", "Julio"]; `proyectar_reajuste(m, 0.04).sum()` ≈ 94_307_200
   (`np.allclose`).
6. Sorpresa (a): las cinco anteriores contra referencia.
7. `cuaderno_a_dataframe()`: DataFrame 24×4 con columnas exactas y
   `resumen_vencidas` oficial == (8, 976000) con tipos int nativos.
8. Sorpresa (b): `resumen_vencidas` == referencia.
9. `salidas/informe_panorama.txt` existe y contiene `90,680,000` y
   `Diciembre`.
10. `RESPUESTAS.md` sin marcadores pendientes.

Cierre en verde + teaser Lab 04 ("las cuatro fuentes": los datos por fin
llegan en archivos).

### 8.4 `bin/recuperar_lab.py`
Contrato estándar (solución → raíz, regenerar salidas, interrogatorio
intacto/pendiente).

## 9. Guías (redacción original de mocito; convenciones de siempre)

- **01-contexto.md** — la planilla del Concejo; preparar entorno (¡ahora
  descarga bibliotecas — salida esperada lo muestra!); el porqué de NumPy
  con DEMO obligatoria de vectorización: sumar 12 totales con bucle vs
  `matriz.sum(axis=1)` — y una analogía original (sugerencia: el bucle es
  ir timbre por timbre cobrando patente a patente; NumPy es el pregonero
  que cobra a toda la cuadra de un grito). REPL: importar numpy y pandas,
  ver `__version__` de ambos.
- **02-arrays.md** — `np.array(RECAUDACION)`; `shape/dtype/ndim` (analogía
  de shape: las dimensiones del archivador — cajones × carpetas);
  literales con `_`; indexación 2D `m[fila, col]` y slicing (`m[0]`,
  `m[:, 2]` — la columna del Turismo); 🔮 predicción: `m[5, 2]` (¿la
  recaudación turística de Junio?); agregaciones con `axis` (regla
  mnemotécnica obligatoria: `axis` es el eje QUE COLAPSA); `max`, `argmax`;
  💥 rómpelo: `m[12, 0]` → IndexError 2D leído con calma.
- **03-vectorizacion.md** — broadcasting escalar (`m * 1.04` — el reajuste
  del Concejo) y por qué NO hace falta bucle; máscaras booleanas:
  `tot_mes < 6_500_000` → array de True/False → seleccionar meses; 🔮
  predicción del resultado del umbral ANTES de ejecutar (alimenta
  interrogatorio); combinar máscaras (`&`, `|` — 💥 rómpelo: usar `and`
  entre arrays → ValueError "truth value is ambiguous", el error MÁS
  googleado de NumPy, leerlo y entender por qué existe); `np.where` breve.
- **04-dataframes.md** — el puente: "una matriz con nombres" — `pd.Series`
  (30 segundos) y `pd.DataFrame` desde `PATENTES` con `columns=`;
  reencuentro con el cuaderno del Lab 01 ("míralo ahora con esteroides");
  `head/info/dtypes/shape` (mencionar que pandas 3 muestra las columnas de
  texto como dtype `str` — es NUEVO de pandas 3, los tutoriales viejos
  muestran `object`); `loc` vs `iloc` (etiqueta vs posición — analogía:
  buscar por nombre de contribuyente vs por número de fila del archivador);
  filtrado booleano `df[df["estado"] == "VENCIDA"]`; columna derivada
  `df["con_deuda"] = df["deuda"] > 0`; `value_counts()` sobre estado;
  `describe()` sobre deuda; 💥 rómpelo: `df["Estado"]` → KeyError (¡las
  mayúsculas importan!).
- **05-panorama.md** — bifurcación 🛠️/🔎 (cp/Copy-Item); construir/ejecutar
  `panorama.py` con salida esperada (cifras de control); comentar la
  historia estacional del Turismo; modificación obligatoria del Explorador
  (interrogatorio P5); interrogatorio; verificación final; **desafío
  extra**: "el rubro estrella" — ¿qué rubro creció más entre Junio y
  Diciembre en términos porcentuales? (una línea de NumPy:
  `(m[11] - m[5]) / m[5] * 100`; solución en
  `soluciones/desafio-rubro-estrella.md` con la respuesta: Turismo,
  +289.3 % — verificar cifra al construir). Checkpoint final + teaser
  Lab 04.

## 10. Troubleshooting (agregados específicos del lab)

Los de siempre + nuevos: `uv sync` lento/fallando la primera vez (red,
proxy corporativo, antivirus reteniendo wheels — paciencia y reintento) ·
`ModuleNotFoundError: No module named 'numpy'` (corrió con el Python del
sistema en vez de `uv run`) · "truth value of an array is ambiguous" (usar
`&`/`|` con paréntesis, no `and`/`or`) · el clásico `Killed`/MemoryError
NO aplica aquí (datos chicos) pero anotar que arrays gigantes se verán en
el curso avanzado 😄 · diferencias de dtype `str` vs `object` si el alumno
compara con tutoriales viejos de pandas.

## 11. Interrogatorio — 5 preguntas (marcador estándar; H-02 vigente)

1. **El axis:** según TU ejecución, ¿`matriz.sum(axis=0)` devolvió 3 o 12
   números? Explica la regla "el eje que colapsa" con este ejemplo.
2. **La máscara:** ¿qué meses quedaron bajo el umbral de $6.500.000 en TU
   informe? Copia el array booleano que imprimiste en la Guía 3 y marca a
   mano cuáles True corresponden a esos meses.
3. **El error ambiguo:** pega la última línea del ValueError que provocaste
   al usar `and` entre arrays y explica con tus palabras por qué NumPy no
   puede decidir solo.
4. **loc vs iloc:** en TU sesión, ¿qué devolvió `df.iloc[6]` y qué patente
   es? ¿Cómo obtendrías LA MISMA fila si el DataFrame estuviera ordenado
   por deuda descendente — te serviría iloc[6] todavía? ¿Por qué?
5. **Modifica y explica (Explorador obligatorio):** cambia el umbral de
   `meses_bajo_umbral` en `main` a $7.000.000, re-ejecuta y explica qué
   meses aparecieron de más y qué le dirías al Concejo con ese nuevo corte.
   Revierte al terminar.

## 12. Guion de pruebas 🎭 (clon limpio, en orden, evidencia por escenario)

- **E01 — Flujo feliz Explorador:** preparar (ver descarga de deps la
  primera vez) → solución → ejecutar → informe con `$90,680,000`,
  `Diciembre`, `Junio, Julio`, `(8, ...976,000...)` → verificador N-1/N
  (solo interrogatorio) → responder → N/N exit 0.
- **E02 — Artesano a medio camino:** plantilla intacta → errores con
  pistas útiles → completar SOLO TODO 1 → ese check pasa, el resto no.
- **E03 — Tramposo:** hardcodear retornos oficiales (incluidos los arrays)
  → verificador ×3 → los datasets sorpresa lo cazan las 3 veces.
- **E04 — Perdido:** `cp soluciones/panorama.py guia/ && cd guia && uv run
  python panorama.py` → ModuleNotFoundError de `datos` documentado con cura;
  limpiar.
- **E05 — Rompe cosas:** borrar informe → cura → verde · SyntaxError →
  reporte elegante · breakpoint() olvidado → anti-cuelgue · **NUEVO:**
  simular biblioteca rota — `uv run python -c "import numpy"` tras borrar
  `.venv/` → correr `verificar_entorno.py` → debe reportar `[ERROR]` con
  pista del preparador (no traceback); re-preparar → verde.
- **E06 — Rezagado:** recuperador → N-1/N (interrogatorio pendiente).
- **E07 — Idempotencia:** preparador ×3 (la 2ª y 3ª SIN re-descargar).
- **E08 — Higiene:** `git status` limpio (ampliar .gitignore con
  `labs/*/panorama.py` — documentar patrón elegido).
- **E09 — Regresión:** verificadores de Lab 01 Y Lab 02 sobre flujo rápido
  (recuperador + respuestas dummy) → 12/12 y N/N respectivos; archivos de
  ambos labs intactos (`git diff` vacío fuera del lab 03 y portada).

## 13. Cambios en archivos existentes (únicas excepciones al aislamiento)
- Portada del repo: tabla de labs → Lab 03 ✅ Disponible.
- `.gitignore`: patrón para el artefacto de alumno de este lab (§12-E08).

## 14. Flujo Git, certificación y DoD

Commits convencionales (`feat: Lab 03 — Los números del puerto` · `docs:
spec SPEC-004` · `test: certificación del Lab 03 como alumno` + fixes) ·
reporte `docs/certificacion-lab-03.md` (tabla E01–E09, Hallazgos,
veredicto) · con CERTIFICADO limpio: tag `lab-03-v1.0.0` + push · si hay
observación abierta: detener y consultar (protocolo H-01).

**DoD:** lab conforme §3–§11 con `uv.lock` versionado y deps pineadas
exactas · portada y .gitignore actualizados · E01–E09 CERTIFICADO ·
commits + tag pusheados · hallazgos reportados.

---

*Firmado: El Arquitecto de Puerto Siracusa.*
*"Doce meses, tres rubros, una matriz — y el Concejo tendrá sus totales
por donde los mire."* 🏛️📐
