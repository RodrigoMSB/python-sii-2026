# ─────────────────────────────────────────────────────────────────────────
#  Preparador del Lab 02 (Windows / PowerShell)
#  Uso, desde la raíz del lab:
#      powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
#
#  Monta el taller aislado: comprueba uv, crea/sincroniza el entorno virtual
#  con Python 3.13 y verifica que todo quedó en verde. Idempotente.
# ─────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"

try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$DirScript = Split-Path -Parent $MyInvocation.MyCommand.Path
$RaizLab = Split-Path -Parent $DirScript
Set-Location $RaizLab

Write-Host "Preparando el Lab 02 - El cuaderno crece" -ForegroundColor Cyan
Write-Host "Carpeta del lab: $RaizLab" -ForegroundColor Cyan
Write-Host ""

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

Write-Host "[INFO] Sincronizando el entorno (uv trae Python 3.13)..." -ForegroundColor Cyan
uv sync
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "[OK] Entorno .venv\ listo." -ForegroundColor Green
Write-Host ""

Write-Host "[INFO] Verificando el entorno..." -ForegroundColor Cyan
uv run python bin/verificar_entorno.py
exit $LASTEXITCODE
