param(
    [ValidateSet("setup", "lint", "typecheck", "test", "ai-fixtures", "build", "secret-scan", "verify")]
    [string]$Task = "verify"
)

$ErrorActionPreference = "Stop"
python "$PSScriptRoot/verify.py" $Task
