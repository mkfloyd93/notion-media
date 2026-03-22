param(
    [string]$PytestArgs = ""
)

Write-Host "Running pytest..."
python -m pytest $PytestArgs
