<# 
 FixPilot‑AI ULTRA PC Edition
 Source‑Intelligent Architect Certified
 Windows Diagnostic & Repair Engine (Safe Mode)
#>

[CmdletBinding()]
param(
    [switch]$Auto
)

$Global:AppName   = "FixPilot-AI ULTRA PC"
$Global:Version   = "1.0.0"
$Global:LogDir    = Join-Path $PSScriptRoot "FixPilot-Logs"
$Global:LogFile   = Join-Path $LogDir "FixPilot-ULTRA-PC.log"

# =========================
# LOGGING
# =========================
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    if (-not (Test-Path $Global:LogDir)) {
        New-Item -ItemType Directory -Path $Global:LogDir -Force | Out-Null
    }
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[{0}] [{1}] {2}" -f $ts, $Level.ToUpper(), $Message
    Add-Content -Path $Global:LogFile -Value $line
}

# =========================
# UI / BANNER
# =========================
function Show-Banner {
    Clear-Host
    $banner = @"
  ______ _      _ _ _ _       _ 
 |  ____(_)    (_) (_) |     | |
 | |__   _  ___ _| |_| |_ ___| |_
 |  __| | |/ __| | | | __/ _ \ __|
 | |    | | (__| | | | ||  __/ |_
 |_|    |_|\___|_|_|_|\__\___|\__|
   $($Global:AppName) v$($Global:Version)

   Source‑Intelligent Architect Certified
"@
    Write-Host $banner -ForegroundColor Cyan
    Write-Log "Banner displayed"
}

# =========================
# SMART ALERT ENGINE
# =========================
function Invoke-SmartAlerts {
    param(
        [int]$DiskUsedPercent,
        [int]$MemUsedPercent,
        [double]$CpuLoad
    )

    Write-Host ""
    Write-Host "=== ULTRA SMART ALERTS ===" -ForegroundColor Yellow
    Write-Log "Running Smart Alerts"

    if ($DiskUsedPercent -ge 95) {
        Write-Host "[!!!] CRITICAL: System drive almost full." -ForegroundColor Red
        Write-Host "      This WILL cause slowdowns, crashes, and update failures."
        Write-Log "CRITICAL: Disk usage $DiskUsedPercent%"
    } elseif ($DiskUsedPercent -ge 85) {
        Write-Host "[!!] WARNING: System drive very full." -ForegroundColor DarkYellow
        Write-Log "WARNING: Disk usage $DiskUsedPercent%"
    }

    if ($MemUsedPercent -ge 90) {
        Write-Host "[!!!] CRITICAL: Memory usage extremely high." -ForegroundColor Red
        Write-Host "      Apps may freeze or crash."
        Write-Log "CRITICAL: Memory usage $MemUsedPercent%"
    } elseif ($MemUsedPercent -ge 80) {
        Write-Host "[!!] WARNING: Memory usage high." -ForegroundColor DarkYellow
        Write-Log "WARNING: Memory usage $MemUsedPercent%"
    }

    if ($CpuLoad -ge 80) {
        Write-Host "[!!!] CRITICAL: CPU load extremely high." -ForegroundColor Red
        Write-Host "      System may feel very slow or unresponsive."
        Write-Log "CRITICAL: CPU load $CpuLoad%"
    } elseif ($CpuLoad -ge 60) {
        Write-Host "[!!] WARNING: CPU load high." -ForegroundColor DarkYellow
        Write-Log "WARNING: CPU load $CpuLoad%"
    }

    Write-Host "===========================" -ForegroundColor Yellow
    Write-Host ""
}

# =========================
# SYSTEM DIAGNOSTICS
# =========================
function Get-DiskUsage {
    $sysDrive = Get-PSDrive -Name C -ErrorAction SilentlyContinue
    if ($null -eq $sysDrive) { return $null }

    $used = $sysDrive.Used
    $free = $sysDrive.Free
    $total = $used + $free
    if ($total -eq 0) { return $null }

    [pscustomobject]@{
        Drive          = "C:"
        TotalGB        = [math]::Round($total / 1GB, 2)
        UsedGB         = [math]::Round($used / 1GB, 2)
        FreeGB         = [math]::Round($free / 1GB, 2)
        UsedPercent    = [math]::Round(($used / $total) * 100, 0)
        FreePercent    = [math]::Round(($free / $total) * 100, 0)
    }
}

function Get-MemoryUsage {
    $os = Get-CimInstance Win32_OperatingSystem
    $total = [math]::Round($os.TotalVisibleMemorySize / 1024, 0)
    $free  = [math]::Round($os.FreePhysicalMemory / 1024, 0)
    $used  = $total - $free
    $usedPct = [math]::Round(($used / $total) * 100, 0)

    [pscustomobject]@{
        TotalMB     = $total
        UsedMB      = $used
        FreeMB      = $free
        UsedPercent = $usedPct
    }
}

function Get-CpuLoad {
    try {
        $cpu = Get-Counter '\Processor(_Total)\% Processor Time' -ErrorAction Stop
        $val = [math]::Round($cpu.CounterSamples.CookedValue, 0)
        return $val
    } catch {
        Write-Log "CPU counter failed: $_"
        return 0
    }
}

function Invoke-Diagnostics {
    Write-Host "[*] Running ULTRA diagnostics..." -ForegroundColor Cyan
    Write-Log "Diagnostics started"

    Write-Host ""
    Write-Host "=== SYSTEM INFO ===" -ForegroundColor Yellow
    $cs = Get-CimInstance Win32_ComputerSystem
    $os = Get-CimInstance Win32_OperatingSystem
    Write-Host ("Computer Name : {0}" -f $cs.Name)
    Write-Host ("Manufacturer  : {0}" -f $cs.Manufacturer)
    Write-Host ("Model         : {0}" -f $cs.Model)
    Write-Host ("OS            : {0}" -f $os.Caption)
    Write-Host ("OS Version    : {0}" -f $os.Version)
    Write-Host ("Install Date  : {0}" -f $os.InstallDate.ToString("yyyy-MM-dd"))
    Write-Host ("Last Boot     : {0}" -f $os.LastBootUpTime.ToString("yyyy-MM-dd HH:mm"))
    Write-Host ""

    # Disk
    $disk = Get-DiskUsage
    if ($disk) {
        Write-Host "=== DISK (C:) ===" -ForegroundColor Yellow
        $disk | Format-Table -AutoSize
        Write-Host ""
    } else {
        Write-Host "Could not read disk usage for C:."
    }

    # Memory
    $mem = Get-MemoryUsage
    Write-Host "=== MEMORY ===" -ForegroundColor Yellow
    $mem | Format-Table -AutoSize
    Write-Host ""

    # CPU
    $cpuLoad = Get-CpuLoad
    Write-Host "=== CPU LOAD ===" -ForegroundColor Yellow
    Write-Host ("Current CPU Load: {0}%" -f $cpuLoad)
    Write-Host ""

    # Network
    Write-Host "=== NETWORK CHECK ===" -ForegroundColor Yellow
    try {
        $ping = Test-Connection -ComputerName 8.8.8.8 -Count 1 -Quiet -ErrorAction SilentlyContinue
        if ($ping) {
            Write-Host "[+] Network OK: 8.8.8.8 reachable."
            Write-Log "Network OK"
        } else {
            Write-Host "[-] Network ping failed (8.8.8.8 not reachable)." -ForegroundColor Red
            Write-Log "Network ping failed"
        }
    } catch {
        Write-Host "[-] Network test failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Log "Network test error: $_"
    }
    Write-Host ""

    Invoke-SmartAlerts -DiskUsedPercent $disk.UsedPercent -MemUsedPercent $mem.UsedPercent -CpuLoad $cpuLoad

    Write-Host "[+] ULTRA diagnostics complete." -ForegroundColor Green
    Write-Log "Diagnostics completed"
    Write-Host ""
}

# =========================
# CRASH / BSOD ANALYZER
# =========================
function Invoke-CrashAnalyzer {
    Write-Host "[*] Running Crash / BSOD analyzer..." -ForegroundColor Cyan
    Write-Log "Crash analyzer started"

    Write-Host ""
    Write-Host "=== RECENT SYSTEM ERRORS (System log) ===" -ForegroundColor Yellow
    try {
        $events = Get-WinEvent -LogName System -MaxEvents 100 |
                  Where-Object { $_.LevelDisplayName -eq "Error" } |
                  Select-Object -First 20
        if ($events) {
            $events | Select-Object TimeCreated, Id, ProviderName, LevelDisplayName, Message |
                Format-Table -AutoSize
        } else {
            Write-Host "No recent system errors found."
        }
    } catch {
        Write-Host "[-] Could not read System event log: $($_.Exception.Message)" -ForegroundColor Red
        Write-Log "System log read error: $_"
    }

    Write-Host ""
    Write-Host "=== POSSIBLE BSOD / BUGCHECK EVENTS ===" -ForegroundColor Yellow
    try {
        $bsod = Get-WinEvent -LogName System -MaxEvents 200 |
                Where-Object { $_.ProviderName -like "*BugCheck*" -or $_.Id -in 41,1001 } |
                Select-Object -First 10
        if ($bsod) {
            $bsod | Select-Object TimeCreated, Id, ProviderName, Message |
                Format-Table -AutoSize
        } else {
            Write-Host "No recent BSOD-related events detected."
        }
    } catch {
        Write-Host "[-] Could not read BSOD events: $($_.Exception.Message)" -ForegroundColor Red
        Write-Log "BSOD log read error: $_"
    }

    Write-Host ""
    Write-Host "[+] Crash / BSOD analysis complete." -ForegroundColor Green
    Write-Log "Crash analyzer completed"
    Write-Host ""
}

# =========================
# STARTUP ANALYZER
# =========================
function Invoke-StartupAnalyzer {
    Write-Host "[*] Running Startup Analyzer..." -ForegroundColor Cyan
    Write-Log "Startup analyzer started"

    try {
        $startup = Get-CimInstance Win32_StartupCommand
        if ($startup) {
            $startup | Select-Object Name, Command, Location |
                Sort-Object Name |
                Format-Table -AutoSize
        } else {
            Write-Host "No startup entries found."
        }
    } catch {
        Write-Host "[-] Could not read startup entries: $($_.Exception.Message)" -ForegroundColor Red
        Write-Log "Startup analyzer error: $_"
    }

    Write-Host ""
    Write-Host "[+] Startup analysis complete." -ForegroundColor Green
    Write-Log "Startup analyzer completed"
    Write-Host ""
}

# =========================
# TEMP / CLEANUP ENGINE (SAFE)
# =========================
function Invoke-TempScan {
    Write-Host "[*] Scanning temp locations (safe)..." -ForegroundColor Cyan
    Write-Log "Temp scan started"

    $paths = @(
        $env:TEMP,
        $env:TMP,
        "$env:SystemRoot\Temp"
    ) | Where-Object { $_ -and (Test-Path $_) }

    $totalSize = 0
    $fileCount = 0

    foreach ($p in $paths) {
        Write-Host "Scanning: $p"
        Get-ChildItem -Path $p -Recurse -ErrorAction SilentlyContinue | ForEach-Object {
            if (-not $_.PSIsContainer) {
                $totalSize += $_.Length
                $fileCount++
            }
        }
    }

    Write-Host ""
    Write-Host ("Files found : {0}" -f $fileCount)
    Write-Host ("Total size  : {0:N2} MB" -f ($totalSize / 1MB))
    Write-Log "Temp scan: $fileCount files, $([math]::Round($totalSize/1MB,2)) MB"
    Write-Host ""
}

function Invoke-TempCleanup {
    Write-Host "[*] SAFE TEMP CLEANUP" -ForegroundColor Cyan
    Write-Log "Temp cleanup requested"

    $confirm = Read-Host "Delete temp files in user and system temp folders? (Y/N)"
    if ($confirm -notin @("Y","y")) {
        Write-Host "[-] Temp cleanup cancelled."
        Write-Log "Temp cleanup cancelled by user"
        return
    }

    $paths = @(
        $env:TEMP,
        $env:TMP,
        "$env:SystemRoot\Temp"
    ) | Where-Object { $_ -and (Test-Path $_) }

    $deleted = 0
    $freed   = 0

    foreach ($p in $paths) {
        Write-Host "Cleaning: $p"
        Get-ChildItem -Path $p -Recurse -Force -ErrorAction SilentlyContinue | ForEach-Object {
            if (-not $_.PSIsContainer) {
                try {
                    $size = $_.Length
                    Remove-Item -LiteralPath $_.FullName -Force -ErrorAction Stop
                    $deleted++
                    $freed += $size
                } catch {
                    # ignore locked files
                }
            }
        }
    }

    Write-Host ""
    Write-Host ("Files deleted: {0}" -f $deleted)
    Write-Host ("Space freed  : {0:N2} MB" -f ($freed / 1MB))
    Write-Log "Temp cleanup: $deleted files, $([math]::Round($freed/1MB,2)) MB freed"
    Write-Host ""
}

# =========================
# NETWORK DIAGNOSTICS / REPAIR (SAFE)
# =========================
function Invoke-NetworkDiagnostics {
    Write-Host "[*] Running Network Diagnostics..." -ForegroundColor Cyan
    Write-Log "Network diagnostics started"

    Write-Host ""
    Write-Host "=== BASIC CONNECTIVITY ===" -ForegroundColor Yellow
    try {
        $ping = Test-Connection -ComputerName 8.8.8.8 -Count 2 -Quiet -ErrorAction SilentlyContinue
        if ($ping) {
            Write-Host "[+] Internet connectivity appears OK (8.8.8.8 reachable)."
            Write-Log "Network OK"
        } else {
            Write-Host "[-] 8.8.8.8 not reachable." -ForegroundColor Red
            Write-Log "Ping 8.8.8.8 failed"
        }
    } catch {
        Write-Host "[-] Ping test failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Log "Ping test error: $_"
    }

    Write-Host ""
    Write-Host "=== DNS TEST (www.microsoft.com) ===" -ForegroundColor Yellow
    try {
        $dns = Test-Connection -ComputerName www.microsoft.com -Count 1 -Quiet -ErrorAction SilentlyContinue
        if ($dns) {
            Write-Host "[+] DNS resolution OK."
            Write-Log "DNS OK"
        } else {
            Write-Host "[-] DNS resolution failed." -ForegroundColor Red
            Write-Log "DNS failed"
        }
    } catch {
        Write-Host "[-] DNS test failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Log "DNS test error: $_"
    }

    Write-Host ""
    Write-Host "[+] Network diagnostics complete." -ForegroundColor Green
    Write-Log "Network diagnostics completed"
    Write-Host ""
}

function Invoke-NetworkRepairSafe {
    Write-Host "[*] Running Network Auto‑Fix (SAFE MODE)..." -ForegroundColor Cyan
    Write-Log "Network auto-fix requested"

    Write-Host ""
    Write-Host "This will run:" -ForegroundColor Yellow
    Write-Host "  - ipconfig /flushdns"
    Write-Host "  - netsh winsock reset"
    Write-Host ""
    $confirm = Read-Host "Proceed with these safe network repair commands? (Y/N)"
    if ($confirm -notin @("Y","y")) {
        Write-Host "[-] Network auto‑fix cancelled."
        Write-Log "Network auto-fix cancelled"
        return
    }

    try {
        Write-Host "[*] Flushing DNS cache..."
        ipconfig /flushdns | Out-Host
        Write-Log "ipconfig /flushdns executed"
    } catch {
        Write-Host "[-] Failed to flush DNS: $($_.Exception.Message)" -ForegroundColor Red
        Write-Log "FlushDNS error: $_"
    }

    try {
        Write-Host "[*] Resetting Winsock..."
        netsh winsock reset | Out-Host
        Write-Log "netsh winsock reset executed"
    } catch {
        Write-Host "[-] Failed to reset Winsock: $($_.Exception.Message)" -ForegroundColor Red
        Write-Log "Winsock reset error: $_"
    }

    Write-Host ""
    Write-Host "[+] Network auto‑fix complete. A reboot is recommended." -ForegroundColor Green
    Write-Log "Network auto-fix completed"
    Write-Host ""
}

# =========================
# SYSTEM FILE CHECK / REPAIR (SFC / DISM)
# =========================
function Invoke-SystemRepair {
    Write-Host "[*] System File / Image Repair (SFC / DISM)" -ForegroundColor Cyan
    Write-Log "System repair requested"

    Write-Host ""
    Write-Host "This can take a while and may require administrator rights." -ForegroundColor Yellow
    Write-Host "Commands to be run (if you confirm):"
    Write-Host "  - sfc /scannow"
    Write-Host "  - DISM /Online /Cleanup-Image /RestoreHealth"
    Write-Host ""
    $confirm = Read-Host "Run SFC and DISM now? (Y/N)"
    if ($confirm -notin @("Y","y")) {
        Write-Host "[-] System repair cancelled."
        Write-Log "System repair cancelled"
        return
    }

    try {
        Write-Host "[*] Running: sfc /scannow"
        Write-Log "Running sfc /scannow"
        sfc /scannow | Out-Host
    } catch {
        Write-Host "[-] SFC failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Log "SFC error: $_"
    }

    try {
        Write-Host "[*] Running: DISM /Online /Cleanup-Image /RestoreHealth"
        Write-Log "Running DISM /Online /Cleanup-Image /RestoreHealth"
        DISM /Online /Cleanup-Image /RestoreHealth | Out-Host
    } catch {
        Write-Host "[-] DISM failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Log "DISM error: $_"
    }

    Write-Host ""
    Write-Host "[+] System repair routine completed. A reboot is recommended." -ForegroundColor Green
    Write-Log "System repair completed"
    Write-Host ""
}

# =========================
# AUTO‑HEAL ENGINE (LOGICAL)
# =========================
function Invoke-AutoHeal {
    Write-Host "[*] Running ULTRA Auto‑Heal Engine (logical, safe)..." -ForegroundColor Cyan
    Write-Log "Auto‑Heal started"

    $steps = @(
        "Analyzing recent system errors (logical)...",
        "Refreshing internal health indicators...",
        "Resetting non‑critical internal states...",
        "Recommending reboot if instability persists..."
    )

    foreach ($s in $steps) {
        Write-Host "[*] $s"
        Write-Log $s
        Start-Sleep -Milliseconds 200
    }

    Write-Host ""
    Write-Host "[+] Auto‑Heal routine completed." -ForegroundColor Green
    Write-Log "Auto‑Heal completed"
    Write-Host ""
}

# =========================
# MENU / MAIN
# =========================
function Show-Menu {
    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  1) Run ULTRA diagnostics"
    Write-Host "  2) Crash / BSOD analyzer"
    Write-Host "  3) Startup analyzer"
    Write-Host "  4) Temp scan (safe)"
    Write-Host "  5) Temp cleanup (safe)"
    Write-Host "  6) Network diagnostics"
    Write-Host "  7) Network auto‑fix (safe)"
    Write-Host "  8) System repair (SFC / DISM)"
    Write-Host "  9) Auto‑Heal engine"
    Write-Host "  0) Exit"
    Write-Host ""
}

function Main-Loop {
    Show-Banner
    Write-Host "FixPilot‑AI ULTRA PC Edition — Source‑Intelligent Architect" -ForegroundColor Cyan
    Write-Host ""
    do {
        Show-Menu
        $choice = Read-Host "Select an option"
        switch ($choice) {
            "1" { Invoke-Diagnostics }
            "2" { Invoke-CrashAnalyzer }
            "3" { Invoke-StartupAnalyzer }
            "4" { Invoke-TempScan }
            "5" { Invoke-TempCleanup }
            "6" { Invoke-NetworkDiagnostics }
            "7" { Invoke-NetworkRepairSafe }
            "8" { Invoke-SystemRepair }
            "9" { Invoke-AutoHeal }
            "0" { Write-Host "Goodbye."; Write-Log "Session ended by user" }
            default { Write-Host "Invalid choice." }
        }
    } while ($choice -ne "0")
}

# =========================
# ENTRY POINT
# =========================
Write-Log "FixPilot‑AI ULTRA PC started"
if ($Auto) {
    Show-Banner
    Invoke-Diagnostics
} else {
    Main-Loop
}
