# Lab 05 — La gran limpieza 🧹

> Módulo 3 (primera parte) · ~2,0 horas · limpieza de datos sucios con pandas ·
> mismas dependencias del Lab 04 (sin descargas nuevas).

## El encargo

El practicante de verano fusionó a mano todas las planillas en un solo archivo
—el **Censo de Patentes de Puerto Siracusa**— y se fue de vacaciones. Vino con
toda la mugre: estados escritos de diez maneras, espacios fantasma, filas
repetidas, deudas "S/I", códigos malformados y una deuda de $9.999.999 que huele
a dedo dormido sobre el teclado.

> «Este censo tiene más mugre que la sentina de un pesquero. Dame un pipeline de
> limpieza.» — Don Arquímedes

Construirás `limpiar.py`: homogeneiza, deduplica, filtra, imputa y detecta
outliers, produciendo el censo limpio + un informe donde **cada fila descartada
queda contada y justificada**.

## Qué vas a aprender

Diagnóstico de calidad (`info`, `value_counts`, `isna`, `describe`) ·
homogeneización con el accessor `.str` · faltantes (`na_values`, `fillna` vs
`dropna`) · duplicados (`drop_duplicates`, `subset`, `keep`) · filtrado con
`query()` y **regex** (`fullmatch` vs `contains`) · **outliers** por IQR y
z-score, y la **decisión de negocio** cuando los métodos no coinciden.

## Dos rutas, un mismo verificador

| Ruta | Para quién | Qué haces |
|------|------------|-----------|
| 🛠️ **Artesano** | Quiero escribir el código | Completas los 6 `TODO` de `plantillas/limpiar.py`. |
| 🔎 **Explorador** | Quiero entender leyendo y probando | Ejecutas `soluciones/limpiar.py`, con la investigación de outliers y la modificación de la Pregunta 5. |

## La regla de la casa (sobre la IA) 🤖

La IA está **invitada**: que te explique una regex o el z-score. Pero el
interrogatorio pregunta por lo que pasó en **TU** terminal (tus variantes, tu
embudo, tu desacuerdo de métodos): eso se entiende, no se copia.

## La lección transversal

**Limpiar no es borrar — es decidir con criterio y dejar rastro.** Los métodos
proponen (IQR, z-score); el analista dispone; y **todo veredicto queda escrito**
(contrato C14: cada fila descartada, contabilizada y justificada).

## Prerrequisitos

- **`uv`** (trae Python 3.13). Instalación:
  [`../../docs/setup-alumno.md`](../../docs/setup-alumno.md). Deps ya cacheadas
  del Lab 04.
- Se recomienda haber hecho los Labs 01–04 (Buceo Fondo Claro, un outlier de este
  lab, viene desde el Lab 01).

Problemas: [`docs/troubleshooting.md`](docs/troubleshooting.md).

## Mapa de las guías

1. **[Guía 1 — El censo del practicante](guia/01-contexto.md)** — entorno y el
   **diagnóstico** antes de tocar nada.
2. **[Guía 2 — Homogeneización](guia/02-homogeneizacion.md)** — `.str`, `na_values`,
   `fillna` vs `dropna`.
3. **[Guía 3 — Duplicados y filtrado](guia/03-duplicados-y-filtrado.md)** —
   `drop_duplicates`, `query()`, regex (`fullmatch` vs `contains`).
4. **[Guía 4 — Outliers](guia/04-outliers.md)** — IQR y z-score, el desacuerdo y
   la decisión del analista.
5. **[Guía 5 — El pipeline](guia/05-pipeline.md)** — armar `limpiar.py`, el embudo
   30→25 y verificar.

## Verifica tu trabajo

Desde la raíz del lab (`labs/lab-05-gran-limpieza/`):

```bash
uv run python bin/verificar.py
```

Meta: `✔ 14/14 verificaciones correctas`. El verificador es de **solo lectura**,
prueba con el censo oficial y con un **censo sorpresa** (mugre aleatoria en un
archivo temporal), y neutraliza cualquier `breakpoint()` olvidado.

## Para el instructor 🧑‍🏫

- **Recuperar a un rezagado:** `uv run python bin/recuperar_lab.py` (restaura el
  censo con `git checkout` si fue alterado, repone `limpiar.py` y `salidas/`).
- **Cifras de control:** censo bruto 30 → dedup 28 → códigos 26 → 3 imputadas →
  IQR {PS-1022-T, PS-1046-C}, z {PS-1046-C} → apartado solo el typo → **censo limpio
  25 filas, $3.107.500**. Estado: 10 variantes crudas → 3.
- **El censo** (`datos/censo_patentes.csv`) es texto versionado: git es su fuente
  de verdad (no hay generador). Restaurar con `git checkout -- datos/censo_patentes.csv`.
- `bin/` solo lectura sobre el trabajo del alumno (salvo `recuperar_lab.py`);
  cuartiles con `quantile` y std muestral (C15); sin `breakpoint()` en
  soluciones/plantillas/bin (C8).
