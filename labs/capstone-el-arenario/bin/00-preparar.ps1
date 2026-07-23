$env:PYTHONUTF8 = "1"  # Windows: Python imprime/lee UTF-8 sin morir (cp1252)
$env:UV_NATIVE_TLS = "1"  # Redes corporativas (SII): usa los certificados del sistema
# ─────────────────────────────────────────────────────────────────────────
#  Preparador del Capstone (Windows / PowerShell)
#  Uso, desde la raíz del lab:
#      powershell -ExecutionPolicy Bypass -File bin\00-preparar.ps1
#
#  Monta el taller: comprueba uv, crea/sincroniza el entorno con Python 3.13
#  y DESCARGA numpy/pandas la primera vez (requiere Internet). Idempotente.
# ─────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"

try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$DirScript = Split-Path -Parent $MyInvocation.MyCommand.Path
$RaizLab = Split-Path -Parent $DirScript
Set-Location $RaizLab

Write-Host "Preparando el Capstone - El Arenario" -ForegroundColor Cyan
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

Write-Host "[INFO] Descargando las bibliotecas del lab (solo la primera vez, requiere Internet)..." -ForegroundColor Cyan
Write-Host "[INFO] matplotlib es la mas pesada del curso: paciencia la 1a vez; si tienes proxy/antivirus, ten paciencia." -ForegroundColor Cyan
uv sync
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "[OK] Entorno .venv\ listo con numpy y pandas." -ForegroundColor Green
Write-Host ""

Write-Host "[INFO] Verificando el entorno..." -ForegroundColor Cyan
uv run python bin/verificar_entorno.py
exit $LASTEXITCODE
