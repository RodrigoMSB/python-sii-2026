# Guía 5 — El consolidado

> **Objetivo:** juntar las cuatro fuentes en `fuentes.py`, registrar el pago
> transaccionalmente, exportar el resumen a los cuatro formatos y pasar el
> verificador.

## Elige tu ruta

El programa se llama `fuentes.py`. Copia el archivo a la raíz del lab.

### 🛠️ Ruta Artesano — completas los TODO

```bash
cp plantillas/fuentes.py fuentes.py          # macOS/Linux
```
```powershell
Copy-Item plantillas\fuentes.py fuentes.py   # Windows
```
Completa los **6 TODO** en orden. Cada carga es casi una línea (lo difícil ya lo
hiciste en las guías); el TODO 4 (`registrar_pago`) es el grande: sigue el guion
commit/rollback que viste en la Guía 4. ¿Trabado? Mira SOLO esa función en
`soluciones/fuentes.py`.

### 🔎 Ruta Explorador — ejecutas y experimentas

```bash
cp soluciones/fuentes.py fuentes.py          # macOS/Linux
```
```powershell
Copy-Item soluciones\fuentes.py fuentes.py   # Windows
```
Obligatorio: harás la modificación de la **Pregunta 5**.

## Ejecuta el consolidado

Desde la raíz del lab:

```bash
uv run python fuentes.py
```

**Salida esperada (puede variar levemente):**

```
INGRESOS DEL MES — Dirección de Rentas de Puerto Siracusa
==========================================================
Pagos (Tesorería)     : $677,500 CLP
Permisos (Turismo)    : $1,000,000 CLP
Multas (sistema)      : $395,000 CLP
----------------------------------------------------------
TOTAL                 : $2,072,500 CLP

Registro transaccional:
  Pago válido   : ACEPTADO (commit)
  Pago inválido : RECHAZADO (rollback — código inexistente)

[INFO] Informe y exportaciones en: .../salidas
```

Fíjate en la sección **Registro transaccional**: el programa intentó dos pagos.
El de `PS-1031-G` (que SÍ está en `contribuyentes`) fue **ACEPTADO** (commit); el
de `PS-9999-X` (que no existe) fue **RECHAZADO** (rollback). Ninguna media
boleta. La base de datos, por fin, sin miedo.

## La vuelta a las oficinas: la exportación

El informe no se queda en un `.txt`: viaja de vuelta a cada oficina **en su
propio dialecto**. Mira lo que apareció en `salidas/`:

```bash
ls salidas/
#   informe_fuentes.txt  resumen.csv  resumen.xlsx  resumen.json  gestion.db  registro.db
```

- `resumen.csv` / `resumen.json` → ábrelos como texto, se leen a ojo.
- `resumen.xlsx` → ábrelo con **Excel / Numbers / LibreOffice** (es un Excel de
  verdad).
- `gestion.db` → consúltalo con SQLite:
  ```python
  >>> import sqlite3
  >>> con = sqlite3.connect("salidas/gestion.db")
  >>> try:
  ...     print(con.execute("SELECT * FROM resumen_mensual").fetchall())
  ... finally:
  ...     con.close()          # C11: siempre explícito (ver Guía 4)
  ...
  [('pagos', 677500), ('permisos', 1000000), ('multas', 395000), ('total', 2072500)]
  ```

Los cuatro métodos `to_csv` / `to_excel` / `to_json` / `to_sql` son el **espejo**
de los cuatro lectores del principio. Leer y escribir cada formato: eso es cerrar
el círculo del Módulo 2.

## 🔧 La modificación obligatoria (Pregunta 5)

En `main`, cambia el pago **válido** por uno con un código que **NO** esté en
`contribuyentes`:

```python
    pago_ok = registrar_pago(bd_trabajo, "PS-0000-Z", hoy, 22000)   # código inexistente
```

Re-ejecuta y observa: la línea "Pago válido" del informe ahora dirá **RECHAZADO**,
y la tabla `pagos_registrados` de tu copia (`salidas/registro.db`) quedará **vacía**.
Explica por qué (¿qué hizo tu `registrar_pago` al no encontrar el código?) y
**revierte** a `PS-1031-G`.

## Responde el interrogatorio y verifica

```bash
cp plantillas/RESPUESTAS.md RESPUESTAS.md          # macOS/Linux
```
```powershell
Copy-Item plantillas\RESPUESTAS.md RESPUESTAS.md   # Windows
```

Responde las 5 preguntas (varias piden lo que viste en TU terminal: la boleta sin
timbre, el rollback, el tipo de `json.load`, el dtype del dinero). Luego:

```bash
uv run python bin/verificar.py
```

Meta: `✔ 12/12 verificaciones correctas` y el mensaje de Don Arquímedes. El
verificador prueba tus lectores con **fuentes sorpresa** (archivos aleatorios en
una carpeta temporal) y tu transacción sobre una **copia** de la BD: si copiaste
cifras fijas, el sorpresa te delata.

## 🏅 Desafío extra (opcional): la quinta fuente

Tesorería manda un CSV rebelde: separado por `;` y con decimales por coma. Léelo
con las perillas correctas de `read_csv` (`sep=";"`, `decimal=","`). La solución
está en
[`../soluciones/desafio-quinta-fuente.md`](../soluciones/desafio-quinta-fuente.md).

## ✅ Checkpoint final del Lab 04

- [ ] Entendiste los cuatro lectores y los cuatro `to_*` (leer y escribir).
- [ ] Copiaste `fuentes.py` a la raíz por tu ruta (🛠️ o 🔎).
- [ ] El informe muestra `$2,072,500` y el pago inválido RECHAZADO (rollback).
- [ ] Abriste los cuatro exportados de `salidas/` (incluido el `.xlsx` con Excel).
- [ ] Hiciste el experimento de la Pregunta 5 y lo revertiste.
- [ ] Respondiste las 5 preguntas y el verificador dice `✔ 12/12`.

---

🎉 **¡Domaste las cuatro fuentes!** Leíste CSV, Excel, JSON y SQLite; registraste
un pago de forma transaccional (commit y rollback, sin medias boletas); y
exportaste el informe de vuelta en los cuatro formatos. Con esto **cierras el
Módulo 2**: ya sabes traer datos de donde vivan y devolverlos a donde vayan.

> **Teaser — Lab 05:** hasta ahora los datos llegaron ordenaditos, casi de
> laboratorio. Se acabó la buena vida: en el **Módulo 3** los datos llegan
> **SUCIOS** —espacios de más, mayúsculas mezcladas, celdas vacías, duplicados,
> fechas en tres formatos distintos—. La **gran limpieza** te espera. Nos vemos
> en el mesón. ⚓
