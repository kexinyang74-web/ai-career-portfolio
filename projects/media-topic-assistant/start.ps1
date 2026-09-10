$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$localPython = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $localPython)) {
    python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Could not create Python environment.' }
    & $localPython -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Could not install dependencies. Check your network, then run setup again.' }
}
& $localPython -c 'import fastapi, uvicorn, httpx, dotenv'
if ($LASTEXITCODE -ne 0) {
    & $localPython -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Could not install dependencies.' }
}
if (-not (Test-Path -LiteralPath '.env')) {
    Copy-Item -LiteralPath '.env.example' -Destination '.env'
}
Write-Host 'Open http://127.0.0.1:8765 in your browser. Press Ctrl+C to stop.'
& $localPython -m uvicorn app:create_app --factory --host 127.0.0.1 --port 8765
