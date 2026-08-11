param(
    [ValidateSet("setup", "lint", "typecheck", "test", "build", "secret-scan", "verify")]
    [string]$Task = "verify"
)

$ErrorActionPreference = "Stop"
python "$PSScriptRoot/verify.py" $Task
