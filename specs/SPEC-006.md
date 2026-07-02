# SPEC-006 — Lab 05: "La gran limpieza"

> **Proyecto:** Curso Programación en Python — SII 2026 · "Puerto Siracusa"
> **Emitido por:** El Arquitecto (Claude) · **Aprobado por:** Rodrigo Silva Bravo (PO)
> **Ejecutor:** mocito (Claude Code) — dueño del repositorio y único constructor
> **Fecha:** 2026-07-02 · **Versión:** 1.0
> **Dependencias:** repo con tags `lab-01/02/03/04-v1.0.0` (Módulos 1 y 2 completos)

---

## ⚠️ 0. Verificación del Arquitecto (leer PRIMERO)

**Premisas verificadas por el Arquitecto:**
- ✅ **Sin dependencias nuevas:** mismas del Lab 04 (`numpy==2.5.0`,
  `pandas==3.0.3`, `openpyxl==3.1.5` — esta última solo porque el informe
  final exporta un resumen a Excel; ya validadas, sin yank).
- ✅ **Cifras de control computadas CON PANDAS REAL** (no con el módulo
  `statistics`, cuyos cuartiles difieren — trampa conocida): censo bruto
  **30 filas** → tras duplicados exactos **28** (−2) → códigos válidos
  **26** (−2 malformados) → **3** deudas faltantes imputadas → outliers
  IQR: **{PS-1022-T: 520.000, PS-1046-C: 9.999.999}** con Q1=29.000,
  Q3=200.000, IQR=171.000, límite superior 456.500 → outliers |z|>3 (std
  muestral, ddof=1): **solo PS-1046-C** → censo limpio final
  **25 filas, deuda total $3.107.500**. Variantes crudas de `estado`:
  **10 → 3** tras homogeneizar.
- ✅ El dataset es **CSV = texto plano** → se especifica VERBATIM y se
  versiona directo, sin generador (los binarios del Lab 04 fueron la
  excepción, no la regla — lección H-04 no aplica aquí).
- ✅ Alcance cruzado contra temario: **Módulo 3, primera parte** —
  limpieza y homogeneización (duplicados, faltantes, filtrado con
  `query()` y regex, outliers IQR y z-score). Transformación y combinación
  quedan para el Lab 06; Matplotlib para Lab 06/capstone.

**Supuestos a validar por el PO o mocito ANTES de ejecutar:**
1. Repo en `main` limpio y sincronizado; Labs 01–04 certificados intactos.
2. Sin cambios de sistema desde SPEC-005 (deps ya en caché de uv:
   `uv sync` no debería descargar nada nuevo).

---

## 1. Contexto y narrativa del lab

El practicante de verano del municipio tuvo una idea "brillante": fusionó
a mano TODAS las planillas de patentes en un solo archivo — el **Censo de
Patentes de Puerto Siracusa** — y se fue de vacaciones. Don Arquímedes lo
abre y palidece: estados escritos de diez maneras distintas, espacios
fantasma, filas repetidas, deudas "S/I", códigos que no respetan el
formato, y una deuda de **$9.999.999** que huele a dedo dormido sobre el
teclado.

El dolor pedagógico: hasta ahora los datos venían limpios porque alguien
(nosotros) los limpió antes. **Ese alguien ahora eres tú.** La lección
transversal: limpiar NO es borrar — es **decidir con criterio y dejar
rastro** de cada decisión. El clímax del lab: IQR acusa a dos
contribuyentes de outliers, z-score solo a uno... y el analista debe
descubrir que uno es un negocio real (Buceo Fondo Claro, viejo conocido de
labs anteriores) y el otro un error de digitación. **Los métodos proponen;
el analista dispone.**

Misión: construir `limpiar.py` — el pipeline que homogeneiza, deduplica,
filtra, imputa y detecta outliers, produciendo el censo limpio + un
informe donde CADA fila descartada está contabilizada y justificada.

## 2. Datos duros

| Ítem | Valor |
|------|-------|
| Carpeta del lab | `labs/lab-05-gran-limpieza/` |
| Duración objetivo | ~2,0 horas (Módulo 3, 1ª parte; presupuesto: 7 labs / 20 hrs) |
| Python / deps | 3.13 · `numpy==2.5.0` · `pandas==3.0.3` · `openpyxl==3.1.5` |
| Tag al certificar | `lab-05-v1.0.0` |

## 3. Estructura del lab

```
labs/lab-05-gran-limpieza/
├── README.md · pyproject.toml · .python-version
├── bin/ (00-preparar.sh/.ps1 · lib_comunes.py · verificar_entorno.py ·
│         verificar.py · recuperar_lab.py)
├── datos/censo_patentes.csv     ← dataset VERBATIM (§5), versionado directo
├── guia/ (01-contexto.md · 02-homogeneizacion.md · 03-duplicados-y-filtrado.md ·
│          04-outliers.md · 05-pipeline.md)
├── plantillas/ (limpiar.py con TODO 1..6 · RESPUESTAS.md)
├── soluciones/ (limpiar.py · desafio-certificado-calidad.md)
└── docs/troubleshooting.md
```

## 4. Alcance pedagógico (temario Módulo 3, 1ª parte)

**Cubre:** diagnóstico de calidad (`info`, `value_counts`, `isna().sum()`,
`describe`) · homogeneización de texto con el accessor `.str` (`strip`,
`upper`, `title`) · marcadores de faltante → `NaN` (`na_values` en
`read_csv`) y tratamiento (`fillna` con regla de negocio documentada vs
`dropna` — se enseñan ambos, la solución imputa 0 por regla de Don
Arquímedes) · duplicados: `duplicated()` y `drop_duplicates()` (parámetros
`subset` y `keep`) · filtrado: booleano clásico, **`query()`** y **regex**
(`str.fullmatch`, `str.contains`) · **outliers**: método IQR (cuartiles
con `quantile`) y **z-score** (media y std muestral), comparación crítica
entre ambos y decisión de negocio.

**Fuera de alcance (Lab 06):** mapeos/`map`, discretización/`cut`,
dummies, `merge`/`concat`, `groupby`/pivot, Matplotlib.

## 5. Dataset — `datos/censo_patentes.csv` (VERBATIM, es contrato)

Archivo de texto UTF-8, separador coma, CON encabezado. La mugre es
INTENCIONAL Y EXACTA — cada espacio, mayúscula y celda vacía es contrato
(las cifras de control dependen de ellos). Ver `datos/censo_patentes.csv`
para el contenido exacto (30 filas de datos).

**Inventario de la mugre (para las guías y el verificador):**
- 30 filas de datos (+ encabezado).
- `estado` con **10 variantes crudas** → **3** tras homogeneizar
  (VIGENTE, VENCIDA, SUSPENDIDA).
- Nombre con espacios fantasma: `  Café La Palanca  `.
- **2 duplicados exactos** (PS-1005-C y PS-1020-G repetidas al final).
- **2 códigos malformados**: `PS-999` y `XX-1050-G`.
- **3 faltantes de deuda** con tres marcadores: celda vacía, `S/I`, `sin dato`.
- **1 outlier de digitación**: PS-1046-C con 9.999.999.
- **1 outlier legítimo**: PS-1022-T (Buceo Fondo Claro, 520.000 — deuda
  real conocida desde el Lab 01; la continuidad narrativa ES la evidencia).

**Cifras de control (verificadas §0):** 30 → 28 (dedup) → 26 (códigos) →
3 imputaciones → IQR flags {520000, 9999999} → z>3 flags {9999999} →
**apartado solo el typo** → censo limpio **25 filas, $3.107.500**.

## 6. Contratos de código
Rigen **C1–C12**. Agregados:
- **C13:** ninguna función de limpieza muta el DataFrame recibido: opera
  sobre copia y retorna (`df = df.copy()` al entrar).
- **C14:** toda fila descartada o alterada queda CONTABILIZADA en el
  reporte del pipeline (dict de métricas). Limpiar sin rastro está
  prohibido — es el anti-patrón que el lab combate.
- **C15:** cuartiles con `Series.quantile` de pandas; desviación estándar
  MUESTRAL (`Series.std()`, ddof=1). Prohibido mezclar con el módulo
  `statistics` (sus métodos difieren).

## 7. El programa del lab — `limpiar.py`

### 7.1 Solución (`soluciones/limpiar.py`)
Funciones obligatorias (reciben DataFrame o ruta; C12/C13):
`cargar_censo` (read_csv con na_values), `homogeneizar` (.str strip/upper),
`quitar_duplicados` → (df, n), `filtrar_codigos` → (válidos, descartados)
vía `str.fullmatch(r"PS-\d{4}-[CGT]")`, `imputar_deuda` → (df, n) con
fillna(0) a int (regla de negocio de Don Arquímedes, comentada),
`outliers_iqr` (Q1/Q3/IQR con quantile), `outliers_z(df, umbral=3.0)` (std
muestral), `vencidas_grandes(df, umbral)` con query() y `@umbral`,
`limpiar_censo(ruta)` → (censo_limpio 25, reporte dict con TODAS las
métricas; regla: se aparta solo lo señalado por AMBOS métodos = consenso;
lo solo-IQR se conserva con nota), `construir_informe` (título, `=`×58, el
embudo etapa a etapa, outliers con veredicto, cierre 25 filas / $3,107,500).
`main()` ejecuta, imprime, escribe `salidas/informe_limpieza.txt`, exporta
`censo_limpio.csv` y `.xlsx`.

### 7.2 Plantilla — TODO 1..6
TODO 1 homogeneizar (.str) · TODO 2 quitar_duplicados (len antes/después) ·
TODO 3 filtrar_codigos (regex; ~ invierte) · TODO 4 imputar_deuda
(isna().sum(); fillna) · TODO 5 outliers_iqr (quantile) · TODO 6 la regla
de consenso en limpiar_censo (isin / cod_iqr & cod_z). Corre con TODOs
pendientes.

## 8. Verificadores

### 8.1 `verificar_entorno.py`
Estándar + imports pineados + existencia de `datos/censo_patentes.csv`
con **exactamente 30 filas de datos** (si difiere: pista de restaurar con
`git checkout -- datos/censo_patentes.csv`).

### 8.2 `bin/verificar.py` — checks
Referencia propia + **censo sorpresa** en tempdir (CSV pequeño con mugre
sorteada de los mismos tipos). Checks: existe · importa (anti-cuelgue C8) ·
10 funciones · cargar_censo 30×4 con deuda float y 3 NaN · homogeneizar →
{VIGENTE, VENCIDA, SUSPENDIDA} y nombre sin bordes · quitar_duplicados 28/2 ·
filtrar_codigos 26/2 con descartados {PS-999, XX-1050-G} · imputar_deuda 3,
0 NaN, dtype int · outliers_iqr {PS-1022-T, PS-1046-C} y outliers_z
{PS-1046-C} · vencidas_grandes correcto · limpiar_censo oficial 25 filas,
$3.107.500 y reporte con TODAS las métricas (C14) · censo sorpresa ==
referencia · salidas con informe (3,107,500 y embudo 30→25) + censo_limpio
csv/xlsx de 25 filas · RESPUESTAS sin marcadores. Cierre + teaser Lab 06.

### 8.3 `recuperar_lab.py`
Estándar; si el censo fue alterado, restaurarlo vía git (`git checkout`);
si el lab no está en un repo git, se avisa y continúa (decisión documentada:
no hay copia de respaldo interna para no duplicar el dataset).

## 9. Guías (redacción de mocito; convenciones y cápsulas de siempre)

- **01-contexto.md** — la hazaña del practicante; entorno; el RITUAL DE
  DIAGNÓSTICO (head, info, value_counts sobre estado —🔮 predice cuántas
  variantes: 10—, isna, describe con el max 9.999.999); regla "primero
  diagnosticar, después operar" (analogía elevador del mecánico).
- **02-homogeneizacion.md** — el accessor `.str`; value_counts antes/después
  (10 → 3); `na_values` con los TRES marcadores; `fillna` vs `dropna` y la
  regla de negocio; 💥 `"VIGENTE" == "vigente "` y por qué el filtro fallaba.
- **03-duplicados-y-filtrado.md** — `duplicated` vs `drop_duplicates`,
  `subset`/`keep`; `query()` con `@`; regex `fullmatch` vs `contains`
  (💥 anclaje); 🤖 explicar la regex pieza por pieza.
- **04-outliers.md** — `describe`; IQR paso a paso (analogía vara del
  pescador); z-score muestral (C15, trampa `statistics`); el desacuerdo
  (IQR:2, z:1) y la investigación (Buceo Fondo Claro real vs 9.999.999 typo);
  🔮 predice si z marca a Buceo; moraleja: los métodos proponen, el analista
  dispone, todo queda escrito.
- **05-pipeline.md** — bifurcación; armar `limpiar.py`; el embudo 30→28→26→25
  con salida esperada; C14; modificación del Explorador (P5); interrogatorio;
  verificación; desafío "certificado de calidad". Checkpoint + teaser Lab 06.

## 10. Troubleshooting (agregados del lab)
Heredados + nuevos: "mi filtro no encuentra nada" (homogeneizar primero) ·
`deuda` como texto (na_values) · el 9.999.999 tras imputar (sigue, mirar
max) · regex que no calza (fullmatch ancla, contains no) · restaurar el
censo con `git checkout` · CoW de pandas 3 (las vistas ya no mutan; C13
natural).

## 11. Interrogatorio — 5 preguntas (marcador estándar; H-02 vigente)

1. **El diagnóstico:** variantes crudas de `estado` (cuántas y cuáles) y
   cuántas tras homogeneizar.
2. **El embudo:** la secuencia 30→…→25 y qué se perdió en cada salto.
3. **El desacuerdo de los métodos:** qué marcó IQR y qué marcó z-score, por
   qué difieren, y el veredicto de cada outlier.
4. **La regla de negocio:** cuántas deudas imputó y con qué valor; riesgo y
   alternativa (dropna).
5. **Modifica y explica (Explorador):** bajar el umbral del z-score de 3.0 a
   2.0; qué cambió en outliers y en el censo final; revertir.

## 12. Guion de pruebas 🎭 (clon limpio, en orden, evidencia por escenario)

- **E01 — Flujo feliz Explorador:** preparar (sin descargas — deps en caché) →
  solución → ejecutar → informe con embudo 30→25 y `$3,107,500` → salidas
  (txt + csv + xlsx de 25 filas) → verificador N-1/N → responder → N/N exit 0.
- **E02 — Artesano a medio camino:** plantilla → pistas → SOLO TODO 1 →
  homogeneizar pasa, resto no.
- **E03 — Tramposo:** hardcodear reporte y retornos oficiales → censo sorpresa
  lo caza ×3.
- **E04 — Perdido:** solución desde guia/ → error de ruta al censo documentado
  con cura; limpiar.
- **E05 — Rompe cosas:** alterar el censo (borrar una fila) → entorno lo
  detecta (≠30) con pista de git checkout → restaurar → verde · SyntaxError y
  breakpoint() estándar · **NUEVO:** agregar una 4ª variante de faltante
  ("N/A") al censo → el pipeline no la conoce → documentar el síntoma (deuda
  como texto / NaN no detectado) y la cura (na_values) → restaurar censo.
- **E06 — Rezagado:** recuperador (restaura censo si fue tocado) → N-1/N.
- **E07 — Idempotencia:** preparador ×3; pipeline ×2 → mismas salidas.
- **E08 — Higiene:** `git status` limpio (`labs/*/limpiar.py` ignorado; el
  censo SÍ versionado).
- **E09 — Regresión:** verificadores de Labs 01–04 en flujo rápido → todos en
  verde; `git diff` limpio fuera del Lab 05 y portada.

## 13. Cambios en archivos existentes (únicas excepciones)
Portada: Lab 05 ✅ Disponible · `.gitignore`: `labs/*/limpiar.py`.

## 14. Flujo Git, certificación y DoD
Commits convencionales (`feat: Lab 05 — La gran limpieza` · `docs: spec
SPEC-006` · `test: certificación del Lab 05 como alumno` + fixes) ·
reporte `docs/certificacion-lab-05.md` · CERTIFICADO limpio → tag
`lab-05-v1.0.0` + push · observación abierta → detener y consultar
(protocolo H-01/H-03/H-04).

**DoD:** lab conforme §3–§11 · censo verbatim versionado · portada y
.gitignore al día · E01–E09 CERTIFICADO · commits + tag pusheados ·
hallazgos reportados.

---

*Firmado: El Arquitecto de Puerto Siracusa.*
*"Los métodos proponen; el analista dispone — y todo veredicto queda
escrito."* 🏛️🧹📐
