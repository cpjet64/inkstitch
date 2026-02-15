$ErrorActionPreference = "Stop"

$repoRoot = git rev-parse --show-toplevel
Set-Location $repoRoot

git config core.hooksPath .githooks
$hooksPath = git config core.hooksPath
Write-Host "[hooks] Installed. core.hooksPath=$hooksPath"
