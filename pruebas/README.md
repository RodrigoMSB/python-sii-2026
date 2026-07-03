# Suite de Pruebas del Curso 🚦

> Una prueba automática por cada unidad (6 labs + capstone) que reproduce el
> **flujo feliz del alumno** de punta a punta, y un **CI** que la corre en
> **macOS y Windows reales**. Porque "debería funcionar en Windows" no es un
> veredicto de ingeniería.

## Qué hace cada prueba

Por cada lab, en una **copia temporal** (el repo nunca se toca), reproduce lo que
haría un alumno en su primer día:

1. `uv sync` — monta el entorno del lab (respeta su `uv.lock`).
2. `verificar_entorno.py` — el taller quedó en verde.
3. `recuperar_lab.py` — "el alumno resuelve" (solución + salidas).
4. Corre el verificador y **exige que reclame el interrogatorio** (exit 1): una
   prueba que no puede fallar no prueba nada.
5. Responde el interrogatorio (`RESPUESTAS.md` / `BITACORA.md`) con texto de prueba.
6. Corre el verificador final y exige **`N/N` en verde** + las cifras insignia del
   lab en su informe.

La suite **no duplica** las cifras de control: invoca los verificadores ya
certificados de cada lab. Lo que varía por lab vive como **datos** en
[`flujos.py`](flujos.py); el arnés ([`lib_pruebas.py`](lib_pruebas.py)) es genérico.

## Uso local (macOS o Windows, mismo comando)

```bash
# El curso completo:
uv run --no-project python pruebas/probar_curso.py

# Un lab puntual:
uv run --no-project python pruebas/probar_lab.py lab-05-gran-limpieza
uv run --no-project python pruebas/probar_lab.py lab-03          # basta el prefijo

# Otras opciones:
uv run --no-project python pruebas/probar_curso.py --listar      # lista las unidades
uv run --no-project python pruebas/probar_curso.py --lab lab-04  # solo una
uv run --no-project python pruebas/probar_curso.py --desde lab-05  # desde una en adelante
uv run --no-project python pruebas/probar_curso.py --autocheck   # la suite se prueba a sí misma
```

`--no-project` es a propósito: el arnés es 100 % stdlib y no debe arrastrar el
entorno de ningún lab; cada lab sincroniza el suyo dentro de su copia temporal.

## Duración esperada

- **Primera corrida:** descarga las bibliotecas de los labs 03–06 y capstone
  (numpy, pandas, openpyxl, matplotlib) — puede tomar varios minutos, sobre todo
  matplotlib.
- **Corridas siguientes:** con el caché de `uv`, el curso completo tarda ~2 minutos
  en macOS. Los labs 01–02 son casi instantáneos (sin dependencias).

## El autochequeo (¿la suite puede fallar?)

```bash
uv run --no-project python pruebas/probar_curso.py --autocheck
```

Sabotea deliberadamente una copia (borra la solución del Lab 01) y **afirma que la
prueba falla**. Si el sabotaje pasara inadvertido, la suite avisa que es un adorno
verde. Una suite que no puede fallar no prueba nada.

## CI — el semáforo en Windows real

El workflow [`.github/workflows/pruebas-curso.yml`](../.github/workflows/pruebas-curso.yml)
corre la suite en una **matriz `macos-latest` + `windows-latest`** (`fail-fast: false`,
para ver ambos veredictos).

- **Cómo dispararlo:** botón **"Run workflow"** en la pestaña *Actions* del repo
  (trigger `workflow_dispatch`), o desde la terminal:
  `gh workflow run pruebas-curso.yml`. También corre solo en `push` a `main` que
  toque `labs/**`, `pruebas/**` o el propio workflow.
- **Costo:** el plan gratuito da 2.000 min/mes, y **los runners Windows consumen
  minutos a tasa 2×**. Por eso el disparador principal es **manual** y el `push`
  está filtrado por rutas. Corre la suite completa cuando cambies un lab, no en
  cada commit de documentación.
- **Acciones pineadas** (doctrina H-03): `setup-uv` va fijada por **hash de commit
  inmutable** (Astral dejó de mover los tags mayores para prevenir ataques de
  cadena de suministro); `checkout` y `upload-artifact` por versión exacta.
- **Al fallar:** el workflow sube como *artifact* los logs y las `salidas/` de la
  copia del lab caído (el arnés los deja en `pruebas/_reportes/`, que está en el
  `.gitignore`).

## Contratos (SPEC-009 §3)

- **P1** — el repo jamás se ensucia (copia temporal + limpieza garantizada).
- **P2** — 100 % stdlib, `subprocess` con listas (nunca `shell=True`), utf-8
  tolerante, timeouts, ANSI en Windows.
- **P3** — data-driven: agregar un lab futuro = agregar una entrada en `flujos.py`.
- **P4** — salida `[OK]`/`[ERROR]`/`[INFO]`, resumen `N/N`, exit 0 solo si todo pasa.
- **P5** — la suite se prueba a sí misma (`--autocheck`).
