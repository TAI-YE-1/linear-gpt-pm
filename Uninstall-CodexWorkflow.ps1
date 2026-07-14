param(
    [switch]$Apply,
    [string]$HomePath
)

$ErrorActionPreference = "Stop"
$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Get-Command python -ErrorAction SilentlyContinue
if (-not $Python) {
    $Python = Get-Command py -ErrorAction SilentlyContinue
}
if (-not $Python) {
    throw "Python 3 was not found in PATH."
}

$ArgsList = @((Join-Path $PackageRoot "uninstall.py"))
if ($Apply) { $ArgsList += "--apply" }
if ($HomePath) { $ArgsList += @("--home", $HomePath) }

& $Python.Source @ArgsList
exit $LASTEXITCODE
