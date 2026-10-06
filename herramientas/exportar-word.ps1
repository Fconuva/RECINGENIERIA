param([Parameter(Mandatory=$true)][string]$Documento)
$docPath=(Resolve-Path -LiteralPath $Documento).Path
$pdfPath=[IO.Path]::ChangeExtension($docPath,'.pdf')
$wordApp=$null
$ownedDoc=$null
try {
    $wordApp=New-Object -ComObject Word.Application
    $wordApp.Visible=$false
    $ownedDoc=$wordApp.Documents.Open($docPath,$false,$true)
    $ownedDoc.ExportAsFixedFormat($pdfPath,17)
    Write-Output "PDF exportado: $pdfPath"
} finally {
    if($ownedDoc){$ownedDoc.Close(0);[void][Runtime.InteropServices.Marshal]::ReleaseComObject($ownedDoc)}
    if($wordApp){if($wordApp.Documents.Count -eq 0){$wordApp.Quit()};[void][Runtime.InteropServices.Marshal]::ReleaseComObject($wordApp)}
}
