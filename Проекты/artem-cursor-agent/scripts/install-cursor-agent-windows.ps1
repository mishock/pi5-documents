# Установка Cursor Agent CLI на Windows (ПК Артёма)
# Запуск (PowerShell от администратора не обязателен):
#   powershell -ExecutionPolicy Bypass -File install-cursor-agent-windows.ps1
# Или двойной клик после разблокировки (Unblock-File).

param(
    [string]$CredentialsDir = "$PSScriptRoot\..\credentials",
    [switch]$SkipCursorInstall
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }

Write-Step "Cursor Agent — установка для Артёма"

# 1. Cursor CLI (native Windows)
if (-not $SkipCursorInstall) {
    Write-Step "Установка Cursor CLI"
    irm 'https://cursor.com/install?win32=true' | iex
    $agentCmd = Get-Command agent -ErrorAction SilentlyContinue
    if (-not $agentCmd) {
        $localAgent = Join-Path $env:LOCALAPPDATA "cursor-agent\agent.ps1"
        if (Test-Path $localAgent) {
            $env:Path = "$(Split-Path $localAgent);$env:Path"
        }
    }
    agent --version
}

# 2. Папки
$sshDir = Join-Path $env:USERPROFILE ".ssh"
$configDir = Join-Path $env:USERPROFILE ".config"
$cursorDir = Join-Path $env:USERPROFILE ".cursor"
foreach ($d in @($sshDir, $configDir, $cursorDir)) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}

# 3. SSH ключ (из credentials рядом со скриптом)
$keySrc = Join-Path $CredentialsDir "artem_ed25519"
$keyPub = Join-Path $CredentialsDir "artem_ed25519.pub"
$keyDst = Join-Path $sshDir "artem_ed25519"
if (-not (Test-Path $keySrc)) {
    Write-Host "Файл ключа не найден: $keySrc" -ForegroundColor Red
    Write-Host "Скопируйте artem_ed25519 и artem_ed25519.pub в папку credentials" -ForegroundColor Yellow
    exit 1
}
Copy-Item $keySrc $keyDst -Force
if (Test-Path $keyPub) { Copy-Item $keyPub (Join-Path $sshDir "artem_ed25519.pub") -Force }
icacls $keyDst /inheritance:r /grant:r "$env:USERNAME:(R)" | Out-Null

# 4. SSH config — малинки через NetBird
$sshConfig = Join-Path $sshDir "config"
$meshBlock = @"

# === Малинки Шпак (Cursor Agent / мониторинг) ===
Host pi3 pi3-netbird
    HostName 100.102.186.61
    User pi
    IdentityFile ~/.ssh/artem_ed25519
    IdentitiesOnly yes
    ConnectTimeout 25
    ServerAliveInterval 15
    ServerAliveCountMax 4

Host pi5 pi5-netbird
    HostName 100.102.159.200
    User pi
    IdentityFile ~/.ssh/artem_ed25519
    IdentitiesOnly yes
    ConnectTimeout 25
    ServerAliveInterval 15
    ServerAliveCountMax 4

Host kali kali-netbird
    HostName 100.102.121.127
    User kali
    IdentityFile ~/.ssh/artem_ed25519
    IdentitiesOnly yes
    ProxyJump pi3
    ConnectTimeout 30
    ServerAliveInterval 15
    ServerAliveCountMax 4

Host pi5-wan
    HostName 91.215.61.76
    User pi
    IdentityFile ~/.ssh/artem_ed25519
    IdentitiesOnly yes
    ConnectTimeout 20
"@

$marker = "# === Малинки Шпак"
if (Test-Path $sshConfig) {
    $existing = Get-Content $sshConfig -Raw -ErrorAction SilentlyContinue
    if ($existing -match [regex]::Escape($marker)) {
        $existing = ($existing -split [regex]::Escape($marker))[0].TrimEnd()
    }
    Set-Content -Path $sshConfig -Value ($existing + $meshBlock) -Encoding UTF8
} else {
    Set-Content -Path $sshConfig -Value $meshBlock.TrimStart() -Encoding UTF8
}

# 5. Cursor API key
$apiFile = Join-Path $CredentialsDir "cursor-api-key.txt"
$envFile = Join-Path $configDir "cursor-agent.env"
if (Test-Path $apiFile) {
    $apiKey = (Get-Content $apiFile -Raw).Trim()
    Set-Content -Path $envFile -Value "CURSOR_API_KEY=`"$apiKey`"`n" -Encoding UTF8
    [System.Environment]::SetEnvironmentVariable("CURSOR_API_KEY", $apiKey, "User")
    Write-Host "API key записан в $envFile" -ForegroundColor Green
} else {
    Write-Host "cursor-api-key.txt не найден — задайте CURSOR_API_KEY вручную или agent login" -ForegroundColor Yellow
}

# 6. cli-config (composer-2.5, unrestricted)
$cliConfig = Join-Path $cursorDir "cli-config.json"
@{
    version = 1
    permissions = @{
        allow = @("Shell(*)", "Read(*)", "Write(*)", "Grep(*)", "Glob(*)")
        deny = @()
    }
    approvalMode = "unrestricted"
    selectedModel = @{ modelId = "composer-2.5"; parameters = @() }
    hasChangedDefaultModel = $true
} | ConvertTo-Json -Depth 5 | Set-Content $cliConfig -Encoding UTF8

Write-Step "Проверка"
Write-Host "1. Установите NetBird: https://netbird.io/ — тот же аккаунт, что у семьи"
Write-Host "2. После Connected: ssh pi3"
Write-Host "3. Cursor Agent: agent -p `"привет`""
Write-Host "4. PWA Джарвис (Pi5): https://91.215.61.76:8767/app/"
Write-Host "`nГотово." -ForegroundColor Green
