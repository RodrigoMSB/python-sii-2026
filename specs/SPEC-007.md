# SPEC-007 — Lab 06: "Transformar y combinar"

> **Proyecto:** Curso Programación en Python — SII 2026 · "Puerto Siracusa"
> **Emitido por:** El Arquitecto (Claude) · **Aprobado por:** Rodrigo Silva Bravo (PO)
> **Ejecutor:** mocito (Claude Code) — dueño del repositorio y único constructor
> **Fecha:** 2026-07-02 · **Versión:** 1.0
> **Dependencias:** repo con tags `lab-01..05-v1.0.0` (Módulos 1–2 completos; Módulo 3 iniciado)

---

## ⚠️ 0. Verificación del Arquitecto (leer PRIMERO)

**Premisas verificadas por el Arquitecto:**
- ✅ **Dependencia nueva verificada contra PyPI el 2026-07-02, incluyendo
  estado de retiro (doctrina H-03):** `matplotlib==3.11.0` (última estable,
  wheels para todas las plataformas, **sin yank**). Se mantienen
  `numpy==2.5.0`, `pandas==3.0.3`, `openpyxl==3.1.5`.
- ✅ **Nota operativa de matplotlib:** en scripts se usa el backend **Agg**
  (headless) y `savefig` — jamás `plt.show()` (abre ventanas, cuelga
  verificadores y falla en terminales sin GUI). Contrato C16.
- ✅ **Cifras de control computadas CON PANDAS REAL** (§5):
  rubros del censo {Gastronomía: 11, Comercio: 8, Turismo: 6} · tramos de
  deuda con `cut` {Sin deuda: 4, Baja: 11, Media: 7, Alta: 3} · dummies de
  estado {SUSPENDIDA: 5, VENCIDA: 10, VIGENTE: 10} · concat junio+julio =
  **20 pagos, $1.213.000** · merge left → 25 filas, **9 sin pago alguno**,
  **pagos huérfanos {PS-1032-C, PS-1040-G} = $130.500** · pagado total (en
  censo) **$1.082.500** · saldo total **$2.025.000** · deuda por rubro
  {Comercio: 881.000, Gastronomía: 697.500, Turismo: 1.529.000} · saldo por
  rubro {Comercio: 601.000, Gastronomía: 99.000, Turismo: 1.325.000} ·
  pct de Buceo Fondo Claro dentro de Turismo: **34,0 %** · crosstab y
  pivot con valores exactos (§5.4).
- ✅ Datasets = **texto plano (CSV)** → verbatim, versionados directo, sin
  generador (H-04 no aplica).
- ✅ Alcance cruzado contra temario: **Módulo 3, segunda parte** —
  transformación (mapeos discretos, discretización numérica, dummies),
  combinación (merge, concat), agregación/sumarización (groupby,
  transform, crosstab), pivoteo — **y la visualización básica con
  Matplotlib** comprometida como valor agregado en el temario ganador.

**Supuestos a validar por el PO o mocito ANTES de ejecutar:**
1. Repo en `main` limpio; Labs 01–05 certificados intactos.
2. Internet para el `uv sync` (matplotlib es descarga nueva, ~wheels
   grandes: paciencia en la primera sincronización).
3. Sin cambios de sistema desde SPEC-006.

---

## 1. Contexto y narrativa del lab

El censo quedó limpio (Lab 05) y el Concejo Municipal huele resultados:
ahora quiere **EL TABLERO** — un solo cuadro que cruce lo que cada
contribuyente **debe** (censo) con lo que efectivamente **pagó**
(Tesorería, junio y julio), clasificado por rubro y tramo de deuda, con
totales por donde se mire... y "un dibujito para la presentación, que los
concejales no leen tablas".

El dolor pedagógico, en cadena: la letra del rubro no le dice nada al
Concejo → **map**; "¿cuántos deben poco y cuántos una fortuna?" → **cut**;
junio y julio en archivos separados → **concat**; deuda y pagos en tablas
distintas → **merge** (y los pagos huérfanos: dos pagaron y no están en el
censo → `left`/`inner`/`outer`); totales por rubro → **groupby** (+
`transform` para el % dentro del grupo); "todo cruzado" → **crosstab** y
**pivot_table**; y el dibujito → **matplotlib**.

Misión: construir `tablero.py` — transforma, combina, agrega, pivotea y
grafica, entregando el tablero del Concejo con cada peso cuadrado.

## 2. Datos duros

| Ítem | Valor |
|------|-------|
| Carpeta del lab | `labs/lab-06-transformar-combinar/` |
| Duración objetivo | ~2,0 horas (Módulo 3, 2ª parte; presupuesto: 7 labs / 20 hrs) |
| Python / deps | 3.13 · `numpy==2.5.0` · `pandas==3.0.3` · `openpyxl==3.1.5` · **`matplotlib==3.11.0`** |
| Tag al certificar | `lab-06-v1.0.0` |

## 3. Estructura del lab

```
labs/lab-06-transformar-combinar/
├── README.md · pyproject.toml · .python-version
├── bin/ (00-preparar.sh/.ps1 · lib_comunes.py · verificar_entorno.py ·
│         verificar.py · recuperar_lab.py)
├── datos/ (censo_limpio.csv · pagos_junio.csv · pagos_julio.csv)  ← VERBATIM
├── guia/ (01-contexto.md · 02-mapear-y-clasificar.md · 03-combinar.md ·
│          04-agregar-y-pivotear.md · 05-tablero.md)
├── plantillas/ (tablero.py con TODO 1..6 · RESPUESTAS.md)
├── soluciones/ (tablero.py · desafio-grafico-concejo.md)
└── docs/troubleshooting.md
```

## 4. Alcance pedagógico (temario Módulo 3, 2ª parte)

**Cubre:** mapeos discretos `Series.map` (dict) · derivación desde strings
(`str[-1]`) · discretización `pd.cut` (bins, labels, bordes) · dummies
`pd.get_dummies` (dtype bool) · **concat** (`ignore_index`) · **merge**
(`on`, `how` explícito, `left/inner/outer`, `validate=`, huérfanos con
`isin`/`indicator=True`) · **groupby** (agg), **`transform`** (% dentro del
grupo; agg vs transform) · **`crosstab`** · **`pivot_table`** (values/index/
columns/aggfunc/fill_value) · **matplotlib básico** (figura/ejes, barras,
título/etiquetas en español, `tight_layout`, `savefig` PNG, `close`; C16).

**Fuera de alcance (capstone):** storytelling con múltiples gráficos,
series de tiempo, formatos de informe final.

## 5. Datasets (VERBATIM, son contrato)

### 5.1 `datos/censo_limpio.csv` — el producto certificado del Lab 05
CSV UTF-8, encabezado `codigo,nombre,estado,deuda`, **25 filas exactas**
(deudas imputadas, sin el typo apartado). Ver el archivo para el contenido
exacto. Control: 25 filas, deuda total $3.107.500 (amarre con Lab 05).

### 5.2 `datos/pagos_junio.csv` — los 12 pagos del Lab 04
Encabezado `codigo,fecha,monto`; las 12 filas del `PAGOS_CSV` del Lab 04
(total $677.500). Incluye a PS-1040-G y PS-1032-C, que NO están en el censo.

### 5.3 `datos/pagos_julio.csv` — 8 pagos nuevos
8 filas (total $535.500). Concat total: **20 pagos, $1.213.000**.

### 5.4 Cifras de control derivadas (todas verificadas §0)
- `map` rubro: G→Gastronomía (11), C→Comercio (8), T→Turismo (6).
- `cut` deuda, bins `[-1, 0, 100000, 300000, 10**9]`, labels
  `["Sin deuda","Baja","Media","Alta"]`: **4 / 11 / 7 / 3**.
- `get_dummies(estado)`: SUSPENDIDA=5, VENCIDA=10, VIGENTE=10 (dtype bool).
- Merge left censo×pagado: 25 filas; `pagado` NaN→0; **9 sin pago**; pagado
  en censo $1.082.500; `saldo = deuda − pagado` total **$2.025.000**.
  Huérfanos (anti-join): {PS-1032-C, PS-1040-G} = $130.500.
- Groupby deuda: Comercio 881.000 · Gastronomía 697.500 · Turismo 1.529.000.
  Groupby saldo: 601.000 · 99.000 · 1.325.000. Transform: pct de PS-1022-T
  dentro de Turismo = 34,0 %.
- Crosstab estado×rubro: SUSPENDIDA {C:2,G:0,T:3} · VENCIDA {C:4,G:4,T:2} ·
  VIGENTE {C:2,G:7,T:1}.
- Pivot deuda rubro×estado (sum, fill_value=0): Comercio {S:610.000,
  V:221.000, Vig:50.000} · Gastronomía {S:0, V:467.000, Vig:230.500} ·
  Turismo {S:1.120.000, V:409.000, Vig:0}.

## 6. Contratos de código
Rigen **C1–C15**. Agregados:
- **C16 (matplotlib headless):** `matplotlib.use("Agg")` ANTES de importar
  `pyplot` en todo script; salida solo vía `savefig`; `plt.close(fig)`
  siempre; PROHIBIDO `plt.show()` en `soluciones/`, `plantillas/` y `bin/`.
- **C17 (merges con cinturón):** todo `merge` declara `how=` explícito y,
  cuando la cardinalidad es conocida, `validate=` (aquí `"1:1"` entre censo y
  pagos agregados).

## 7. El programa del lab — `tablero.py`

### 7.1 Solución (`soluciones/tablero.py`)
Funciones obligatorias (C12/C13): `cargar_censo`/`cargar_pagos`;
`agregar_rubro` (`str[-1].map(dict)`); `clasificar_deuda` (`pd.cut` con
bins/labels de §5.4); `dummies_estado` (`get_dummies`, bool);
`consolidar_pagos` (`concat`, `ignore_index=True`); `construir_tablero`
(groupby pagos por código, `merge how="left" validate="1:1"`, pagado NaN→0
int, saldo = deuda − pagado, huérfanos por anti-join → retorna
(tablero 25, huérfanos)); `resumen_por_rubro` (groupby suma deuda/pagado/
saldo); `pct_dentro_del_rubro` (columna via `transform("sum")`);
`tabla_cruzada` (`crosstab` estado×rubro); `pivote_deuda` (`pivot_table`
deuda rubro×estado, fill_value=0); `graficar_saldo(tablero, ruta_png)`
(barras saldo por rubro, Agg, título/etiquetas español, tight_layout,
savefig dpi=150, close; C16); `construir_informe` (título, `=`×58, totales
deuda/pagado/saldo, tramos, resumen por rubro, tabla cruzada, sección de
huérfanos con total $130.500). `main()` escribe `salidas/informe_tablero.txt`,
`tablero.csv` (index=False), `tablero.xlsx` y `saldo_por_rubro.png`.

### 7.2 Plantilla — TODO 1..6
TODO 1 agregar_rubro (str[-1] + map) · TODO 2 clasificar_deuda (cut) ·
TODO 3 consolidar_pagos (ignore_index) · TODO 4 el merge de
construir_tablero (how="left"; ¿y con inner?) · TODO 5 pct_dentro_del_rubro
(transform, mismo largo) · TODO 6 graficar_saldo (5 líneas de matplotlib).
Corre con TODOs pendientes.

## 8. Verificadores

### 8.1 `verificar_entorno.py`
Estándar + imports pineados incluyendo matplotlib 3.11.0 + los 3 CSV con
conteos exactos (25/12/8; pista `git checkout --` si no).

### 8.2 `bin/verificar.py` — checks
Referencia propia + **datasets sorpresa** en tempdir (mini-censo 8–12 filas +
dos meses de pagos 3–5 filas, con ≥1 huérfano inyectado). Checks: existe ·
importa (anti-cuelgue C8; Agg no abre ventana) · 12 funciones · rubros
{11,8,6} · tramos {4,11,7,3} con labels exactas · dummies {5,10,10} bool ·
concat 20/1.213.000 · tablero 25 filas, pagado 1.082.500, saldo 2.025.000,
9 sin pago, huérfanos {PS-1032-C,PS-1040-G}=130.500 · resumen por rubro y
pct Buceo 34.0 (tolerancia) · crosstab == §5.4 · pivote == §5.4 · sorpresa:
pipeline == referencia · salidas con informe (2,025,000 + huérfanos),
tablero.csv/xlsx de 25 filas y `saldo_por_rubro.png` válido (>5KB, firma
`\x89PNG`) · RESPUESTAS. Cierre + teaser capstone (El Arenario).

### 8.3 `recuperar_lab.py`
Estándar (restaurar CSVs vía git, solución → raíz, regenerar salidas,
interrogatorio intacto).

## 9. Guías (redacción de mocito; convenciones y cápsulas de siempre)

- **01-contexto.md** — el encargo del tablero; entorno (descarga de
  matplotlib, la más pesada); tour por los 3 CSV y reencuentro con el censo
  limpio; mapa del pipeline transformar→combinar→agregar→graficar.
- **02-mapear-y-clasificar.md** — `map` con dict (analogía timbre traductor;
  🔮 rubro "X" → NaN); `cut` (tramos; borde derecho incluyente — 💥 en qué
  tramo cae 100.000); `get_dummies` (bool moderno).
- **03-combinar.md** — `concat` (ignore_index); `merge` (analogía dos
  oficinas; las tres uniones left:25 / inner:16 / outer:27; `indicator=True`;
  `validate="1:1"` cinturón — 💥 MergeError sin agrupar; huérfanos PS-1032-C
  y PS-1040-G y de qué lab vienen).
- **04-agregar-y-pivotear.md** — `groupby` (bandejas del mesón); agg vs
  `transform` (mismo largo; 🔮 pct de Buceo = 34%); `crosstab` (conteos);
  `pivot_table` (fill_value=0; vs crosstab).
- **05-tablero.md** — bifurcación; matplotlib mínimo (Agg, savefig, close; C16
  explicado, jamás show()); armar `tablero.py`; salida esperada; abrir PNG y
  xlsx; modificación P5 (merge left→inner); interrogatorio; verificación;
  desafío "gráfico apilado". Checkpoint + teaser capstone.

## 10. Troubleshooting (agregados del lab)
Heredados + nuevos: `uv sync` lento por matplotlib · script "pegado" al
graficar (show() sin GUI — C16) · PNG de 0 bytes (savefig tras close, o
figura vacía) · warnings de glyphs (cosméticos) · `MergeError` (validate;
agrupar antes) · tramo NaN tras cut (fuera de bins) · categorías de cut
(sort_index).

## 11. Interrogatorio — 5 preguntas (marcador estándar; H-02 vigente)

1. **El borde del tramo:** ¿en qué tramo cayó una deuda de exactamente
   $100.000? Regla de `cut` y cómo lo verificó.
2. **Las tres uniones:** filas con `left`/`inner`/`outer` y su explicación.
3. **Los huérfanos:** qué códigos, cuánto suman, de qué lab vienen, y qué
   recomendaría hacer con esa plata.
4. **agg vs transform:** largo del groupby-agg vs el transform y por qué.
5. **Modifica y explica (Explorador):** merge `left`→`inner`; qué pasó con el
   saldo total y los sin pago; por qué `left` es lo correcto; revertir.

## 12. Guion de pruebas 🎭 (clon limpio, en orden, evidencia por escenario)

- **E01 — Flujo feliz Explorador:** preparar (descarga matplotlib) → solución
  → ejecutar → informe con `$2,025,000`, tramos 4/11/7/3 y huérfanos $130.500
  → salidas (txt, csv, xlsx, PNG válido) → verificador N-1/N → responder →
  N/N exit 0.
- **E02 — Artesano a medio camino:** plantilla → pistas → SOLO TODO 1 →
  rubros pasa, resto no.
- **E03 — Tramposo:** hardcodear retornos oficiales → datasets sorpresa lo
  cazan ×3.
- **E04 — Perdido:** solución desde guia/ → error de ruta documentado; limpiar.
- **E05 — Rompe cosas:** borrar el PNG → check específico con cura → verde ·
  SyntaxError y breakpoint() estándar · **NUEVO:** inyectar `plt.show()` en
  una copia y ejecutar sin display → documentar el síntoma y confirmar que la
  solución oficial (Agg) no lo sufre · alterar un CSV → verificar_entorno lo
  detecta → git checkout → verde.
- **E06 — Rezagado:** recuperador → N-1/N.
- **E07 — Idempotencia:** preparador ×3 (sin re-descargas tras la 1ª); pipeline
  ×2 → mismas salidas de texto/csv (el PNG puede diferir en metadatos —
  comparar existencia y tamaño, doctrina H-04).
- **E08 — Higiene:** `git status` limpio (`labs/*/tablero.py` ignorado; los 3
  CSV versionados; salidas ignoradas).
- **E09 — Regresión:** verificadores de Labs 01–05 → todos en verde; `git diff`
  limpio fuera del Lab 06 y portada.

## 13. Cambios en archivos existentes (únicas excepciones)
Portada: Lab 06 ✅ Disponible · `.gitignore`: `labs/*/tablero.py`.

## 14. Flujo Git, certificación y DoD
Commits convencionales (`feat: Lab 06 — Transformar y combinar` · `docs: spec
SPEC-007` · `test: certificación del Lab 06 como alumno` + fixes) · reporte
`docs/certificacion-lab-06.md` · CERTIFICADO limpio → tag `lab-06-v1.0.0` +
push directo (protocolo Lab 02/05) · observación abierta → detener y consultar
(protocolo H-01/H-03/H-04).

**DoD:** lab conforme §3–§11 · CSVs verbatim versionados · portada y .gitignore
al día · E01–E09 CERTIFICADO · commits + tag pusheados · hallazgos reportados.

---

*Firmado: El Arquitecto de Puerto Siracusa.*
*"El Concejo vota con los ojos — dale un tablero que no necesite explicación y
un gráfico que no admita discusión."* 🏛️📊📐
