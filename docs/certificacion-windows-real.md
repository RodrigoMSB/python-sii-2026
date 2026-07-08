# Certificación de Windows Real — SPEC-013

> **ESTADO: 🕓 PENDIENTE — esqueleto sin evidencia.** Este documento se rellena con la
> evidencia que el PO capture al recorrer el runbook sobre hardware Windows real
> (runbook de campo del SPEC-013). Mientras las casillas digan PENDIENTE, **el curso
> NO está certificado en Windows**. mocito vuelca aquí las capturas/transcripciones.

> ⚠️ **Dependencia de plataforma:** el modelo de entrega validado es **repo público**
> (Fase 1 = instalar Git + `git clone`, sin login ni zip). A la fecha, el repositorio
> figura **PRIVADO** — la Fase 1 no puede certificarse hasta que sea público.

## Plataformas

| # | Rol | Máquina | Estado |
|---|-----|---------|--------|
| P1 | **Primaria — el sello** (x86-64 nativo) | _(física, por conseguir)_ | 🕓 PENDIENTE |
| P2 | Secundaria — apoyo (Parallels/ARM, emulada) | _(Apple Silicon del PO)_ | 🕓 PENDIENTE |

> Solo **P1 (física x64 + PowerShell 5.1)** certifica. P2 es evidencia de apoyo, nunca sello.

## Fase 0 — Línea base (por plataforma)

| Dato | P1 (física x64) | P2 (Parallels/ARM) |
|------|-----------------|--------------------|
| `PSVersionTable.PSVersion` | _pendiente_ | _pendiente_ |
| Build de Windows | _pendiente_ | _pendiente_ |
| `PROCESSOR_ARCHITECTURE` | _pendiente (AMD64)_ | _pendiente (ARM64)_ |
| Defender / RealTime | _pendiente_ | _pendiente_ |
| ExecutionPolicy vigente | _pendiente_ | _pendiente_ |
| Cuenta admin / proxy / OneDrive | _pendiente_ | _pendiente_ |

## Matriz de resultados — Fase × Plataforma

Veredicto por celda: ✅ CUMPLE · ⚠️ OBSERVACIÓN · ❌ NO CUMPLE · 🕓 PENDIENTE.

| Fase | Qué se prueba | P1 física x64 | P2 Parallels/ARM | Evidencia |
|------|---------------|:-------------:|:----------------:|-----------|
| **F1** Salto cero (clon público) | Git + `git clone` sin login; material íntegro | 🕓 | 🕓 | _captura/transcripción_ |
| **F2** Instalar uv (piso ≥ 0.11) | `uv --version` ≥ 0.11 en consola real | 🕓 | 🕓 | _salida_ |
| **F3** Puerta `.ps1` en PS 5.1 | preparador → verde; `-Bypass`; sin admin; símbolos | 🕓 | 🕓 | _captura consola_ |
| **F4** Lab de punta a punta | verificador N/N (`$2350000` / `$2,072,500` / `$990,000`) | 🕓 | 🕓 | _salida verificador_ |
| **F4-sqlite** Re-ejecución lab-04 | 2.ª corrida sin `WinError 32` | 🕓 | 🕓 | _salida_ |
| **F5** OneDrive | preparador dentro vs fuera de OneDrive | 🕓 | 🕓 | _notas_ |
| **F5** Ruta con espacios/acentos | `.ps1` desde `…\María José\puerto\` | 🕓 | 🕓 | _notas_ |
| **F5** ExecutionPolicy Restricted | `-Bypass` arranca aun con Restricted | 🕓 | 🕓 | _notas_ |
| **F5** pwsh 7 vs 5.1 | paridad de salida | 🕓 | 🕓 | _notas_ |

## Pre-vuelo desde el Mac (ya verificado — no requiere Windows)

Estos puntos se confirmaron en el repo `@ curso-v1.1.0` antes de la corrida, para que
un valor "esperado" equivocado no dispare un NO CUMPLE falso:

- ✅ Cifras insignia correctas: Lab 01 `$2350000` (sin separadores), Lab 04 `$2,072,500`, capstone `$990,000`.
- ✅ Scripts del alumno (`triaje.py`, `fuentes.py`, `arenario.py`) presentes en `soluciones/`.
- ✅ `bin/verificar.py` y `bin/00-preparar.ps1` presentes en los 3 labs foco.
- ✅ Defensa de encoding `sys.stdout.reconfigure(...)` en `lib_comunes.py` de los 3 labs.
- ✅ Material que debe viajar (`uv.lock` + `.python-version` + `pyproject.toml`) en los 7 labs.

## Hallazgos

_(Ninguno registrado aún — la corrida no ha ocurrido. Todo desvío se anota aquí con
evidencia y se convierte en spec de corrección SPEC-014…, no se arregla sobre la marcha.)_

## Veredicto

**🕓 PENDIENTE.** No certificado. Se emitirá **CERTIFICADO WINDOWS** únicamente cuando,
en **P1 física x64 + PowerShell 5.1**, el trayecto cero→verde funcione incluyendo
lab-04 sqlite y la corrida fuera de OneDrive.
