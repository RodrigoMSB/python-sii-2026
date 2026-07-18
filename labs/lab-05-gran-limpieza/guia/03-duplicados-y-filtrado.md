# Guía 3 — Duplicados y filtrado

> **Objetivo:** eliminar filas repetidas y descartar los códigos malformados,
> conociendo `query()` y las expresiones regulares (regex) en pandas.

REPL abierto (`bash bin/repl.sh`); carga y homogeneiza el censo primero (Guía 2).

## Duplicados: `duplicated()` marca, `drop_duplicates()` ejecuta

```python
>>> df["codigo"].duplicated(keep=False)   # marca TODAS las apariciones repetidas
>>> df.drop_duplicates()                  # borra las filas exactamente repetidas
```

- `duplicated()` **señala** (devuelve True/False); útil para *ver* qué se repite.
- `drop_duplicates()` **actúa** (devuelve el DataFrame sin duplicados).

Dos parámetros que mandan:

- **`subset`** — por qué columnas comparar. `drop_duplicates()` sin `subset`
  compara la fila **entera**; `drop_duplicates(subset="codigo")` compara **solo el
  código**.
- **`keep`** — cuál conservar: `"first"` (por defecto), `"last"` o `False` (borra
  todas las repetidas).

```python
>>> ejemplo = pd.DataFrame({"codigo": ["A", "A", "B"], "deuda": [1, 2, 3]})
>>> ejemplo.drop_duplicates(subset="codigo", keep="last")["deuda"].tolist()
[2, 3]
```

> 🤔 **¿Y si dos filas comparten código pero difieren en deuda?** Ahí `subset` y
> `keep` deciden con cuál te quedas (¿la primera?, ¿la última?, ¿la mayor?). En
> nuestro censo los duplicados son **exactos**, así que `drop_duplicates()` a secas
> basta. Pero guarda la idea: es el corazón del desafío final.

## Filtrado: booleano, `query()` y regex

El filtrado booleano ya lo conoces (Lab 03). Para condiciones legibles, pandas
ofrece **`query()`**, que se lee casi como una frase:

```python
>>> df.query("estado == 'VENCIDA' and deuda > 100000")
```

Y si el umbral está en una **variable externa**, la referencias con `@`:

```python
>>> umbral = 100000
>>> df.query("estado == 'VENCIDA' and deuda > @umbral")
```

Esa es exactamente tu función `vencidas_grandes`.

## Regex: validar el formato del código

Los códigos deben ser `PS-####-Y` (Y ∈ C/G/T). Eso se describe con una **regex**:

```
PS-\d{4}-[CGT]
   │   │    └── una letra entre C, G o T
   │   └─────── exactamente 4 dígitos (\d = dígito, {4} = cuatro)
   └─────────── el prefijo literal "PS-"
```

Y hay **dos** formas de aplicarla, con una diferencia crucial:

```python
>>> s = pd.Series(["PS-1006-G", "PS-999", "XX-1050-G", "PS-1006-GX"])
>>> s.str.fullmatch(r"PS-\d{4}-[CGT]")
0     True
1    False
2    False
3    False
>>> s.str.contains(r"PS-\d{4}-[CGT]")
0     True
1    False
2    False
3     True    # 😲
```

### 💥 Rómpelo: `fullmatch` vs `contains` (el anclaje)

Fíjate en `"PS-1006-GX"`: `fullmatch` lo **rechaza**, pero `contains` lo
**acepta**. ¿Por qué?

- **`fullmatch`** exige que la regex calce con **TODO** el string, de principio a
  fin. `"PS-1006-GX"` tiene una `X` de más al final → no calza entero → `False`.
- **`contains`** solo busca el patrón **en alguna parte** del string. `"PS-1006-GX"`
  contiene `PS-1006-G` adentro → `True`, aunque tenga basura pegada.

Para **validar un formato completo** quieres `fullmatch` (anclado). `contains`
sirve para "¿aparece este patrón en algún lado?", no para validar. Usar `contains`
donde va `fullmatch` deja pasar códigos con basura — un bug silencioso.

Por eso tu `filtrar_codigos` usa **`fullmatch`**:

```python
>>> mascara = df["codigo"].str.fullmatch(r"PS-\d{4}-[CGT]")
>>> validos = df[mascara]
>>> descartados = df[~mascara]     # ~ invierte la máscara: los que NO calzan
```

En el censo, los descartados son exactamente `PS-999` (le faltan dígitos y rubro)
y `XX-1050-G` (prefijo ajeno).

### 🤖 Pregúntale a la IA

> *"Explícame esta regex pieza por pieza: `PS-\d{4}-[CGT]`. ¿Qué hace `\d`, qué
> hace `{4}` y qué significan los corchetes `[CGT]`?"*

## ✅ Checkpoint

- [ ] Distinguiste `duplicated()` (marca) de `drop_duplicates()` (actúa) y sus
      parámetros `subset`/`keep`.
- [ ] Usaste `query()` con una variable externa (`@umbral`).
- [ ] Entendiste `fullmatch` (anclado) vs `contains` (substring) con la regex.
- [ ] Filtraste los códigos y viste los descartados (`PS-999`, `XX-1050-G`).

Cuando esté todo ✔, sigue con **[Guía 4 — Outliers](04-outliers.md)**.
