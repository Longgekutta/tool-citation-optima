<#
.SYNOPSIS
    tool-citation-optima 5大通用操作动词脚本 (PowerShell)
#>
param (
    [Parameter(Position = 0)]
    [ValidateSet("setup", "run", "test", "health", "clean")]
    [string]$Verb = "health"
)

$ErrorActionPreference = "Stop"

switch ($Verb) {
    "setup"  { Write-Host "⚙️ [Setup] 环境检查..." -ForegroundColor Cyan; python -c "import sys; print('Python:', sys.version)"; Write-Host "✅ 就绪" -ForegroundColor Green }
    "run"    { Write-Host "🚀 [Run] 核心执行..." -ForegroundColor Cyan; python main.py run }
    "test"   { Write-Host "🧪 [Test] 运行单元测试..." -ForegroundColor Cyan; python -m unittest discover tests }
    "health" { Write-Host "🩺 [Health] 探活..." -ForegroundColor Cyan; python main.py health }
    "clean"  { Write-Host "🧹 [Clean] 清理缓存..." -ForegroundColor Cyan; Get-ChildItem -Path . -Include "__pycache__", "*.pyc" -Recurse -Force | Remove-Item -Recurse -Force; Write-Host "✅ 完成" -ForegroundColor Green }
}
