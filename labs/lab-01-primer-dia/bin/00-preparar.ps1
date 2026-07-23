$env:PYTHONUTF8 = "1"  # Windows: Python imprime/lee UTF-8 sin morir (cp1252)
$env:UV_NATIVE_TLS = "1"  # Redes corporativas (SII): usa los certificados del sistema
# ─────────────────────────────────────────────────────────────────────────
#  Preparador del Lab 01 (Windows / PowerShell)
#  Uso, desde la raíz del lab:
#      powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
#
#  Monta el "taller aislado": comprueba uv, crea/sincroniza el entorno virtual
#  con Python 3.13 y verifica que todo quedó en verde. Es idempotente.
# ─────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"

# Que los acentos y símbolos se vean bien en la consola.
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

# Nos paramos SIEMPRE en la raíz del lab (la carpeta que contiene a bin\).
$DirScript = Split-Path -Parent $MyInvocation.MyCommand.Path
$RaizLab = Split-Path -Parent $DirScript
Set-Location $RaizLab

Write-Host "Preparando el Lab 01 - El primer dia en Rentas" -ForegroundColor Cyan
Write-Host "Carpeta del lab: $RaizLab" -ForegroundColor Cyan
Write-Host ""

# ── 1) ¿Está uv instalado? ────────────────────────────────────────────────
$uv = Get-Command uv -ErrorAction SilentlyContinue
if (-not $uv) {
    Write-Host "[ERROR] No encuentro 'uv' en el PATH." -ForegroundColor Red
    Write-Host "       Pista: instala uv y vuelve a intentar:" -ForegroundColor Yellow
    Write-Host '         powershell -c "irm https://astral.sh/uv/install.ps1 | iex"'
    Write-Host "       Cierra y reabre PowerShell despues de instalar."
    Write-Host "       Mas ayuda en docs\setup-alumno.md y docs\troubleshooting.md."
    exit 1
}
Write-Host "[OK] uv encontrado: $($uv.Source)" -ForegroundColor Green

# ── 2) Crear / sincronizar el entorno virtual con Python 3.13 ─────────────
Write-Host "[INFO] Sincronizando el entorno (uv trae Python 3.13)..." -ForegroundColor Cyan
uv sync
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "[OK] Entorno .venv\ listo." -ForegroundColor Green
Write-Host ""

# ── 3) Verificar que el entorno quedó en verde ────────────────────────────
Write-Host "[INFO] Verificando el entorno..." -ForegroundColor Cyan
uv run python bin/verificar_entorno.py
exit $LASTEXITCODE
