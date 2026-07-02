# SPEC-002 — Fundación del repositorio y CONSTRUCCIÓN del Lab 01

> **Proyecto:** Curso Programación en Python — SII 2026 · "Puerto Siracusa"
> **Emitido por:** El Arquitecto (Claude) · **Aprobado por:** Rodrigo Silva Bravo (PO)
> **Ejecutor:** mocito (Claude Code) — dueño del repositorio y ÚNICO constructor
> **Fecha:** 2026-07-01 · **Versión:** 2.0 — **SUPERSEDE Y ANULA a SPEC-001**

---

## 0. Qué cambió respecto de SPEC-001

SPEC-001 asumía integrar un zip pre-construido. **Eso queda anulado**: no hay
zip, no habrá zip. En este proyecto mocito construye TODO el código y
contenido; el Arquitecto entrega especificaciones y criterios de aceptación;
el PO aprueba. Este spec es autosuficiente: contiene todo lo necesario para
construir el Lab 01 completo sin ningún artefacto externo.

## 1. Contexto del proyecto

Curso de Python de **20 horas** para funcionarios del SII **sin experiencia
previa en programación**. Filosofía pedagógica (inspirada en los labs
Kafka/Strimzi "Banco Meridiano"):

- **Narrativa continua:** el alumno es Analista de Datos de la ficticia
  **Dirección de Rentas de Puerto Siracusa** (municipio costero). Su jefe:
  **Don Arquímedes**, veterano de Rentas, frase célebre: *"Dame una planilla
  limpia y un punto de apoyo, y moveré el presupuesto municipal."*
- **Dos rutas por lab, un solo verificador:** 🛠️ **Artesano** (completa TODOs
  de `plantillas/`) y 🔎 **Explorador** (ejecuta `soluciones/` pero con
  predicción y modificación obligatorias). Ambas convergen en `bin/verificar.py`.
- **Anti-loro:** verificador con *dataset sorpresa* aleatorio (caza números
  hardcodeados) + interrogatorio `RESPUESTAS.md` obligatorio con preguntas
  cuya respuesta depende de la ejecución local del alumno. La IA está
  INVITADA como asistente de comprensión, nunca prohibida.
- **Aprender rompiendo:** cada guía provoca al menos un error a propósito y
  enseña a leer el traceback.
- **Automático y multiplataforma:** el PO desarrolla en macOS; los alumnos
  usarán mayormente Windows. Cero fricción.

## 2. Datos duros (no inventar, no cambiar)

| Ítem | Valor |
|------|-------|
| Ruta local del proyecto | `/Users/rodrigosilva/SII/PYTHON` |
| Repo GitHub | `python-sii-2026` — **PRIVADO** — cuenta `RodrigoMSB` |
| Rama principal | `main` |
| Python del curso | **3.13** pineado (`.python-version` + `pyproject.toml` por lab) |
| Gestor de entorno | `uv` — un entorno virtual **aislado por lab** |
| Dependencias Lab 01 | **NINGUNA** — 100 % biblioteca estándar |

## 3. Estructura del repositorio

```
/Users/rodrigosilva/SII/PYTHON
├── README.md                    ← portada del curso (§9.1)
├── .gitignore                   ← §9.2
├── specs/SPEC-002.md            ← este documento, versionado
├── docs/setup-alumno.md         ← instalación de uv, macOS + Windows (§9.3)
└── labs/
    └── lab-01-primer-dia/
        ├── README.md
        ├── pyproject.toml
        ├── .python-version      ← contenido: 3.13
        ├── bin/
        │   ├── 00-preparar.sh   ← preparador macOS/Linux
        │   ├── 00-preparar.ps1  ← preparador Windows
        │   ├── lib_comunes.py   ← colores y helpers [OK]/[ERROR]
        │   ├── verificar_entorno.py
        │   ├── verificar.py     ← el verificador del lab
        │   └── recuperar_lab.py ← herramienta del instructor
        ├── datos/cuaderno.py    ← dataset oficial (§5, VERBATIM)
        ├── guia/
        │   ├── 01-contexto.md
        │   ├── 02-variables-y-tipos.md
        │   ├── 03-cadenas.md
        │   ├── 04-listas.md
        │   └── 05-triaje.md
        ├── plantillas/
        │   ├── triaje.py        ← con TODO 1..5
        │   └── RESPUESTAS.md    ← interrogatorio (§7)
        ├── soluciones/
        │   ├── triaje.py        ← solución oficial
        │   └── desafio-mayor-deudor.md
        └── docs/troubleshooting.md
```

## 4. Alcance pedagógico del Lab 01 (sintonía con el temario SII)

Lab de **~2,5 horas**, primera mitad del Módulo 1 del temario adjudicado:
variables, tipos de datos y operaciones (aritméticas, comparación, lógicas) ·
cadenas: indexación, slicing, métodos, f-strings (incl. formato `:,`) ·
listas: creación, indexación, slicing, `append/sort/sorted/sum/max/len`,
la trampa del alias vs `.copy()` · operadores relacionales y de pertenencia
(`in`, `not in`) · `if` y `for` en su forma mínima (recorrer y filtrar).
**Fuera de alcance** (Lab 02): dicts/tuplas/sets, comprensiones, funciones
avanzadas (*args, lambdas, scope), excepciones en profundidad, pdb.

## 5. Dataset oficial — `datos/cuaderno.py` (VERBATIM, es contrato)

El archivo debe declarar `PATENTES`: lista de listas
`[codigo:str, nombre:str, estado:str, deuda:int]`, con docstring que
documente posiciones y formato de código `PS-####-Y` (Y ∈ {C, G, T} =
Comercio, Gastronomía, Turismo). Estados posibles: `VIGENTE`, `VENCIDA`,
`SUSPENDIDA`. Registros EXACTOS (el orden importa):

```python
PATENTES = [
    ["PS-1001-G", "Pescadería La Miríada", "VIGENTE", 0],
    ["PS-1002-C", "Ferretería El Tornillo Feliz", "VIGENTE", 0],
    ["PS-1003-G", "Cocinería Doña Eureka", "VENCIDA", 185000],
    ["PS-1004-T", "Hostal Vista al Faro", "VIGENTE", 0],
    ["PS-1005-C", "Abarrotes El Arenario", "VENCIDA", 92000],
    ["PS-1006-G", "Café La Palanca", "VIGENTE", 45000],
    ["PS-1007-T", "Kayaks Bahía Serena", "SUSPENDIDA", 310000],
    ["PS-1008-C", "Librería El Papiro", "VIGENTE", 0],
    ["PS-1009-G", "Sanguchería El Puerto", "VENCIDA", 127500],
    ["PS-1010-C", "Bazar Las Tres Anclas", "VIGENTE", 0],
    ["PS-1011-T", "Tour Cavernas del Sur", "VENCIDA", 260000],
    ["PS-1012-G", "Heladería Polo Austral", "VIGENTE", 18000],
    ["PS-1013-C", "Botillería La Sirena", "SUSPENDIDA", 405000],
    ["PS-1014-G", "Pizzería La Espiral", "VIGENTE", 0],
    ["PS-1015-T", "Cabañas Punta Norte", "VENCIDA", 149000],
    ["PS-1016-C", "Verdulería Don Ciro", "VIGENTE", 0],
    ["PS-1017-G", "Marisquería El Nivel del Mar", "VIGENTE", 76000],
    ["PS-1018-C", "Paquetería Correo del Istmo", "VENCIDA", 58000],
    ["PS-1019-T", "Museo del Ancla", "VIGENTE", 0],
    ["PS-1020-G", "Jugos La Corriente", "VENCIDA", 33500],
    ["PS-1021-C", "Peluquería Ondas del Pacífico", "VIGENTE", 0],
    ["PS-1022-T", "Buceo Fondo Claro", "SUSPENDIDA", 520000],
    ["PS-1023-G", "Empanadas La Balanza", "VIGENTE", 0],
    ["PS-1024-C", "Ciber La Antena", "VENCIDA", 71000],
]
```

**Verdades derivadas del dataset (cifras de control para pruebas):**
- Total patentes: **24** · Vigentes: **13** · Vencidas: **8** · Suspendidas: 3
- Deuda total (todas): **2.350.000** CLP
- Códigos vencidas, en orden: PS-1003-G, PS-1005-C, PS-1009-G, PS-1011-T,
  PS-1015-T, PS-1018-C, PS-1020-G, PS-1024-C
- Mayor deudor: Buceo Fondo Claro, $520.000 (para el desafío extra)
- Matices pedagógicos intencionales: hay VIGENTES con deuda (Café La Palanca
  45.000, Heladería 18.000, Marisquería 76.000) y SUSPENDIDAS que no son ni
  vigentes ni vencidas. Las guías deben comentar esta "zona gris".

## 6. Contratos de código (para este y todos los labs futuros)

- **C1.** Scripts de `bin/` **solo lectura** sobre el trabajo del alumno
  (verificar/reportar; solo `recuperar_lab.py` escribe, y únicamente lo
  descrito en §8.6) y **100 % stdlib**.
- **C2.** Todo comando del alumno se documenta como `uv run python ...`
  ejecutado desde la raíz del lab.
- **C3.** Formato de salida de verificadores: `[OK] msj`,
  `[ERROR] msj` + línea `Pista: ...`, `[INFO] msj`, resumen final
  `✔|✘ N/N verificaciones correctas`. Exit code 0 solo si TODO pasa.
  Colores ANSI (verde/rojo/amarillo/cian) con activación para Windows
  (`os.system("")` en nt) y degradación limpia si no hay TTY.
- **C4.** `pathlib.Path` para toda ruta; `encoding="utf-8"` explícito en
  toda lectura/escritura de texto. Cero rutas con separadores literales.
- **C5.** El interrogatorio JAMÁS se auto-responde por ninguna herramienta.
- **C6.** Español chileno-neutro profesional; código con nombres en español
  coherentes con las guías (`contar_vigentes`, no `count_active`).

## 7. El interrogatorio — `plantillas/RESPUESTAS.md`

Encabezado que instruya: copiarlo a la raíz del lab como `RESPUESTAS.md` y
responder con palabras propias; marcador de respuesta pendiente EXACTO:
`(escribe aquí tu respuesta)` (el verificador lo cuenta). Las 5 preguntas:

1. **La rotura de la Guía 2:** pegar la última línea del `TypeError` visto
   en SU terminal y explicar qué dice.
2. **Slicing:** cómo extrajo la letra de rubro de `"PS-1007-T"` y por qué
   `codigo[-1]` también funciona.
3. **El número de su triaje:** vencidas y deuda total según SU informe; y si
   la deuda total incluye los $45.000 del Café La Palanca (VIGENTE) — debe
   justificar mirando `deuda_total`.
4. **Predicción de pertenencia:** resultado de `"PS-1013-C" in vencidas`
   (lista manual de la Guía 4), si acertó su predicción y por qué (la
   Botillería está SUSPENDIDA, no VENCIDA).
5. **Modifica y explica:** cambiar `== "VENCIDA"` por `!= "VIGENTE"` en
   `codigos_vencidas`, re-ejecutar, explicar qué códigos aparecen de más y
   qué significa en términos de negocio; luego revertir.

## 8. Especificación por archivo

### 8.1 `soluciones/triaje.py` (y su gemelo `plantillas/triaje.py`)

Programa nivel principiante (solo `for`, `if`, listas, f-strings; SIN
comprensiones, SIN dicts). Estructura obligatoria:

- Constantes de posición: `POS_CODIGO=0, POS_NOMBRE=1, POS_ESTADO=2, POS_DEUDA=3`
  (con comentario del porqué: nombres sobre números mágicos).
- `contar_vigentes(patentes) -> int` — cuenta estado == "VIGENTE".
- `codigos_vencidas(patentes) -> list[str]` — códigos con estado == "VENCIDA",
  en el orden del cuaderno.
- `deuda_total(patentes) -> int` — suma deuda de TODAS las patentes.
- `construir_informe(patentes) -> str` — texto multilinea con f-strings:
  título `INFORME DE TRIAJE — Dirección de Rentas de Puerto Siracusa`,
  línea de `=` × 58, y renglones (alineación con espacios tal cual):
  `Patentes registradas : {n}` · `Patentes vigentes    : {v}` ·
  `Patentes vencidas    : {len(vencidas)}` · `Deuda total          : ${t} CLP`,
  luego lista `  - {codigo}` por cada vencida.
- `main()` — imprime el informe, crea `salidas/` (`mkdir(exist_ok=True)`) y
  escribe `salidas/informe_triaje.txt` (informe + salto final, UTF-8).
- Import del dataset: `from datos.cuaderno import PATENTES` (ejecutable desde
  la raíz del lab). Guard `if __name__ == "__main__":`.

La **plantilla** es el mismo archivo con el cuerpo de las 3 funciones y dos
bloques del informe reemplazados por **TODO 1..5** comentados, cada uno con
pista concreta (TODO 1: for+if+contador, pista `==` · TODO 2: append, pista
`.append(...)` · TODO 3: acumulador sin condición · TODO 4: cuatro f-strings
del resumen · TODO 5: for sobre vencidas agregando `  - codigo`). Los `return`
y el esqueleto quedan para que el archivo corra (devolviendo 0/[] vacíos)
aunque los TODO estén pendientes.

### 8.2 `bin/lib_comunes.py`

Helpers compartidos: paleta ANSI (verde/rojo/amarillo/cian/negrita) con
detección de TTY + `FORCE_COLOR`, activación Windows; funciones `ok()`,
`error(msg, pista="")`, `info()`, `titulo()`, y `resumen() -> int` que
imprime `✔|✘ N/N verificaciones correctas` y retorna 0/1 según contadores.

### 8.3 `bin/verificar_entorno.py`

Solo lectura. Chequea: Python 3.13 en ejecución (con pista de usar
`uv run` si no) · `uv` en PATH y ejecutable · existencia de `.venv/` (pista:
correr el preparador) · estructura de carpetas completa · presencia de
`datos/cuaderno.py`. Cierra con `Entorno en verde. Puedes continuar con la
Guía 2.` si todo pasa.

### 8.4 `bin/00-preparar.sh` y `bin/00-preparar.ps1`

Idempotentes. Flujo: (1) verificar `uv` instalado — si falta, imprimir
instrucciones de instalación (brew/curl en sh; irm|iex en ps1) y salir con
código 1; (2) `uv sync` (crea/sincroniza `.venv` con Python 3.13);
(3) invocar `uv run python bin/verificar_entorno.py`. Salida con colores.
El `.ps1` se documenta con invocación
`powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1`.

### 8.5 `bin/verificar.py` (el corazón del lab)

Solo lectura. Contiene su PROPIA implementación de referencia de las 3
funciones (así no hay números mágicos que mantener) y un generador de
**dataset sorpresa**: 6–10 patentes aleatorias (`random.Random()` SIN
semilla fija — debe variar entre ejecuciones), códigos `ZZ-9###-?`, estados
y deudas sorteados de listas fijas. Verifica, en orden:

1. `triaje.py` existe en la raíz del lab (pista → Guía 5 paso de copia).
2. Se importa sin excepciones (`importlib.util`; capturar CUALQUIER
   excepción y reportar `[ERROR]` con tipo+mensaje y pista de leer el
   traceback — jamás explotar con traceback crudo).
3. Existen y son callables las 3 funciones (pista: no renombrar).
4. Las 3 funciones dan resultados == referencia con el **cuaderno oficial**
   Y con el **cuaderno sorpresa** (mensajes de error deben incluir valor
   obtenido y esperado; pistas orientadas: "¿comparas contra 'VIGENTE'
   exacto?", "la deuda se suma para TODAS las patentes").
5. `salidas/informe_triaje.txt` existe (pista: ejecutar el triaje) y
   contiene la deuda total correcta como substring (pista: re-ejecutar tras
   corregir — informe desactualizado).
6. `RESPUESTAS.md` existe en la raíz y NO contiene ningún marcador
   `(escribe aquí tu respuesta)` (reporta cuántas faltan).

Cierre en verde: mensaje de Don Arquímedes archivando el informe + teaser
del Lab 02.

### 8.6 `bin/recuperar_lab.py` (modo instructor)

Único script que escribe: copia `soluciones/triaje.py` → raíz, ejecuta el
triaje con `sys.executable` para regenerar `salidas/`, y copia
`plantillas/RESPUESTAS.md` → raíz **solo si no existe** (si existe, lo
respeta e informa). Mensaje final explícito: el interrogatorio queda
pendiente a propósito — *"recuperar el código es gratis; recuperar la
comprensión, jamás."*

### 8.7 Las 5 guías (`guia/*.md`)

Redacción original de mocito siguiendo la filosofía; requisitos mínimos por
guía (tono cercano, analogías, convención de bloques "comando que ejecutas"
vs "Salida esperada (puede variar levemente)"):

- **01-contexto.md** — narrativa del encargo; explicación del entorno
  virtual como "taller/mesón aislado" (analogía obligatoria); ejecución del
  preparador según SO con salida esperada; la regla de oro `uv run`; primer
  contacto con el REPL (print, aritmética, cómo salir). Checkpoint final.
- **02-variables-y-tipos.md** — variables como etiquetas; tipos str/int/
  float/bool con ejemplos del municipio; `type()`; 🔮 predicción: `deuda/2`
  es float; operadores aritméticos (incl. `//`, `%`, `**`), de comparación y
  lógicos con el caso "vigente PERO con deuda" (Café La Palanca);
  💥 rómpelo: `"texto: " + numero` → TypeError, leer la última línea primero,
  dos arreglos (`str()` y adelanto de f-string); nota de que el error
  alimenta la Pregunta 1; 🤖 prompt sugerido sobre por qué Python no
  convierte solo. Checkpoint.
- **03-cadenas.md** — anatomía del código `PS-1007-T` (diagrama ASCII);
  indexación desde 0 y negativos; 💥 IndexError con `codigo[9]`; slicing
  `[desde:hasta]` excluyente; métodos encadenados (`.strip().title()` como
  primer "pipeline"), `startswith`, `replace`, `split` (adelanto: devuelve
  lista); f-strings con `:,`; nota Pregunta 2; 🤖 prompt de mini-formatos.
  Checkpoint.
- **04-listas.md** — importar `PATENTES` desde el REPL en la raíz; `len`,
  doble indexación, slicing; 🔮 predicción `PATENTES[2][2]`; construir
  `bandeja` con `append`; `sort()` vs `sorted()` (in-place vs copia);
  `sum/max/reverse`; pertenencia `in`/`not in`; 🔮 ejercicio de la Pregunta 4
  con la lista manual de vencidas y `"PS-1013-C"`; 💥 la trampa del alias
  (`copia = original`) con la analogía de la segunda llave de la misma
  bodega, y `.copy()`; 🤖 prompt de diagrama de memoria. Checkpoint.
- **05-triaje.md** — `if` (indentación como sintaxis, analogía reglamento de
  tránsito) y `for` (patrón recorrer-y-filtrar, puente conceptual a pandas
  del Módulo 2); bifurcación de rutas con comandos de copia para macOS
  (`cp`) y Windows (`Copy-Item`); regla del Artesano trabado >10 min (mirar
  SOLO esa función de la solución, cerrarla, escribirla); modificación
  obligatoria del Explorador (Pregunta 5); ejecución con salida esperada
  (usar las cifras de control §5); comentario de la zona gris
  (vigentes-con-deuda, suspendidas); copia y respuesta del interrogatorio;
  verificación final `12/12`; **desafío extra opcional**: mayor deudor SIN
  `max()` (patrón acumulador con comparación), remitiendo a
  `soluciones/desafio-mayor-deudor.md`. Checkpoint final del lab + teaser
  Lab 02.

### 8.8 `soluciones/desafio-mayor-deudor.md`

Solución del desafío con el patrón "recordar el mayor visto hasta ahora",
salida esperada (Buceo Fondo Claro, $520.000), por qué el patrón importa
(es el abuelo de `df["deuda"].max()`), y la variante del empate (`>` vs `>=`).

### 8.9 `docs/troubleshooting.md` (del lab)

Dos carriles 🍎/🪟 + síntomas comunes: instalación de uv por SO ·
`No module named 'datos'` (carpeta equivocada) · triaje.py no está en la
raíz · informe desactualizado · `SyntaxError` que apunta una línea tarde ·
`IndentationError` · zsh command not found tras instalar · ExecutionPolicy ·
uv no reconocido en PowerShell viejo · acentos rotos (chcp 65001 / Windows
Terminal) · antivirus reteniendo uv. Cierre: técnica universal de leer el
traceback de abajo hacia arriba.

### 8.10 `README.md` del lab y `pyproject.toml`

README: narrativa del encargo (cita de Don Arquímedes), objetivos, tabla de
las dos rutas, "regla de la casa" sobre IA (entender > repetir; el
interrogatorio vive en TU terminal), prerrequisitos (solo uv), mapa de las
5 guías, convención de bloques y cápsulas 🔮/💥/🤖, sección "Verifica tu
trabajo" y sección "Para el instructor". `pyproject.toml`:
`requires-python = "==3.13.*"`, `dependencies = []`, comentario del porqué
del venv sin dependencias (hábito profesional desde el día uno).

## 9. Archivos raíz del repo

### 9.1 README.md portada
Título del curso, narrativa breve, tabla de labs (Lab 01 ✅ Disponible; el
resto "en construcción"), las dos rutas en 4 líneas, inicio rápido
(setup-alumno → lab-01), nota de repo privado/no redistribuir.

### 9.2 .gitignore
Ignorar artefactos de alumno y entorno SIN ignorar material del curso
(usar patrones con ruta): `.venv/`, `__pycache__/`, `*.pyc`,
`.pytest_cache/`, `.DS_Store`, `labs/*/salidas/`, `labs/*/triaje.py`,
`labs/*/RESPUESTAS.md`, `labs/*/desafio.py`. **`uv.lock` de cada lab SÍ se
versiona** (reproducibilidad). `plantillas/` y `soluciones/` completos SÍ
se versionan.

### 9.3 docs/setup-alumno.md
Una página: instalar uv en macOS (brew o curl) y Windows (irm|iex),
verificación `uv --version`, y aclaración de que NO hay que instalar Python
(uv lo trae). Coherente con el troubleshooting del lab.

## 10. Flujo Git (mocito es dueño del repo)

1. `git init` en `/Users/rodrigosilva/SII/PYTHON`, rama `main`.
2. Crear remoto **privado** `RodrigoMSB/python-sii-2026` (`gh repo create`)
   y conectar `origin`. Confirmar con el PO antes de crear si ya existiera.
3. Commits atómicos en español (`feat|fix|docs|test|chore: descripción`):
   fundación → lab 01 → docs → certificación.
4. Tras certificación en verde: tag anotado `lab-01-v1.0.0`, push de `main`
   y del tag.

## 11. Guion de pruebas — "mocito juega a ser alumno" 🎭

Tras construir, ejecutar EN ORDEN desde un **clon limpio** en directorio
temporal (simula al alumno que recién recibe el material). Sin variables
mágicas, sin activar venvs a mano. Registrar comando, salida relevante y
veredicto por escenario.

- **E01 — Flujo feliz, Ruta Explorador:** preparador → `5/5` y `.venv/`
  creado · `uv run python --version` → 3.13.x · copiar solución →
  `uv run python triaje.py` → informe con `Patentes vigentes    : 13` y
  `Deuda total          : $2350000 CLP`, archivo en `salidas/` ·
  verificador → **11/12** con único error de `RESPUESTAS.md`, exit 1 ·
  copiar interrogatorio, responder los 5 marcadores → verificador **12/12**,
  exit 0, mensaje de Don Arquímedes.
- **E02 — Artesano a medio camino:** con plantilla sin tocar, verificador
  reporta los 3 cálculos con valor obtenido vs esperado y pistas útiles,
  exit 1 · completar SOLO el TODO 1 a mano → `contar_vigentes` pasa, el
  resto sigue fallando con pistas.
- **E03 — Tramposo (anti-loro):** `triaje.py` con las 3 funciones
  retornando hardcodeados los valores oficiales (13 / lista de 8 códigos /
  2350000) · correr el verificador **3 veces** → las 3 veces fallan checks
  del cuaderno sorpresa, exit 1 siempre.
- **E04 — Perdido:** ejecutar el triaje desde `guia/` → falla con
  `No module named 'datos'`; confirmar que el síntoma Y la cura están en
  `docs/troubleshooting.md` y que la cura funciona.
- **E05 — Rompe cosas:** borrar `salidas/informe_triaje.txt` → error
  específico con pista, aplicar cura, vuelve a verde · meter `SyntaxError`
  en triaje.py (quitar un `:`) → el verificador NO explota: `[ERROR]` de
  carga con tipo de excepción y pista, exit 1.
- **E06 — Rezagado:** en clon limpio preparado, `recuperar_lab.py` →
  reconstruye código+informe, copia interrogatorio sin responder ·
  verificador → **11/12** (solo interrogatorio pendiente).
- **E07 — Idempotencia:** preparador 2 y 3 veces seguidas → sin errores ni
  duplicaciones.
- **E08 — Higiene:** con el lab "sucio" tras E01–E07, `git status` →
  working tree limpio (el .gitignore hace su pega).

## 12. Reporte de certificación (entregable)

`labs/lab-01-primer-dia/docs/certificacion-lab-01.md`: fecha, macOS y
versiones (uv, Python resuelto); tabla E01–E08 con veredicto
CUMPLE/NO CUMPLE y evidencia breve (2–5 líneas por escenario); sección
**Hallazgos** (todo desvío, aunque el escenario cumpla); veredicto final
**CERTIFICADO** solo con E01–E08 íntegros.

## 13. Protocolo ante problemas

- Ambigüedad o contradicción en este spec → detenerse y consultar al
  Arquitecto vía PO; no improvisar contratos.
- Problema del entorno de mocito (permisos, red, auth de gh) → resolver,
  anotar en Hallazgos, continuar.
- Prohibido: cambiar contratos (§6), las cifras de control (§5), los nombres
  de funciones/archivos, o auto-responder el interrogatorio.

## 14. Definición de terminado (DoD)

- [ ] Repo local + remoto privado `RodrigoMSB/python-sii-2026` conectados,
      `main` pusheada.
- [ ] Estructura §3 completa; portada, .gitignore y setup-alumno conformes §9.
- [ ] Lab 01 construido conforme §4–§8; `uv.lock` versionado.
- [ ] E01–E08 ejecutados; certificación con veredicto **CERTIFICADO**.
- [ ] Commits convencionales + tag `lab-01-v1.0.0` pusheados.
- [ ] Hallazgos reportados (aunque sea "sin hallazgos").

---

*Firmado: El Arquitecto de Puerto Siracusa. Esta vez, especificando — que
construir le toca a mocito.* 🏛️📐
