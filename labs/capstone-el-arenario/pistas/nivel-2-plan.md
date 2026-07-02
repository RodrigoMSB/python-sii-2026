# Pista Nivel 2 — Plan de ataque 📋

> *Destapa solo lo que necesites. Pedir un mapa no es perderse; es navegar.*

Pseudocódigo por etapas, con entradas/salidas y las **trampas señalizadas** ⚠️.
No es código copiable: es el plan. El código lo escribes tú.

## Etapa A — Depurar el censo

```
entrada: datos/censo_anual.csv
  cargar con read_csv, declarando na_values = los TRES marcadores de faltante
     ⚠️ TRAMPA: uno de ellos es 's/d' (minúscula), que NO es NA por defecto de pandas
  homogeneizar: estado -> strip().upper(); nombre -> strip()
  drop_duplicates()                         # gana el primero
  filtrar: quedarse con codigo que cumpla PS-\d{4}-[CGT]  (str.fullmatch)
  imputar: deuda faltante -> 0, y pasar la columna a int
  outliers: IQR (quantile .25/.75) y z-score (std muestral)
            apartar SOLO los que estén en AMBOS conjuntos (consenso ∩)
salida: censo_depurado (DataFrame)
```

## Etapa B — Cargar las otras fuentes

```
pagos:  read_excel(xlsx, sheet_name=...)     # ⚠️ TRAMPA: son DOS hojas (S1 y S2);
        apílalas (concat, ignore_index)        léelas ambas y únelas
multas: json.load -> DataFrame
contrib: sqlite3 + read_sql("SELECT codigo, giro FROM contribuyentes")
```

## Etapa C — Combinar y calcular

```
agrupar pagos por codigo (sum)   -> 'pagado'   ⚠️ TRAMPA: agrupa ANTES de unir,
agrupar multas por codigo (sum)  -> 'multas'      o el merge no será 1:1
partir de censo_depurado; agregar:
  rubro  = codigo.str[-1].map({C:Comercio, G:Gastronomía, T:Turismo})
  tramo  = pd.cut(deuda, bins=[-1,0,100000,300000,1e9], labels=[...])
merge (how="left", validate="1:1") con: contrib(giro), pagado, multas
  pagado y multas: NaN -> 0
  saldo = deuda + multas − pagado            ⚠️ TRAMPA: el saldo incluye las MULTAS
huérfanos: pagos/multas cuyo codigo NO está en el censo depurado (anti-join con isin)
salida: tablero (27 filas, 10 columnas) + huérfanos
```

## Etapa D — Agregar, graficar, informar

```
resumen por rubro: groupby("rubro")["saldo"].sum()   (3 filas -> gestion.db, to_sql)
al día = (saldo <= 0).sum() ; morosos = (saldo > 0).sum()
gráficos (Agg + savefig, C16):
  saldo_por_rubro.png  = barras del saldo por rubro
  tramos_de_deuda.png  = barras del conteo por tramo
informe: embudo + totales + tramos + saldo por rubro + al día/morosos +
         huérfanos + SECCIÓN "Hallazgos del analista" (explica los saldos < 0)
```

## Los 6 productos (checklist)

- [ ] `salidas/censo_depurado.csv`
- [ ] `salidas/tablero_anual.csv` y `.xlsx`
- [ ] `salidas/informe_anual.txt` (con sección de hallazgos)
- [ ] `salidas/graficos/saldo_por_rubro.png` y `tramos_de_deuda.png`
- [ ] `salidas/gestion.db` (tabla `resumen_anual`)
- [ ] `BITACORA.md` respondida

> ¿Trabado en un paso concreto (las dos hojas, el consenso, el doble merge)? La
> **Pista Nivel 3** trae fragmentos de código casi-completos — con el último paso
> tuyo.
