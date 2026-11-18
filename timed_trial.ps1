<#
Timed fresh-clone trial for criterion 2 (revised): criteria.md.

    powershell -ExecutionPolicy Bypass -File .\timed_trial.ps1 -Trial 1

Does the RUNNING.md steps on a fresh clone in a NEW folder with a NEW venv, and
times them. The one human step is pasting your API key: the script stops and
asks, and that wait is inside the timer. Your key is never printed.

Pass for a trial: setup (clone, venv, install, key, test.py) within 300 s AND
at least 4 of 5 runs print a "Fit card:" line. The result is appended to
results/criterion2_trials.md.

What this does NOT test: that a reader can follow the written instructions. It
runs the RUNNING.md commands for you, so it shows the commands work from a clean
clone, not that the text is clear.
#>
param(
    [int]$Trial = 1,
    [string]$Repo = "https://github.com/KiranmaiMrudulaV/ai201-project2-fitfindr-starter-v2026.git",
    [string]$Query = 'vintage graphic tee under $30',
    [int]$SetupLimitSeconds = 300,
    [int]$MinFitCards = 4
)

$ErrorActionPreference = "Continue"
$resultsFile = Join-Path $PSScriptRoot "results\criterion2_trials.md"
$root = Join-Path $env:TEMP "fitfindr_trial$Trial"
if (Test-Path $root) { Remove-Item -Recurse -Force $root }
New-Item -ItemType Directory -Path $root | Out-Null
Set-Location $root

$failed = $null
function Fail($step) { if (-not $script:failed) { $script:failed = $step; Write-Host "FAILED at: $step" -ForegroundColor Red } }

Write-Host "Trial $Trial in $root. The timer starts now." -ForegroundColor Cyan
$watch = [System.Diagnostics.Stopwatch]::StartNew()
$marks = [ordered]@{}

git clone -q $Repo
if ($LASTEXITCODE -ne 0) { Fail "git clone" }
$marks["clone"] = [int]$watch.Elapsed.TotalSeconds

Set-Location (Join-Path $root "ai201-project2-fitfindr-starter-v2026")
$py = Join-Path (Get-Location) ".venv\Scripts\python.exe"

py -3.12 -m venv .venv
if ($LASTEXITCODE -ne 0) { Fail "py -3.12 -m venv .venv" }
$marks["venv"] = [int]$watch.Elapsed.TotalSeconds

& $py -m pip install -q -r requirements.txt 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Fail "pip install -r requirements.txt" }
$marks["pip install"] = [int]$watch.Elapsed.TotalSeconds

Copy-Item .env.example .env

# The human step. The wait is inside the timer.
$secure = Read-Host "Paste your GEMINI_API_KEY now (hidden), then press Enter" -AsSecureString
$key = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure))
(Get-Content .env) -replace '^GEMINI_API_KEY=.*$', "GEMINI_API_KEY=$key" | Set-Content .env -Encoding utf8
$key = $null
$marks["key pasted"] = [int]$watch.Elapsed.TotalSeconds

$testOut = & $py test.py 2>&1 | Out-String
if ($LASTEXITCODE -ne 0 -or $testOut -notmatch "You're set") { Fail "python test.py" }
$setup = [int]$watch.Elapsed.TotalSeconds
$marks["test.py done (setup time)"] = $setup
$watch.Stop()

# Five runs. Cache off, so every fit card is a real model answer.
$env:AI201_CACHE = "0"
$fit = 0
$runTimes = @()
for ($i = 1; $i -le 5; $i++) {
    $t = [System.Diagnostics.Stopwatch]::StartNew()
    $out = & $py app.py ask $Query 2>&1 | Out-String
    $t.Stop()
    $got = $out -match "Fit card:"
    if ($got) { $fit++ }
    $runTimes += [math]::Round($t.Elapsed.TotalSeconds, 1)
    Write-Host ("  run {0}: {1} ({2:N1}s)" -f $i, $(if ($got) { "fit card" } else { "NO fit card" }), $t.Elapsed.TotalSeconds)
}

$setupOk = ($setup -le $SetupLimitSeconds) -and (-not $failed)
$pass = $setupOk -and ($fit -ge $MinFitCards)
$verdict = if ($pass) { "PASS" } else { "FAIL" }

Write-Host ""
Write-Host "Setup time: $setup s (limit $SetupLimitSeconds s)  Fit cards: $fit of 5  =>  $verdict" -ForegroundColor $(if ($pass) { "Green" } else { "Red" })
foreach ($k in $marks.Keys) { Write-Host ("  {0,-28} {1,4} s" -f $k, $marks[$k]) }

if (-not (Test-Path $resultsFile)) {
    New-Item -ItemType Directory -Force -Path (Split-Path $resultsFile) | Out-Null
    "# Criterion 2 (revised): timed fresh-clone trials`n`n| Trial | Date | Setup time | Fit cards | Failed step | Verdict | Notes |`n|---|---|---|---|---|---|---|" | Set-Content $resultsFile -Encoding utf8
}
$steps = ($marks.Keys | ForEach-Object { "$_ $($marks[$_])s" }) -join "; "
"| $Trial | $(Get-Date -Format 'yyyy-MM-dd HH:mm') | $setup s | $fit of 5 | $(if ($failed) { $failed } else { 'none' }) | $verdict | $steps; runs $($runTimes -join ', ') s |" | Add-Content $resultsFile -Encoding utf8
Write-Host "Appended to $resultsFile"
Set-Location $PSScriptRoot
