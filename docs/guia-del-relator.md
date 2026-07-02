# Guía del Relator — Curso Python SII 2026 · Puerto Siracusa

> Para quien dicta el curso. Cómo está armado, cómo correr una sesión y cómo
> evaluar. Dos páginas, al grano.

## El mapa: 20 horas, 3 módulos, 7 unidades

El curso es **7 unidades** (6 labs + capstone) con **narrativa continua**: el
alumno es analista de la Dirección de Rentas de Puerto Siracusa y su jefe, Don
Arquímedes, le encarga tareas reales. Cada unidad produce el insumo de la siguiente.

| Unidad | Tema | Módulo del temario | Horas aprox. |
|--------|------|--------------------|:------------:|
| Lab 01 — El primer día | Variables, tipos, listas, `for`/`if` | **Módulo 1** — Fundamentos | ~2,5 |
| Lab 02 — El cuaderno crece | Dicts/tuplas/sets, funciones, excepciones, pdb | **Módulo 1** | ~2,5 |
| Lab 03 — Los números del puerto | NumPy + pandas (intro) | **Módulo 2** — Datos | ~2,0 |
| Lab 04 — Las cuatro fuentes | CSV/Excel/JSON/SQLite + transacciones | **Módulo 2** | ~2,0 |
| Lab 05 — La gran limpieza | Limpieza: duplicados, faltantes, outliers | **Módulo 3** — Análisis | ~2,0 |
| Lab 06 — Transformar y combinar | map/cut/merge/groupby + Matplotlib | **Módulo 3** | ~2,0 |
| Capstone — El Arenario | Proyecto integrador (todo) | **Módulos 1–3** | ~2,0 |

Total lectivo ≈ **15 h**; el resto de las 20 h son holgura para exposición,
preguntas y ritmo de un grupo sin experiencia previa.

## El flujo de una sesión tipo

Cada lab está pensado para una sesión con tres momentos:

1. **Exposición (20–30 min):** presentas el encargo narrativo del lab (el `README`
   del lab y la Guía 1 sirven de guion) y el concepto nuevo del día.
2. **Laboratorio (60–80 min):** el alumno elige ruta —🛠️ **Artesano** (completa los
   `TODO`) o 🔎 **Explorador** (ejecuta la solución prediciendo y modificando)— y
   avanza por las guías numeradas. Ambas rutas convergen en el mismo verificador.
3. **Interrogatorio y cierre (15–20 min):** el alumno responde `RESPUESTAS.md` (en el
   capstone, `BITACORA.md`) con lo que vio en SU terminal, y corre el verificador
   hasta `N/N`. Cierras conectando con el encargo del siguiente lab (los verificadores
   traen un *teaser*).

## Herramientas para la clase

- **Preparador** (`bin/00-preparar.sh` / `.ps1`): monta el entorno del lab con `uv`
  (Python 3.13 aislado) y verifica que todo esté en verde. Idempotente. Los labs
  03–06 y el capstone descargan bibliotecas la primera vez (matplotlib es la más
  pesada).
- **Verificador** (`bin/verificar.py`): de solo lectura, con salida `[OK]/[ERROR]` y
  pistas. Usa **datasets sorpresa aleatorios** (anti-copia) y exige el interrogatorio
  respondido. En el capstone mide **productos**, no el código.
- **Recuperador** (`bin/recuperar_lab.py`): repone código y salidas de un alumno
  rezagado, **sin responder** el interrogatorio. Úsalo para desatascar, no para
  regalar la nota. En el capstone es **solo demostración** y NO certifica.
- **Multiplataforma:** el PO desarrolla en macOS; los alumnos usan mayormente
  Windows. Cada lab trae `docs/troubleshooting.md` con curas por sistema.

## Filosofía de evaluación

- **Labs 01–06:** la meta es el verificador en verde (`N/N`) con el interrogatorio
  respondido con criterio. El anti-loro (dataset sorpresa) impide aprobar copiando
  números; el interrogatorio, aprobar copiando código.
- **Capstone — El Arenario:** examen de madurez. El **verificador** (9 checks)
  comprueba la exactitud de los 6 productos; la **rúbrica**
  (`labs/capstone-el-arenario/escenario/RUBRICA.md`) la aplicas tú:
  - Exactitud verificada **40 %** · Calidad del pipeline **25 %** · Informe y
    gráficos **20 %** · Bitácora **15 %**.
  - Puntúa cada criterio (Excelente 100 / Logrado 75 / Básico 50 / Insuficiente 0),
    calcula el puntaje ponderado `P` y conviértelo a nota (60 % de exigencia):
    `P ≥ 60 → nota = 4 + (P−60)/40·3`; `P < 60 → nota = 1 + P/60·3`. Aprueba con **4,0**.
  - **La exactitud no basta:** un informe sin explicar los hallazgos o una bitácora
    vacía bajan la nota aunque el verificador esté verde. El capstone premia el
    criterio del analista, no solo que los números cuadren.

## Reproducibilidad y continuidad

Todo el curso corre con `uv` y versiones **pineadas exactas** (`uv.lock`
versionado): en la máquina del alumno se instala lo mismo que en la tuya. La
narrativa está encadenada de punta a punta (ver "El viaje completo" en el `README`
del repo): los datos de un lab reaparecen en el siguiente, y el capstone los reúne
todos. Esa continuidad **es** parte de la pedagogía: al final, el alumno ha contado
Puerto Siracusa entero.
