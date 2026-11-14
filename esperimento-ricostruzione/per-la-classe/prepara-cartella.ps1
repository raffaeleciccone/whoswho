# Prepara una cartella con SOLO i documenti di Who's Who, per l'esperimento di ricostruzione.
#
#   .\prepara-cartella.ps1 C:\lezione\ricostruito            # documenti attuali (consigliato)
#   .\prepara-cartella.ps1 C:\lezione\ricostruito -Prova1    # documenti della prova 1 (prima delle correzioni)
#
# Se PowerShell blocca lo script: powershell -ExecutionPolicy Bypass -File .\prepara-cartella.ps1 <cartella>
param(
    [Parameter(Mandatory = $true)][string]$Cartella,
    [switch]$Prova1
)
$ErrorActionPreference = "Stop"
$qui = Split-Path -Parent $MyInvocation.MyCommand.Path
$radice = Resolve-Path (Join-Path $qui "..\..")

if ((Test-Path $Cartella) -and (Get-ChildItem $Cartella -Force | Select-Object -First 1)) {
    throw "La cartella $Cartella non e' vuota: scegline una nuova."
}
New-Item -ItemType Directory -Force $Cartella | Out-Null

if ($Prova1) {
    Copy-Item (Join-Path $qui "documenti-prova-1\*.md") $Cartella
} else {
    foreach ($f in "SPEC.md", "PIANO.md", "AGENTS.md", "CLAUDE.md", "README.md", "HANDOFF.md") {
        Copy-Item (Join-Path $radice $f) $Cartella
    }
    New-Item -ItemType Directory -Force (Join-Path $Cartella "design") | Out-Null
    Copy-Item (Join-Path $radice "design\bozza.html") (Join-Path $Cartella "design")
}
Write-Host "Pronto. Nella cartella ci sono solo questi file:"
Get-ChildItem $Cartella -Recurse -File | ForEach-Object { Write-Host "  " $_.FullName.Substring((Resolve-Path $Cartella).Path.Length + 1) }
