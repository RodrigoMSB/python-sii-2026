# SPEC-008 — Capstone: "El Arenario" 🏖️

> **Proyecto:** Curso Programación en Python — SII 2026 · "Puerto Siracusa"
> **Emitido por:** El Arquitecto (Claude) · **Aprobado por:** Rodrigo Silva Bravo (PO)
> **Ejecutor:** mocito (Claude Code) — dueño del repositorio y único constructor
> **Fecha:** 2026-07-02 · **Versión:** 1.0
> **Dependencias:** repo con tags `lab-01..06-v1.0.0` (los 6 labs regulares completos)

---

## ⚠️ 0. Verificación del Arquitecto (leer PRIMERO)

**Premisas verificadas por el Arquitecto:**
- ✅ **Sin dependencias nuevas:** las mismas cuatro pineadas y validadas
  (`numpy==2.5.0`, `pandas==3.0.3`, `openpyxl==3.1.5`, `matplotlib==3.11.0`).
- ✅ **Cifras de control computadas con el pipeline de referencia COMPLETO en
  pandas real** (§5.6): censo bruto **31** → dedup **29** → códigos válidos **28**
  → **3** imputaciones → consenso IQR∩z aparta solo **PS-1047-T** ($8.888.888; IQR
  también marcó a PS-1022-T/Buceo, que se conserva) → **censo depurado 27 filas,
  deuda $3.238.000** · pagos anuales (xlsx, 2 hojas): S1 20 filas $1.213.000 + S2
  11 filas $1.340.000 = **31 pagos, $2.553.000** · pago huérfano **{PS-1050-C} =
  $30.000** · multas huérfanas **{PS-1029-C, PS-1036-T} = $120.000** · tablero
  anual 27 filas: pagado $2.523.000, multas aplicadas $275.000, **SALDO ANUAL
  $990.000** · tramos {Sin deuda: 4, Baja: 13, Media: 7, Alta: 3} · saldo por rubro
  {Comercio: 193.500, Gastronomía: 6.500, Turismo: 790.000} · **al día (saldo ≤ 0):
  16 · morosos: 11** · pivote saldo rubro×estado con el **saldo NEGATIVO −$202.000
  en Comercio/VENCIDA** (sobrepagos + efecto de la imputación a 0 — el giro final).
- ✅ Doctrinas vigentes: H-03 (versiones sin yank), H-04 (binarios vía semilla +
  generador solo-faltantes), H-05 (marcador de faltante desconocido: **`s/d`**).
- ✅ Alcance: **proyecto integrador del temario completo** (Módulos 1–3). NO
  introduce contenido nuevo — evalúa lo aprendido.

**Supuestos a validar por el PO o mocito ANTES de ejecutar:**
1. Repo en `main` limpio; Labs 01–06 certificados intactos.
2. Sin cambios de sistema desde SPEC-007 (deps en caché; `uv sync` sin red).

---

## 1. Qué es El Arenario (y qué NO es)

Arquímedes de Siracusa escribió *El Arenario* para demostrar que ningún número es
demasiado grande para ser contado. Nuestro Arenario es el examen de madurez del
curso: **contar Puerto Siracusa entero**.

**NO es un lab más.** No hay guías paso a paso, no hay Ruta Explorador, no hay
TODOs. Hay un **escenario**, un **objetivo medible**, **pistas graduadas** que el
alumno destapa solo si las necesita, un **verificador** implacable y una **rúbrica**
con la que el relator evalúa. Filosofía del capstone Meridiano: *se evalúa lo que
diseñas, no la plomería provista.*

El escenario base va en `escenario/ESCENARIO.md` (encargo de fin de año: el Informe
Anual de Rentas; la caja con las 4 fuentes; los ex-huérfanos inscritos y los saldos
que dan que hablar).

## 2. Datos duros

| Ítem | Valor |
|------|-------|
| Carpeta | `labs/capstone-el-arenario/` |
| Duración objetivo | ~2,0 horas (cierra el presupuesto: 7 labs / 20 hrs) |
| Python / deps | 3.13 · las cuatro pineadas de siempre |
| Modalidad | **Solo Ruta Artesano** — el alumno construye libre |
| Tags al certificar | `capstone-v1.0.0` **y** `curso-v1.0.0` (cierre del curso) |

## 3. Estructura del capstone

```
labs/capstone-el-arenario/
├── README.md · pyproject.toml · .python-version
├── bin/ (00-preparar.sh/.ps1 · lib_comunes.py · verificar_entorno.py ·
│         verificar.py · recuperar_lab.py · generar_fuentes.py)
├── escenario/ (ESCENARIO.md · RUBRICA.md)
├── pistas/ (nivel-1-orientacion.md · nivel-2-plan.md · nivel-3-fragmentos.md)
├── datos/
│   ├── fuentes_semilla.py       ← VERBATIM (§5) — única fuente de verdad
│   ├── censo_anual.csv          ← VERBATIM directo (texto)
│   ├── multas.json              ← VERBATIM directo (texto)
│   └── fuentes/ (pagos_anuales.xlsx [S1,S2] · contribuyentes.db)  ← generadas (H-04)
├── plantillas/BITACORA.md
├── soluciones/arenario.py       ← implementación de REFERENCIA (instructor)
└── docs/troubleshooting.md
```

## 4. Objetivo medible y entregables contractuales

Estructura de la solución **libre** (un `arenario.py` o los módulos que el alumno
quiera) en la raíz del capstone. Lo que NO es libre son los **productos** que el
verificador y la rúbrica miden en `salidas/`:

1. `censo_depurado.csv` — 27 filas, `codigo,nombre,estado,deuda`, deuda $3.238.000,
   sin duplicados, sin códigos inválidos, sin el outlier de consenso.
2. `tablero_anual.csv` **y** `.xlsx` — 27 filas, columnas
   `codigo,nombre,estado,deuda,rubro,tramo,giro,pagado,multas,saldo`
   (`saldo = deuda + multas − pagado`; giro desde la BD).
3. `informe_anual.txt` — título `INFORME ANUAL DE RENTAS — Puerto Siracusa`, con:
   embudo de depuración (31→29→28→27 con veredicto de outliers), totales
   (deuda/pagado/multas/**saldo $990.000**), tramos, saldo por rubro, **al día 16 /
   morosos 11**, huérfanos (pago PS-1050-C $30.000; multas $120.000) y una sección
   **"Hallazgos del analista"** con la explicación de los saldos negativos.
4. `salidas/graficos/` — DOS PNG válidos: `saldo_por_rubro.png` y `tramos_de_deuda.png`
   (Agg + savefig, C16).
5. `salidas/gestion.db` — tabla `resumen_anual` (una fila por rubro con saldo, `to_sql`).
6. `BITACORA.md` respondida en la raíz (§7).

Reglas (en ESCENARIO.md): fuentes de solo lectura · decisiones de limpieza = reglas
oficiales del curso (imputación a 0, consenso IQR∩z, gana-el-primero) · IA permitida
como asistente, pero la bitácora se responde con TUS resultados · pistas graduadas
sin penalización del verificador (la rúbrica del relator sí pondera autonomía).

## 5. Datos (VERBATIM, son contrato)

### 5.1 `datos/censo_anual.csv` — 31 filas brutas
Las 25 filas del censo limpio del Lab 06 (§5.1) re-ensuciadas con las variantes de
estado del Lab 05/06 y los tres marcadores de faltante en PS-1043-G (vacío),
PS-1044-C (`S/I`) y PS-1045-T (**`s/d`**, H-05), **más** 6 filas al final:
PS-1032-C/PS-1040-G (ex-huérfanos inscritos), PS-1047-T ($8.888.888, outlier nuevo),
PS-77 (código malformado), y PS-1005-C + PS-1031-G (dos duplicados exactos). mocito
construye el CSV fila a fila y **verifica contra §0 antes de versionar**.

### 5.2 `PAGOS_S1` (hoja "S1") — 20 filas
Los 20 pagos del Lab 06 (junio+julio), total $1.213.000.

### 5.3 `PAGOS_S2` (hoja "S2") — 11 filas
Total $1.340.000. PS-1005-C paga de nuevo (sobrepago intencional); PS-1050-C es
huérfano.

### 5.4 `datos/multas.json` — 10 multas
VERBATIM del Lab 04, total $395.000. PS-1029-C y PS-1036-T no están en el depurado →
multas huérfanas $120.000.

### 5.5 `CONTRIBUYENTES_BD` — 27 filas `[codigo, nombre, giro]`
Los 27 códigos del censo depurado, con giro coherente (los 10 del Lab 04 se reutilizan).
Generada en `contribuyentes.db` vía el generador.

### 5.6 Cifras de control consolidadas
Las de §0 — el verificador las implementa vía referencia propia, jamás hardcodeadas
sueltas sin la referencia.

## 6. Contratos
Rigen **C1–C17** completos. Se agrega:
- **C18:** el verificador mide **productos** (archivos + cifras), no estructura
  interna del código del alumno. La calidad del código la evalúa el relator con la
  rúbrica — separación limpia máquina-verifica / humano-pondera.

## 7. La Bitácora del Analista — `plantillas/BITACORA.md`
Reemplaza al interrogatorio (marcador estándar; H-02 vigente). 5 preguntas: el
embudo (justificar cada descarte con la regla oficial) · el veredicto de outliers
(por qué se conserva Buceo por tercera vez) · los saldos negativos (quiénes y las
dos causas: operacional y consecuencia de la imputación) · los huérfanos del año ·
la retrospectiva (qué regla oficial cambiarías y qué cifra cambiaría).

## 8. La Rúbrica — `escenario/RUBRICA.md`
Cuatro criterios con peso: Exactitud verificada 40 % · Calidad del pipeline 25 % ·
Informe y visualizaciones 20 % · Bitácora 15 %. Escala por criterio Excelente (100)
/ Logrado (75) / Básico (50) / Insuficiente (0) con descriptores concretos.
Conversión puntaje→nota con 60 % de exigencia (aprueba con 4,0 en escala 1–7).

## 9. Las pistas graduadas — `pistas/`
Cada archivo abre con *"Destapa solo lo que necesites. Pedir un mapa no es
perderse; es navegar."* Nivel 1 (orientación, sin código: orden de batalla + qué
lab cubre cada etapa + 3 preguntas-brújula) · Nivel 2 (plan, pseudocódigo con
entradas/salidas y las trampas señalizadas) · Nivel 3 (fragmentos casi-solución de
los pasos duros: dos hojas del xlsx, el `s/d`, el consenso, el doble merge con
validate, el to_sql, el gráfico headless — cada uno con el último paso para el alumno).

## 10. Verificadores

### 10.1 `verificar_entorno.py`
Estándar + las 4 fuentes presentes (censo 31, multas 10, xlsx con hojas S1/S2, db
consultable; pista del generador/git según corresponda).

### 10.2 `bin/verificar.py` — mide PRODUCTOS (C18)
Referencia propia completa. Checks: censo_depurado.csv (27×4, deuda 3.238.000, sin
duplicados, todos los códigos válidos, sin PS-1047-T ni PS-77) · tablero csv y xlsx
(27 filas, 10 columnas, pagado 2.523.000, multas 275.000, saldo 990.000) · tramos
{4,13,7,3} · saldo por rubro == §0 · al día 16 / morosos 11 · informe contiene
`990,000`, el embudo `31`→`27`, `PS-1050-C` y la sección de hallazgos con saldo
negativo · los DOS PNG válidos (firma `\x89PNG`, > 5 KB) · gestion.db con
resumen_anual de 3 filas · BITACORA sin marcadores. **Sin dataset sorpresa**; el
anti-loro es la consistencia: el verificador RE-DERIVA todo desde las fuentes y
compara contra los archivos del alumno (fabricar los 6 productos coherentes a mano
cuesta más que hacer el pipeline). Cierre en verde: Don Arquímedes firma, cita a
Arquímedes y declara al alumno **Analista de Datos de Puerto Siracusa**. 🎓

### 10.3 `recuperar_lab.py` — SOLO INSTRUCTOR
Advertencia en pantalla: reconstruye los productos desde la referencia PARA
DEMOSTRACIÓN; el rescate NO certifica al alumno (la rúbrica manda). BITÁCORA jamás
se toca.

## 11. Guion de pruebas 🎭 (adaptado a capstone; clon limpio, evidencia)

- **E01 — El alumno competente:** resolver el capstone COMPLETO con la solución de
  referencia → los 6 productos → verificador N/N exit 0 (con BITACORA dummy).
- **E02 — El alumno a medias:** solo censo_depurado.csv correcto → el verificador
  reporta CADA producto faltante con pista (no la respuesta). Exit 1.
- **E03 — El fabricante:** informe con cifras correctas PERO tablero inconsistente
  (saldo alterado) → el verificador detecta la inconsistencia contra las fuentes.
  Exit 1.
- **E04 — Perdido:** ejecutar desde subcarpeta → error de rutas documentado con cura.
- **E05 — Rompe cosas:** borrar un PNG → check específico · corromper el xlsx →
  entorno lo detecta → generador solo-faltantes lo repone (H-04) · SyntaxError/
  breakpoint estándar sobre la referencia.
- **E06 — Rescate de demostración:** recuperador → productos reconstruidos +
  advertencia de solo-instructor + BITÁCORA pendiente.
- **E07 — Idempotencia:** preparador ×3; generador ×2 sin ensuciar git; pipeline de
  referencia ×2 → productos de texto idénticos.
- **E08 — Higiene:** `git status` limpio (artefactos del alumno y salidas/ ignorados;
  semilla, csv, json y fuentes generadas versionadas).
- **E09 — Regresión FINAL:** los verificadores de los 6 labs en flujo rápido → TODOS
  en verde. El curso entero se certifica de una pasada.

## 12. Cierre del curso (además del capstone)
1. Portada del repo: capstone ✅ Disponible + tabla final de 7/7 + sección "El viaje
   completo" (una línea por lab encadenando la narrativa).
2. `docs/guia-del-relator.md` (NUEVO, máx. 2 páginas): mapa horas-por-lab vs los 3
   módulos, flujo de una sesión tipo, cómo usar recuperadores y verificadores, y cómo
   aplicar la rúbrica del capstone.
3. Tags: `capstone-v1.0.0` y, con TODO verde (E09 incluido), **`curso-v1.0.0`**.

## 13. Flujo Git, certificación y DoD
Commits convencionales (`feat: Capstone — El Arenario` · `docs: spec SPEC-008,
rúbrica y guía del relator` · `test: certificación del capstone y regresión final
del curso` + fixes) · reporte `docs/certificacion-capstone.md` · CERTIFICADO limpio
→ tags `capstone-v1.0.0` + `curso-v1.0.0` pusheados · observación abierta → detener y
consultar (protocolo H-01/H-03/H-04).

**DoD:** capstone conforme §3–§10 · pistas y rúbrica completas · guía del relator ·
portada final · E01–E09 CERTIFICADO (incluida la regresión de los 6 labs) · commits +
AMBOS tags pusheados · hallazgos reportados.

---

*Firmado: El Arquitecto de Puerto Siracusa.*
*"Ningún dato es demasiado sucio para limpiarse; ningún número, demasiado grande
para contarse. Cuenta la arena, analista."* 🏛️🏖️📐
