# El Arenario — El Informe Anual de Rentas 🏖️

> Arquímedes de Siracusa escribió *El Arenario* para demostrar que ningún número
> es demasiado grande para ser contado — ni los granos de arena del universo.
> Este es tu examen de madurez: **contar Puerto Siracusa entero.**

## El encargo

Fin de año en Puerto Siracusa. El Concejo Municipal y la Gobernación Regional
exigen el **Informe Anual de Rentas**: el estado completo de las patentes del
puerto —deudas, pagos, multas, saldos— depurado, cruzado, resumido y graficado.
Don Arquímedes te entrega una caja con todo lo que las oficinas mandaron durante
el año y te dice su frase final:

> *"En este puerto aprendiste que ningún dato es demasiado sucio para limpiarse ni
> ningún número demasiado grande para contarse. Cuenta la arena, analista. El
> Concejo espera."*

Hay dos noticias enterradas en los datos: los ex-huérfanos del tablero (¿los
recuerdas del Lab 06?) por fin se inscribieron... y hay **saldos que darán que
hablar**. Encuéntralos. Explícalos. Ese es el trabajo.

## Lo que hay en la caja (`datos/`, SOLO LECTURA)

- **`censo_anual.csv`** — el padrón de patentes, que volvió a ensuciarse durante el
  año (estados desordenados, faltantes, duplicados, un código malo y un outlier de
  digitación).
- **`fuentes/pagos_anuales.xlsx`** — lo que recaudó Tesorería, en **dos hojas**:
  `S1` (primer semestre) y `S2` (segundo semestre).
- **`multas.json`** — las multas del año, del sistema antiguo.
- **`fuentes/contribuyentes.db`** — el registro maestro (SQLite): código, nombre y
  **giro** de cada contribuyente.

## Lo que debes entregar (en `salidas/`)

Tu solución tiene **estructura libre** (un `arenario.py` o los módulos que
prefieras, en la raíz del capstone). Lo que NO es libre son los **productos** —
esto es exactamente lo que el verificador mide:

1. **`salidas/censo_depurado.csv`** — el censo limpio: columnas
   `codigo,nombre,estado,deuda`, sin duplicados, sin códigos inválidos, sin el
   outlier de consenso.
2. **`salidas/tablero_anual.csv`** y **`salidas/tablero_anual.xlsx`** — el cruce
   completo, columnas exactas:
   `codigo,nombre,estado,deuda,rubro,tramo,giro,pagado,multas,saldo`
   (con **`saldo = deuda + multas − pagado`**; `giro` desde la BD).
3. **`salidas/informe_anual.txt`** — título `INFORME ANUAL DE RENTAS — Puerto
   Siracusa`, y como mínimo: el embudo de depuración con el veredicto de outliers,
   los totales (deuda / pagado / multas / **saldo**), los tramos de deuda, el saldo
   por rubro, cuántos están **al día vs morosos**, la sección de **huérfanos**, y
   una sección **"Hallazgos del analista"** donde EXPLIQUES los saldos negativos.
4. **`salidas/graficos/saldo_por_rubro.png`** y **`salidas/graficos/tramos_de_deuda.png`**
   — dos gráficos de barras, titulados en español (backend Agg, `savefig`; C16).
5. **`salidas/gestion.db`** — tabla `resumen_anual` (una fila por rubro con el
   saldo), escrita con `to_sql`.
6. **`BITACORA.md`** respondida en la raíz — tu defensa escrita (ver
   `plantillas/BITACORA.md`).

## Las reglas del examen

- **Fuentes intocables:** `datos/` es de SOLO LECTURA. Todo lo tuyo va a `salidas/`.
- **Las decisiones de limpieza son las reglas oficiales del curso** (el Concejo
  audita con estas): imputar deuda faltante a **0**; apartar outliers solo por
  **consenso IQR ∩ z-score**; en duplicados exactos, **gana el primero**; formato
  de código válido `PS-####-Y`. (¿Marcador de faltante? Recuerda que no todos los
  "vacíos" se escriben igual — mira bien el censo.)
- **La IA es un asistente permitido**, pero la BITÁCORA se responde con TUS
  resultados y TU criterio.
- **Las pistas están para usarse** (`pistas/`, tres niveles): destaparlas no baja tu
  nota en el verificador. La rúbrica del relator sí pondera cuánta autonomía
  mostraste — pero pedir un mapa no es perderse, es navegar.

## Cómo saber si lo lograste

```bash
uv run python bin/verificar.py
```

Cuando llegue a `✔ 9/9`, Don Arquímedes firma el informe y quedas declarado
**Analista de Datos de Puerto Siracusa**. La nota final la pone el relator con la
**[RUBRICA.md](RUBRICA.md)**.

> *"Dame un punto de apoyo y moveré el mundo."* — Arquímedes de Siracusa.
> Tu punto de apoyo es saber contar la arena. Adelante.
