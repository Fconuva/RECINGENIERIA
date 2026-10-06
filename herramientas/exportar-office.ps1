param([string]$Root = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'
$recMaterial = Join-Path $Root 'materiales_comerciales'
$recEvidence = Join-Path $Root 'documentacion/evidencias/diapositivas'
New-Item -ItemType Directory -Path $recEvidence -Force | Out-Null
$recPowerPoint = New-Object -ComObject PowerPoint.Application
try {
    foreach ($recFile in @('REC-presentacion-comercial','REC-tarjeta-91x61-con-sangrado')) {
        $recDeck = $recPowerPoint.Presentations.Open((Join-Path $recMaterial ($recFile+'.pptx')), -1, 0, 0)
        try {
            $recDeck.SaveAs((Join-Path $recMaterial ($recFile+'.pdf')), 32)
            if ($recFile -eq 'REC-presentacion-comercial') {
                for ($recN=1; $recN -le $recDeck.Slides.Count; $recN++) {
                    $recDeck.Slides.Item($recN).Export((Join-Path $recEvidence ('diapositiva-{0:00}.png' -f $recN)), 'PNG', 1600, 900)
                }
            }
            Write-Output ($recFile+': '+$recDeck.Slides.Count+' diapositivas, PDF exportado')
        } finally { $recDeck.Close() }
    }
} finally {
    if ($recPowerPoint.Presentations.Count -eq 0) { $recPowerPoint.Quit() }
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($recPowerPoint)
}
