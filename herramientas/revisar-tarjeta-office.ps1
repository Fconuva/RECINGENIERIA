param([string]$Root = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'
$recMaterial = Join-Path $Root 'materiales_comerciales'
$recEvidence = Join-Path $Root 'documentacion/evidencias/diapositivas'
New-Item -ItemType Directory -Path $recEvidence -Force | Out-Null
$recPowerPoint = New-Object -ComObject PowerPoint.Application
try {
    $recDeck = $recPowerPoint.Presentations.Open((Join-Path $recMaterial 'REC-tarjeta-91x61-con-sangrado.pptx'), -1, 0, 0)
    try {
        if ($recDeck.Slides.Count -ne 2) { throw 'La tarjeta debe tener dos caras.' }
        for ($recN=1; $recN -le 2; $recN++) {
            $recDeck.Slides.Item($recN).Export((Join-Path $recEvidence ('tarjeta-ppt-{0:00}.png' -f $recN)), 'PNG', 2150, 1441)
        }
        Write-Output 'PowerPoint: dos caras abiertas y exportadas para revisar. PDF original conservado.'
    } finally { $recDeck.Close() }
} finally {
    if ($recPowerPoint.Presentations.Count -eq 0) { $recPowerPoint.Quit() }
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($recPowerPoint)
}
