"""Verificador del Capstone — El Arenario.

Se ejecuta desde la raíz del capstone:

    uv run python bin/verificar.py

Mide PRODUCTOS, no la estructura del código (contrato C18): re-deriva TODO desde
las fuentes con su propia implementación de referencia y compara contra los
archivos que dejaste en salidas/. No hay dataset sorpresa: el anti-loro es la
consistencia — para pasar, tus 6 productos deben cuadrar entre sí y con las
fuentes (fabricarlos a mano coherentes cuesta más que hacer el pipeline). La
calidad del código y del informe la evalúa el relator con la rúbrica.
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

import lib_comunes as lc  # noqa: E402

try:
    import pandas as pd
except Exception as exc:  # pragma: no cover
    lc.error(f"No pude importar pandas: {exc}", "Corre el preparador.")
    sys.exit(1)

DATOS = RAIZ / "datos"
FUENTES = DATOS / "fuentes"
SALIDAS = RAIZ / "salidas"
GRAFICOS = SALIDAS / "graficos"
RUTA_BITACORA = RAIZ / "BITACORA.md"
MARCADOR = "(escribe aquí tu respuesta)"
PATRON = r"PS-\d{4}-[CGT]"
RUBRO = {"C": "Comercio", "G": "Gastronomía", "T": "Turismo"}
BINS = [-1, 0, 100_000, 300_000, 10**9]
LABELS = ["Sin deuda", "Baja", "Media", "Alta"]


# ─── Referencia (re-derivada desde las fuentes) ────────────────────────────

def _ref():
    df = pd.read_csv(DATOS / "censo_anual.csv", na_values=["", "S/I", "s/d"], keep_default_na=True)
    df = df.copy()
    df["estado"] = df["estado"].str.strip().str.upper(); df["nombre"] = df["nombre"].str.strip()
    df = df.drop_duplicates()
    df = df[df["codigo"].str.fullmatch(PATRON)].copy()
    df["deuda"] = df["deuda"].fillna(0).astype(int)
    q1, q3 = df["deuda"].quantile(.25), df["deuda"].quantile(.75); iqr = q3 - q1
    ci = set(df[(df["deuda"] < q1 - 1.5 * iqr) | (df["deuda"] > q3 + 1.5 * iqr)]["codigo"])
    z = (df["deuda"] - df["deuda"].mean()) / df["deuda"].std()
    cz = set(df[z.abs() > 3]["codigo"])
    dep = df[~df["codigo"].isin(ci & cz)].copy()
    dep["rubro"] = dep["codigo"].str[-1].map(RUBRO)
    dep["tramo"] = pd.cut(dep["deuda"], bins=BINS, labels=LABELS)

    hojas = pd.read_excel(FUENTES / "pagos_anuales.xlsx", sheet_name=None)
    pagos = pd.concat(hojas.values(), ignore_index=True)
    pagado = pagos.groupby("codigo", as_index=False)["monto"].sum().rename(columns={"monto": "pagado"})
    with open(DATOS / "multas.json", encoding="utf-8") as f:
        multas = pd.DataFrame(json.load(f))
    multa = multas.groupby("codigo", as_index=False)["monto"].sum().rename(columns={"monto": "multas"})

    t = dep.merge(pagado, on="codigo", how="left").merge(multa, on="codigo", how="left")
    t["pagado"] = t["pagado"].fillna(0).astype(int); t["multas"] = t["multas"].fillna(0).astype(int)
    t["saldo"] = t["deuda"] + t["multas"] - t["pagado"]
    return {
        "dep_filas": len(dep), "dep_deuda": int(dep["deuda"].sum()),
        "dep_codigos": set(dep["codigo"]),
        "pagado": int(t["pagado"].sum()), "multas": int(t["multas"].sum()),
        "saldo": int(t["saldo"].sum()),
        "tramos": {k: int(v) for k, v in dep["tramo"].value_counts().sort_index().items()},
        "saldo_rubro": {k: int(v) for k, v in t.groupby("rubro")["saldo"].sum().items()},
        "al_dia": int((t["saldo"] <= 0).sum()), "morosos": int((t["saldo"] > 0).sum()),
    }


def main() -> int:
    lc.titulo("Verificador del Capstone — El Arenario")
    cont = lc.Contador()
    R = _ref()

    # 1) censo_depurado.csv
    p = SALIDAS / "censo_depurado.csv"
    try:
        cd = pd.read_csv(p)
        cols_ok = list(cd.columns) == ["codigo", "nombre", "estado", "deuda"]
        ok = (cols_ok and len(cd) == R["dep_filas"] and int(cd["deuda"].sum()) == R["dep_deuda"]
              and not cd["codigo"].duplicated().any()
              and cd["codigo"].str.fullmatch(PATRON).all()
              and set(cd["codigo"]) == R["dep_codigos"])
        if ok:
            lc.ok(f"censo_depurado.csv: {len(cd)}×4, deuda ${R['dep_deuda']:,}, sin duplicados ni códigos inválidos.", cont)
        else:
            lc.error(f"censo_depurado.csv incorrecto (filas={len(cd)}, deuda={int(cd['deuda'].sum())}, "
                     f"esperado {R['dep_filas']}/{R['dep_deuda']}; ¿quitaste PS-1047-T y PS-77?).",
                     "Depura con las reglas oficiales: dedup, regex, imputar, consenso IQR∩z.", cont)
    except Exception as exc:  # noqa: BLE001
        lc.error(f"No pude leer salidas/censo_depurado.csv: {exc}", "Genera el censo depurado.", cont)

    # 2) tablero_anual csv + xlsx
    tablero = None
    cols_esp = ["codigo", "nombre", "estado", "deuda", "rubro", "tramo", "giro", "pagado", "multas", "saldo"]
    try:
        tc = pd.read_csv(SALIDAS / "tablero_anual.csv")
        tx = pd.read_excel(SALIDAS / "tablero_anual.xlsx")
        ok = (list(tc.columns) == cols_esp and len(tc) == 27 and len(tx) == 27
              and int(tc["pagado"].sum()) == R["pagado"] and int(tc["multas"].sum()) == R["multas"]
              and int(tc["saldo"].sum()) == R["saldo"])
        if ok:
            tablero = tc
            lc.ok(f"tablero_anual.csv/.xlsx: 27×10, pagado ${R['pagado']:,}, multas ${R['multas']:,}, saldo ${R['saldo']:,}.", cont)
        else:
            lc.error(f"tablero_anual incorrecto (cols={list(tc.columns)==cols_esp}, filas={len(tc)}, "
                     f"pagado={int(tc['pagado'].sum())}, saldo={int(tc['saldo'].sum())}; esperado saldo {R['saldo']}).",
                     "saldo = deuda + multas − pagado; columnas exactas; giro desde la BD.", cont)
            tablero = tc
    except Exception as exc:  # noqa: BLE001
        lc.error(f"No pude leer el tablero anual: {exc}", "Genera tablero_anual.csv y .xlsx.", cont)

    # 3-5) métricas del tablero
    if tablero is not None and "tramo" in tablero.columns:
        tramos = {k: int(v) for k, v in tablero["tramo"].value_counts().items()}
        _chk(tramos == R["tramos"], f"Tramos de deuda == {R['tramos']}.",
             f"Tramos: obtuvo {tramos}, se esperaba {R['tramos']}.", "Revisa pd.cut.", cont)
        sr = {k: int(v) for k, v in tablero.groupby("rubro")["saldo"].sum().items()}
        _chk(sr == R["saldo_rubro"], f"Saldo por rubro == {R['saldo_rubro']}.",
             f"Saldo por rubro: obtuvo {sr}, se esperaba {R['saldo_rubro']}.", "Revisa rubro y saldo.", cont)
        ad, mo = int((tablero["saldo"] <= 0).sum()), int((tablero["saldo"] > 0).sum())
        _chk(ad == R["al_dia"] and mo == R["morosos"], f"Al día {R['al_dia']} / morosos {R['morosos']}.",
             f"Al día/morosos: obtuvo {ad}/{mo}, se esperaba {R['al_dia']}/{R['morosos']}.", "saldo ≤ 0 = al día.", cont)
    else:
        for _ in range(3):
            lc.error("No evaluable: falta un tablero_anual válido con columna 'tramo'.", "Genera el tablero.", cont)

    # 6) informe
    p = SALIDAS / "informe_anual.txt"
    if p.exists():
        txt = p.read_text(encoding="utf-8"); low = txt.lower()
        faltan = [x for x in ("990,000", "31", "27", "PS-1050-C") if x not in txt]
        hallazgo = ("hallazgo" in low) and ("negativ" in low)
        if not faltan and hallazgo:
            lc.ok("informe_anual.txt: contiene $990,000, el embudo 31→27, el huérfano PS-1050-C y los hallazgos con saldos negativos.", cont)
        else:
            lc.error(f"informe_anual.txt incompleto (faltan: {faltan}; sección de hallazgos con negativos: {hallazgo}).",
                     "El informe debe incluir el embudo, el saldo, el huérfano y una sección 'Hallazgos' que explique los saldos negativos.", cont)
    else:
        lc.error("No existe salidas/informe_anual.txt.", "Genera el informe anual.", cont)

    # 7) los dos gráficos
    problemas = []
    for g in ("saldo_por_rubro.png", "tramos_de_deuda.png"):
        ruta = GRAFICOS / g
        if not ruta.exists():
            problemas.append(f"{g} ausente")
        elif ruta.stat().st_size < 5000 or ruta.read_bytes()[:4] != b"\x89PNG":
            problemas.append(f"{g} inválido")
    _chk(not problemas, "salidas/graficos/: los dos PNG (saldo_por_rubro, tramos_de_deuda) son válidos.",
         "Gráficos: " + "; ".join(problemas) + ".", "Genera ambos PNG con Agg + savefig.", cont)

    # 8) gestion.db
    p = SALIDAS / "gestion.db"
    if p.exists():
        try:
            con = sqlite3.connect(p)
            n = con.execute("SELECT COUNT(*) FROM resumen_anual").fetchone()[0]
            con.close()
            _chk(n == 3, "gestion.db: tabla resumen_anual con 3 filas (una por rubro).",
                 f"resumen_anual tiene {n} filas, se esperaban 3.", "to_sql del resumen por rubro.", cont)
        except Exception as exc:  # noqa: BLE001
            lc.error(f"gestion.db sin tabla resumen_anual legible: {exc}", "Escribe resumen_anual con to_sql.", cont)
    else:
        lc.error("No existe salidas/gestion.db.", "Exporta el resumen por rubro con to_sql.", cont)

    # 9) bitácora
    if not RUTA_BITACORA.exists():
        lc.error("No encuentro BITACORA.md en la raíz del capstone.",
                 "Cópiala desde plantillas/ y respóndela: cp plantillas/BITACORA.md BITACORA.md.", cont)
    else:
        pend = RUTA_BITACORA.read_text(encoding="utf-8").count(MARCADOR)
        if pend == 0:
            lc.ok("BITACORA.md está completa (sin respuestas pendientes).", cont)
        else:
            lc.error(f"BITACORA.md tiene {pend} respuesta(s) sin contestar.",
                     f"Reemplaza cada '{MARCADOR}' por tu defensa.", cont)

    codigo = lc.resumen(cont)
    if codigo == 0:
        print()
        lc.titulo("Don Arquímedes firma el Informe Anual")
        print(
            "Don Arquímedes lee el informe de principio a fin, se detiene en los saldos\n"
            "negativos que supiste explicar, y estampa su firma. Luego, despacio, dice:\n"
            "«Dame un punto de apoyo y moveré el mundo, escribió mi tocayo. Tú ya tienes\n"
            "el punto de apoyo: sabes contar la arena de este puerto, grano a grano.»\n"
        )
        print(
            f"{lc.CIAN}{lc.NEGRITA}Quedas declarado Analista de Datos de Puerto Siracusa. 🎓{lc.RESET}\n"
            "Seis labs, tres módulos, un puerto entero contado. Se cierra El Arenario."
        )
    return codigo


def _chk(cond, msg_ok, msg_err, pista, cont):
    if cond:
        lc.ok(msg_ok, cont)
    else:
        lc.error(msg_err, pista, cont)


if __name__ == "__main__":
    sys.exit(main())
