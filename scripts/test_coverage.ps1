param(
    [string]$PytestArgs = ""
)

Write-Host "Running pytest with coverage..."
python -m pytest --cov=. --cov-report=term-missing --cov-report=html $PytestArgs
Write-Host "HTML report: htmlcov/index.html"
