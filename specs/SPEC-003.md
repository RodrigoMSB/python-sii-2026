# SPEC-003 — Lab 02: "El cuaderno crece"

> **Proyecto:** Curso Programación en Python — SII 2026 · "Puerto Siracusa"
> **Emitido por:** El Arquitecto (Claude) · **Aprobado por:** Rodrigo Silva Bravo (PO)
> **Ejecutor:** mocito (Claude Code) — dueño del repositorio y único constructor
> **Fecha:** 2026-07-02 · **Versión:** 1.0
> **Dependencias:** repo `RodrigoMSB/python-sii-2026` con tag `lab-01-v1.0.0` (SPEC-002 completado)

---

## ⚠️ 0. Verificación del Arquitecto (leer PRIMERO)

**Premisas verificadas por el Arquitecto:**
- ✅ Las cifras de control del dataset (§5) fueron **computadas y validadas**
  con la lógica de negocio de este spec: 18 brutos → 15 válidos, 2 rechazos
  por deuda no numérica, 1 por código duplicado, deuda total válidos
  **$1.042.000**, por rubro C=$338.000 / G=$260.000 / T=$444.000, estados
  válidos VIGENTE=9 / VENCIDA=4 / SUSPENDIDA=2.
- ✅ Este spec es autosuficiente: **no depende de ningún artefacto externo**.
  Todo el contenido a construir está especificado aquí.
- ✅ El alcance (§4) fue cruzado contra el temario adjudicado del SII:
  cubre la segunda mitad del Módulo 1 sin invadir los Módulos 2 y 3.

**Supuestos a validar por el PO o mocito ANTES de ejecutar:**
1. El repo local en `/Users/rodrigosilva/SII/PYTHON` está en `main`, limpio,
   y sincronizado con `origin` (tag `lab-01-v1.0.0` presente).
2. El Lab 01 sigue certificado: `labs/lab-01-primer-dia/` intacto. Este spec
   NO modifica el Lab 01, con UNA excepción declarada: §9.1 (tabla de labs
   del README portada).
3. `uv`, `git` y `gh` siguen operativos en la máquina (ya verificado en
   SPEC-002; re-confirmar solo si hubo cambios de sistema).

---

## 1. Contexto y narrativa del lab

Don Arquímedes quedó contento con el triaje... y como todo jefe contento,
trae más trabajo: apareció el **archivador antiguo** con patentes que nunca
se digitalizaron. Su asistente las transcribió a la carrera y el resultado
tiene de todo: deudas escritas como texto con puntos ("38.000"), registros
"S/I" (sin información) y hasta una patente pegada dos veces.

El dolor pedagógico de este lab (estilo Meridiano: el dolor motiva la
herramienta):
- Buscar una patente en una lista de listas es lento e ilegible → nacen los
  **diccionarios** (y las **tuplas**/**sets** de paso).
- El triaje se repetirá cada semana → nacen las **funciones** de verdad.
- Los datos vienen sucios y el programa muere → nacen las **excepciones**.
- "Funciona pero no sé por qué da eso" → nace **pdb** (el interrogatorio
  policial al programa en vivo).

Misión del lab: construir `consolidar.py`, el programa que toma los
registros brutos del archivador, **rechaza los inválidos sin morirse**,
consolida los válidos en un fichero (diccionario) y genera el informe de
consolidación para Don Arquímedes.

## 2. Datos duros

| Ítem | Valor |
|------|-------|
| Carpeta del lab | `labs/lab-02-cuaderno-crece/` |
| Duración objetivo | ~2,5 horas (segunda mitad del Módulo 1; presupuesto total del curso: 7 labs / 20 hrs) |
| Python | 3.13 pineado con `uv` (idéntico a Lab 01) |
| Dependencias | NINGUNA — 100 % stdlib |
| Tag al certificar | `lab-02-v1.0.0` |

## 3. Estructura del lab (anatomía estándar del curso)

Idéntica al Lab 01, con los nombres propios de este lab:

```
labs/lab-02-cuaderno-crece/
├── README.md
├── pyproject.toml               ← requires-python "==3.13.*", deps []
├── .python-version              ← 3.13
├── bin/
│   ├── 00-preparar.sh / 00-preparar.ps1
│   ├── lib_comunes.py           ← MISMO contrato que Lab 01 (puede copiarse)
│   ├── verificar_entorno.py
│   ├── verificar.py
│   └── recuperar_lab.py
├── datos/
│   ├── cuaderno.py              ← COPIA EXACTA del dataset del Lab 01 (§5 SPEC-002)
│   └── archivador.py            ← dataset nuevo (§5, VERBATIM)
├── guia/
│   ├── 01-contexto.md
│   ├── 02-diccionarios.md
│   ├── 03-funciones.md
│   ├── 04-excepciones.md
│   └── 05-consolidacion.md
├── plantillas/
│   ├── consolidar.py            ← con TODO 1..6
│   └── RESPUESTAS.md
├── soluciones/
│   ├── consolidar.py
│   └── desafio-top-deudores.md
└── docs/troubleshooting.md
```

## 4. Alcance pedagógico (sintonía con el temario SII — Módulo 1, 2ª mitad)

**Cubre:** tuplas, sets y diccionarios (características, diferencias, casos
de uso) · estructuras de control completas: `while`, `range()`, `break`,
`continue` · comprensiones de listas (sintaxis y aplicación práctica) ·
funciones: parámetros, valores por defecto, `*args`/`**kwargs`, retorno,
lambdas y funciones como objetos de primera clase, scope local/global ·
manejo de excepciones: `try/except/else/finally`, tipos comunes, excepciones
personalizadas, `raise` · técnicas de depuración: print debugging, `pdb` vía
`breakpoint()`.

**Fuera de alcance (labs 03+):** NumPy, pandas, archivos CSV/Excel/JSON,
bases de datos. (La lectura de archivos externos NO entra aquí: el
archivador llega como módulo Python, igual que el cuaderno del Lab 01.)

## 5. Dataset nuevo — `datos/archivador.py` (VERBATIM, es contrato)

Docstring que cuente la historia (archivador antiguo, transcripción
apurada) y documente el formato: lista de **diccionarios** con claves
`"codigo"`, `"nombre"`, `"estado"`, `"deuda"` — donde `deuda` es **str**
(así llegó del archivador: con puntos de miles, o "S/I", o texto libre).
Registros EXACTOS, en este orden:

```python
REGISTROS_BRUTOS = [
    {"codigo": "PS-1025-G", "nombre": "Rotisería El Ágora", "estado": "VIGENTE", "deuda": "0"},
    {"codigo": "PS-1026-C", "nombre": "Imprenta El Estilete", "estado": "VIGENTE", "deuda": "38.000"},
    {"codigo": "PS-1027-T", "nombre": "Paseos Corriente Austral", "estado": "VENCIDA", "deuda": "154.000"},
    {"codigo": "PS-1028-G", "nombre": "Fuente de Soda La Espuma", "estado": "VIGENTE", "deuda": "0"},
    {"codigo": "PS-1029-C", "nombre": "Relojería El Péndulo", "estado": "VENCIDA", "deuda": "S/I"},
    {"codigo": "PS-1030-T", "nombre": "Miradores del Istmo", "estado": "SUSPENDIDA", "deuda": "290.000"},
    {"codigo": "PS-1031-G", "nombre": "Pastelería Pi", "estado": "VIGENTE", "deuda": "27.500"},
    {"codigo": "PS-1032-C", "nombre": "Cordelería El Nudo Firme", "estado": "VENCIDA", "deuda": "83.000"},
    {"codigo": "PS-1026-C", "nombre": "Imprenta El Estilete", "estado": "VIGENTE", "deuda": "38.000"},
    {"codigo": "PS-1033-T", "nombre": "Velero Escuela Borde Costero", "estado": "VIGENTE", "deuda": "0"},
    {"codigo": "PS-1034-G", "nombre": "Cevichería El Teorema", "estado": "VENCIDA", "deuda": "121.000"},
    {"codigo": "PS-1035-C", "nombre": "Vidriería Cristal del Sur", "estado": "VIGENTE", "deuda": "0"},
    {"codigo": "PS-1036-T", "nombre": "Termas Secas del Cerro", "estado": "VENCIDA", "deuda": "no informado"},
    {"codigo": "PS-1037-G", "nombre": "Amasandería La Palanca Dos", "estado": "VIGENTE", "deuda": "64.000"},
    {"codigo": "PS-1038-C", "nombre": "Tornería El Eje", "estado": "SUSPENDIDA", "deuda": "205.000"},
    {"codigo": "PS-1039-T", "nombre": "Guías Ruta del Faro", "estado": "VIGENTE", "deuda": "0"},
    {"codigo": "PS-1040-G", "nombre": "Jugos El Cilindro", "estado": "VENCIDA", "deuda": "47.500"},
    {"codigo": "PS-1041-C", "nombre": "Bodegaje El Silo", "estado": "VIGENTE", "deuda": "12.000"},
]
```

**Cifras de control (verificadas por el Arquitecto, §0):**
- Registros brutos: **18** · Válidos: **15** · Rechazados por deuda no
  numérica: **2** (PS-1029-C "S/I", PS-1036-T "no informado") · Rechazados
  por código duplicado: **1** (segunda aparición de PS-1026-C).
- Regla de duplicados: **gana el primero visto**; el duplicado se rechaza.
- Deuda total de válidos: **$1.042.000** CLP.
- Deuda por rubro (letra final del código): **C=$338.000 · G=$260.000 ·
  T=$444.000**.
- Estados entre válidos: VIGENTE=9 · VENCIDA=4 · SUSPENDIDA=2.
- Top deudor válido: Miradores del Istmo, $290.000 (para el desafío).

Además: `datos/cuaderno.py` se copia EXACTO del Lab 01 (mismo VERBATIM del
SPEC-002 §5) — la narrativa lo usa como "lo ya digitalizado" en la Guía 2.

## 6. Contratos de código

Rigen **C1–C6 del SPEC-002 §6** sin cambios. Se agrega:
- **C7.** La solución y la plantilla usan SOLO lo enseñado hasta la guía
  correspondiente (p. ej., nada de comprensiones antes de presentarlas en
  la Guía 5; ninguna feature fuera del alcance §4).
- **C8.** `breakpoint()` puede aparecer en las guías como ejercicio, pero
  JAMÁS en `soluciones/`, `plantillas/` ni `bin/` (un alumno que copia no
  debe quedar atrapado en un debugger sin querer).

## 7. El programa del lab — `consolidar.py`

### 7.1 Solución (`soluciones/consolidar.py`)

Nivel: principiante que YA pasó el Lab 01. Estructura obligatoria:

- Import: `from datos.archivador import REGISTROS_BRUTOS`.
- Excepción personalizada:
  `class RegistroInvalido(ValueError):` con docstring (se lanza cuando un
  registro bruto no puede convertirse en ficha).
- `normalizar_deuda(texto) -> int` — quita puntos de miles
  (`texto.replace(".", "")`) e intenta `int(...)`; si falla, **relanza**
  como `RegistroInvalido` con mensaje que incluya el texto original
  (patrón: `raise RegistroInvalido(f"...") from None` o equivalente simple;
  mantener legible para principiantes).
- `crear_ficha(registro) -> dict` — retorna dict con claves `codigo`,
  `nombre`, `estado`, `deuda` (int normalizado) y `rubro` (letra final del
  código). Usa `normalizar_deuda`.
- `consolidar(registros) -> tuple[dict, list]` — recorre los brutos con
  `for`; usa `try/except RegistroInvalido` para acumular rechazos (lista de
  tuplas `(codigo, motivo)`), y un dict `fichero = {codigo: ficha}` donde el
  duplicado se detecta con `codigo in fichero` (gana el primero; el
  duplicado va a rechazos con motivo "código duplicado"). Retorna
  `(fichero, rechazos)`.
- `deuda_por_rubro(fichero) -> dict` — dict `{rubro: total}` acumulando con
  `.get(rubro, 0)`.
- `construir_informe(fichero, rechazos) -> str` — f-strings, formato:
  título `INFORME DE CONSOLIDACIÓN — Dirección de Rentas de Puerto Siracusa`,
  línea `=` × 62, renglones: `Registros del archivador : 18` (usar
  `len(fichero) + len(rechazos)`), `Fichas consolidadas      : {n}`,
  `Registros rechazados     : {n}`, `Deuda total consolidada  : ${t:,} CLP`
  (¡con separador de miles!), sección `Deuda por rubro:` con líneas
  `  {rubro}: ${total:,} CLP` en orden C, G, T; sección
  `Rechazados (código → motivo):` con líneas `  - {codigo}: {motivo}`.
- `main()` — imprime informe y lo escribe en
  `salidas/informe_consolidacion.txt` (UTF-8, pathlib, mkdir exist_ok).
- Guard `if __name__ == "__main__":`.

Nota de formato: el informe usa `{t:,}` → `1,042,000`; el verificador debe
buscar la cifra formateada con coma (o normalizar), NO el número pelado.

### 7.2 Plantilla (`plantillas/consolidar.py`)

Mismo esqueleto con **TODO 1..6** y pistas concretas:
- TODO 1 → cuerpo de `normalizar_deuda` (pista: `.replace(".", "")`,
  `int()`, y el `try/except ValueError` que relanza `RegistroInvalido`).
- TODO 2 → cuerpo de `crear_ficha` (pista: el rubro es `codigo[-1]`, guiño
  al Lab 01).
- TODO 3 → detección de duplicado en `consolidar` (pista: `in` sobre dicts
  pregunta por las CLAVES).
- TODO 4 → el `try/except RegistroInvalido` dentro del bucle de
  `consolidar` (pista: el programa NO debe morir por un registro malo).
- TODO 5 → cuerpo de `deuda_por_rubro` (pista: `.get(clave, 0)`).
- TODO 6 → renglones del resumen en `construir_informe` (pista: f-string
  con `:,`).
El archivo debe correr con los TODO pendientes (funciones retornando
valores vacíos/neutros) sin lanzar excepciones.

## 8. Especificación de guías (redacción original de mocito)

Convenciones idénticas al Lab 01 (bloques comando/salida esperada, cápsulas
🔮/💥/🤖, checkpoint final por guía). Contenidos mínimos:

- **01-contexto.md** — narrativa del archivador; preparar entorno (mismo
  flujo Lab 01, salida esperada); **tuplas** (inmutables — analogía
  obligatoria: el folio timbrado del archivo municipal: una vez timbrado,
  no se corrige, se emite otro) y **sets** (unicidad — motivar con "¿cuántos
  códigos ÚNICOS hay en el archivador?": `len({r["codigo"] for r in ...})`
  se muestra como magia y se promete explicar la comprensión en la Guía 5;
  alternativa sin comprensión con bucle). 🔮 predicción: `len(set([...]))`
  con lista con repetidos.
- **02-diccionarios.md** — el dolor de buscar en lista de listas (mostrar
  el bucle de búsqueda sobre `datos/cuaderno.py` del Lab 01) → dict como
  fichero con pestañas; crear, leer (`[]` vs `.get()` — 💥 KeyError a
  propósito y su lectura), escribir, `in` sobre claves, `keys/values/items`,
  iterar con `for clave, valor in d.items()`. Construcción manual de una
  ficha `{"codigo": ..., ...}`. 🤖 prompt sugerido: cuándo lista vs dict.
- **03-funciones.md** — del script al taller de herramientas: `def`,
  parámetros y retorno; valores por defecto (ej.: `formatear_pesos(monto,
  simbolo="$")`); `*args` (sumar deudas variables) y `**kwargs` (ficha
  flexible) en dosis breve; lambdas + `sorted(fichas, key=lambda ...)` para
  ordenar por deuda; funciones como objetos (pasar una función a otra);
  scope local vs global con 💥 UnboundLocalError o el clásico "modifiqué la
  global sin `global`" explicado sin dramatismo. Checkpoint.
- **04-excepciones.md** — la transcripción sucia: `int("S/I")` → 💥
  ValueError leído línea a línea; `try/except` mínimo; `else` y `finally`
  (analogía obligatoria: el protocolo de la caja municipal — `else` es "si
  el trámite salió bien, timbra", `finally` es "pase lo que pase, cierra la
  caja"); jerarquía breve (ValueError, KeyError, TypeError ya conocidos);
  crear `RegistroInvalido(ValueError)` y `raise`; por qué capturar
  específico y no `except:` pelado. Nota para Pregunta del interrogatorio.
- **05-consolidacion.md** — `while` + `break`/`continue` en 10 líneas
  (buscar la primera patente con deuda > 200.000 y parar) y `range()`;
  **comprensiones de listas** presentadas como "el for de una línea"
  (reescribir 2 bucles del lab; regla de estilo: si no cabe legible en una
  línea, usa for); bifurcación de rutas 🛠️/🔎 con comandos cp/Copy-Item;
  construir/ejecutar `consolidar.py` con salida esperada (cifras de control
  §5); **sesión guiada de pdb**: insertar `breakpoint()` dentro del bucle
  de `consolidar`, ejecutar, y recorrer con `n`, `p registro`, `c`, `q`
  observando el registro "S/I" en el momento exacto del rechazo (tabla de
  comandos mínimos incluida; recordar quitar el breakpoint — C8); copia y
  respuesta del interrogatorio; verificación final; **desafío extra**: top
  3 deudores del fichero consolidado usando `sorted` + lambda + slicing
  (solución en `soluciones/desafio-top-deudores.md`: Miradores del Istmo
  $290.000, Tornería El Eje $205.000, Paseos Corriente Austral $154.000).
  Checkpoint final + teaser Lab 03 (los números del puerto: NumPy).

## 9. Interrogatorio — `plantillas/RESPUESTAS.md`

Mismo mecanismo del Lab 01 (marcador EXACTO `(escribe aquí tu respuesta)`;
**cuidado H-02**: el encabezado NO debe contener el marcador literal — debe
describirlo sin reproducirlo). Las 5 preguntas:

1. **El KeyError de la Guía 2:** pegar la última línea del error visto en
   SU terminal al pedir una clave inexistente con `[]`, y explicar qué
   habría devuelto `.get()` en el mismo caso.
2. **Duplicados:** según SU informe, ¿qué código fue rechazado por
   duplicado y por qué quedó la PRIMERA aparición y no la segunda? (debe
   citar la línea de `consolidar` que lo decide).
3. **Los números de SU consolidación:** fichas consolidadas, rechazados y
   deuda total según SU `salidas/informe_consolidacion.txt`; y ¿la deuda
   total incluye a las patentes SUSPENDIDAS? Justificar mirando el código.
4. **La sesión pdb:** ¿en qué registro del archivador se detuvo cuando el
   programa entró al `except` (código y contenido de `deuda`)? ¿Qué comando
   de pdb usó para inspeccionarlo?
5. **Modifica y explica (Explorador obligatorio / Artesano opcional):**
   cambiar la regla de duplicados para que gane el ÚLTIMO visto (pista:
   asignar sin preguntar `in`), re-ejecutar, explicar qué cambió en el
   informe y por qué en términos de negocio; luego revertir.

## 9.1 Cambio en archivo EXISTENTE (única excepción al aislamiento)

`README.md` de la portada del repo: actualizar la tabla de labs → Lab 02
"El cuaderno crece" pasa a ✅ Disponible. Ningún otro archivo del Lab 01 se
toca.

## 10. Verificadores

### 10.1 `bin/verificar_entorno.py`, preparadores, `lib_comunes.py`, `recuperar_lab.py`
Mismos contratos del Lab 01 (SPEC-002 §8.2–8.4, §8.6), adaptando nombres
(`consolidar.py`, `informe_consolidacion.txt`). El recuperador copia la
solución, regenera salidas, y respeta/copia el interrogatorio SIN responder.

### 10.2 `bin/verificar.py` — checks (en orden)
Implementación de referencia propia + **archivador sorpresa**: generador
aleatorio (`random.Random()` sin semilla) de 8–12 registros brutos estilo
§5 que DEBE incluir siempre: al menos 1 deuda no numérica (sortear de
["S/I", "pendiente", "sin dato"]), al menos 1 código duplicado, y deudas
con puntos de miles. Checks:

1. `consolidar.py` en la raíz del lab (pista → Guía 5).
2. Importa sin excepciones (manejo idéntico Lab 01; además: si el import se
   cuelga >10 s, sospechar `breakpoint()` olvidado — reportar con pista C8).
3. Existen y son callables: `normalizar_deuda`, `crear_ficha`, `consolidar`,
   `deuda_por_rubro`, y existe la clase `RegistroInvalido` (subclase de
   ValueError).
4. `normalizar_deuda("154.000") == 154000` y `normalizar_deuda("0") == 0`.
5. `normalizar_deuda("S/I")` **lanza RegistroInvalido** (y NO un ValueError
   genérico ni otro tipo) — pista: relanzar dentro del except.
6. `consolidar` con el **archivador oficial**: fichero con 15 fichas,
   3 rechazos, y el fichero NO contiene ficha del duplicado con datos de la
   segunda aparición (gana el primero).
7. `deuda_por_rubro` oficial == {"C": 338000, "G": 260000, "T": 444000}.
8. `consolidar` + `deuda_por_rubro` con el **archivador sorpresa** ==
   referencia (mensajes con valor obtenido vs esperado).
9. `salidas/informe_consolidacion.txt` existe y contiene la deuda total
   correcta EN FORMATO `1,042,000` (o normalizando separadores; documentar
   la decisión en el código del verificador).
10. `RESPUESTAS.md` sin marcadores pendientes (contar y reportar).

Cierre en verde con mensaje de Don Arquímedes + teaser del Lab 03.

## 11. Guion de pruebas — "mocito juega a ser alumno" 🎭

Desde clon limpio en directorio temporal, en orden, registrando evidencia:

- **E01 — Flujo feliz Explorador:** preparar → copiar solución → ejecutar →
  informe con `Fichas consolidadas      : 15`, `Registros rechazados     : 3`
  y `$1,042,000` → verificador N-1/N con único error de interrogatorio →
  responder → **N/N exit 0**.
- **E02 — Artesano a medio camino:** plantilla sin tocar → verificador
  reporta con pistas útiles, exit 1 → completar SOLO TODO 1 a mano →
  checks de `normalizar_deuda` pasan, el resto sigue fallando.
- **E03 — Tramposo:** hardcodear los retornos con las cifras oficiales →
  verificador 3 veces → el archivador sorpresa lo caza las 3, exit 1.
- **E04 — Perdido:** `cp soluciones/consolidar.py guia/ && cd guia &&
  uv run python consolidar.py` → `ModuleNotFoundError: No module named
  'datos'` documentado en troubleshooting con cura verificada; limpiar
  (`rm guia/consolidar.py`).
- **E05 — Rompe cosas:** borrar el informe → error específico + cura →
  verde · `SyntaxError` (quitar un `:`) → `[ERROR]` de carga elegante ·
  **NUEVO:** dejar un `breakpoint()` en `consolidar.py` y correr el
  verificador → NO debe quedar colgado indefinidamente; debe reportar
  según check 2/pista C8.
- **E06 — Rezagado:** recuperador → código+informe reconstruidos,
  interrogatorio pendiente → verificador N-1/N.
- **E07 — Idempotencia:** preparador ×3 sin errores.
- **E08 — Higiene:** lab sucio tras E01–E07 → `git status` limpio
  (validar que el .gitignore cubre `labs/*/consolidar.py` — si el patrón
  actual solo cubre `triaje.py`, AMPLIARLO en este spec es parte del
  trabajo: usar patrón por lab o lista explícita; documentar decisión).
- **E09 — Regresión Lab 01:** ejecutar el verificador del Lab 01 sobre un
  flujo feliz rápido (recuperador + respuestas dummy) → sigue 12/12. El
  Lab 02 no puede romper al Lab 01.

## 12. Flujo Git y certificación

1. Rama de trabajo opcional; merge/commits directos a `main` permitidos
   (repo unipersonal), commits convencionales en español:
   `feat: Lab 02 — El cuaderno crece` · `docs: spec SPEC-003` ·
   `test: certificación del Lab 02 como alumno` · fixes según hallazgos.
2. Reporte `labs/lab-02-cuaderno-crece/docs/certificacion-lab-02.md`
   (formato del Lab 01: tabla E01–E09, evidencia breve, Hallazgos,
   veredicto).
3. Con **CERTIFICADO** limpio: tag anotado `lab-02-v1.0.0` + push. Si hay
   observación abierta → detener y consultar al Arquitecto (como en H-01).

## 13. Protocolo ante problemas

Idéntico a SPEC-002 §13: ambigüedad → consultar; entorno propio → resolver
y anotar; prohibido cambiar contratos, cifras de control, nombres, o
auto-responder interrogatorios.

## 14. Definición de terminado (DoD)

- [ ] Lab 02 construido conforme §3–§10; `uv.lock` versionado.
- [ ] Portada del repo actualizada (§9.1) y `.gitignore` ampliado si E08 lo
      exigió.
- [ ] E01–E09 ejecutados; certificación **CERTIFICADO**.
- [ ] Commits convencionales + tag `lab-02-v1.0.0` pusheados.
- [ ] Hallazgos reportados (aunque sea "sin hallazgos").

---

*Firmado: El Arquitecto de Puerto Siracusa.*
*"El cuaderno creció; que crezca también el analista."* 🏛️📐
