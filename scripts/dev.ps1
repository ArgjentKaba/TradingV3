param()

function Invoke-Format {
  Write-Host "== Black =="
  black .
  Write-Host "== isort =="
  isort .
}

function Invoke-Lint {
  Write-Host "== flake8 =="
  flake8 .
}

function Invoke-Checks {
  Write-Host "== pre-commit (all files) =="
  pre-commit run --all-files
}

function New-Feature {
  param([Parameter(Mandatory=$true)][string]$Name)
  git checkout -b $Name
}

function Push-Feature {
  $branch = git rev-parse --abbrev-ref HEAD
  git push -u origin $branch
}

function Open-PR {
  $branch = git rev-parse --abbrev-ref HEAD
  $url = "https://github.com/ArgjentKaba/TradingV3/compare/dev...$branch?quick_pull=1"
  Write-Host "PR URL: $url"
  try { Start-Process $url } catch { Write-Host "Öffne im Browser: $url" }
}

Write-Host "Geladen. Verfügbare Befehle:"
Write-Host " - Invoke-Format     (Black + isort)"
Write-Host " - Invoke-Lint       (flake8)"
Write-Host " - Invoke-Checks     (pre-commit run --all-files)"
Write-Host " - New-Feature -Name 'feat/<name>'"
Write-Host " - Push-Feature"
Write-Host " - Open-PR"
