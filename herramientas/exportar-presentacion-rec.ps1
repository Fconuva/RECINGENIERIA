param([Parameter(Mandatory=$true)][string]$Documento)
$ErrorActionPreference='Stop'
$recPptPath=(Resolve-Path -LiteralPath $Documento).Path
$recPdfPath=[IO.Path]::ChangeExtension($recPptPath,'.pdf')
$recPptApp=New-Object -ComObject PowerPoint.Application
$recPptDoc=$null
$recOwnApp=($recPptApp.Presentations.Count -eq 0)
try {
    $recPptDoc=$recPptApp.Presentations.Open($recPptPath,-1,0,0)
    $recPptDoc.SaveAs($recPdfPath,32)
    @{paginas=$recPptDoc.Slides.Count;pdf=$recPdfPath} | ConvertTo-Json -Compress
} finally {
    if($recPptDoc){$recPptDoc.Close();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($recPptDoc)}
    if($recOwnApp -and $recPptApp.Presentations.Count -eq 0){$recPptApp.Quit()}
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($recPptApp)
}
