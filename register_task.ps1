# Register Windows Scheduled Task for Daily Kalvium WI Google Form Bot
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }

$pythonExe = (Get-Command python).Source
$pythonwExe = Join-Path (Split-Path $pythonExe) "pythonw.exe"
if (-not (Test-Path $pythonwExe)) {
    $pythonwExe = $pythonExe
}

$taskName = "DailyKalviumWIFormBot"
$action = New-ScheduledTaskAction -Execute $pythonwExe -Argument "main.py --run-now" -WorkingDirectory $scriptDir
$trigger = New-ScheduledTaskTrigger -Daily -At "11:00 AM"

$settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -WakeToRun `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 15)

try {
    # Unregister existing task if present
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    
    # Register the task for current user
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Automatically fills the daily Kalvium WI Google Form at 11:00 AM IST."
        
    Write-Host "`n[SUCCESS] Windows Scheduled Task '$taskName' has been registered successfully!" -ForegroundColor Green
    Write-Host "Schedule: Every day at 11:00 AM IST" -ForegroundColor Cyan
    Write-Host "Runner: $pythonwExe (silent background mode)" -ForegroundColor Cyan
    Write-Host "Working Directory: $scriptDir" -ForegroundColor Cyan
    Write-Host "Missed Run Catch-up: Enabled (if laptop was asleep/off at 11:00 AM, it runs when turned on)`n" -ForegroundColor Yellow
} catch {
    Write-Host "`n[ERROR] Failed to register scheduled task: $_" -ForegroundColor Red
    exit 1
}
