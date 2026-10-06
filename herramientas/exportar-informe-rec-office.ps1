param([Parameter(Mandatory=$true)][string]$Documento)
$ErrorActionPreference='Stop'
$recDocPath=(Resolve-Path -LiteralPath $Documento).Path
$recPdfPath=[IO.Path]::ChangeExtension($recDocPath,'.pdf')
$recWordApp=New-Object -ComObject Word.Application
$recOwnedDoc=$null
$recWordPid=0
$recStarted=Get-Date
Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class RecOfficeWindow { [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr hwnd, out int processId); }'
$recIsolated=($recWordApp.Documents.Count -eq 0)
try {
    if(-not $recIsolated){throw 'The export requires an empty dedicated Word instance.'}
    $recWordApp.Visible=$false
    $recWordApp.DisplayAlerts=0
    [Console]::Error.WriteLine('Office: opening document')
    $recOwnedDoc=$recWordApp.Documents.Open($recDocPath,$false,$false)
    [void][RecOfficeWindow]::GetWindowThreadProcessId([intptr]$recOwnedDoc.ActiveWindow.Hwnd,[ref]$recWordPid)
    if($recOwnedDoc.TablesOfContents.Count -ne 1){throw 'Expected one table of contents.'}
    $recOwnedDoc.TablesOfContents.Item(1).Update()
    $recOwnedDoc.Fields.Update() | Out-Null
    $recOwnedDoc.Repaginate()
    $recOwnedDoc.TablesOfContents.Item(1).Update()
    $recOwnedDoc.Repaginate()
    $recOwnedDoc.Save()
    $recPages=$recOwnedDoc.ComputeStatistics(2)
    [Console]::Error.WriteLine('Office: index updated and saved')
    $recOwnedDoc.ExportAsFixedFormat($recPdfPath,17,$false,0,0,1,1,0,$true,$true,1,$true,$false,$false)
    [Console]::Error.WriteLine('Office: PDF exported')
    @{paginas=$recPages;indice_actualizado=$true} | ConvertTo-Json -Compress
} finally {
    if($recOwnedDoc){
        try {$recOwnedDoc.Close(0)} catch {[Console]::Error.WriteLine($_.Exception.Message)}
        [void][Runtime.InteropServices.Marshal]::ReleaseComObject($recOwnedDoc)
    }
    # This application was created exclusively for this export.
    if($recIsolated){try {$recWordApp.Quit(0)} catch {[Console]::Error.WriteLine($_.Exception.Message)}}
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($recWordApp)
    # Word can leave its isolated automation process alive after disconnecting.
    # Never touch another Office instance or a document open before this export.
    if($recIsolated -and $recWordPid -gt 0){
        $recProcess=Get-CimInstance Win32_Process -Filter "ProcessId=$recWordPid"
        if($recProcess -and $recProcess.Name -eq 'WINWORD.EXE' -and
           $recProcess.CommandLine -match '/Automation -Embedding' -and
           $recProcess.CreationDate -ge $recStarted.AddSeconds(-5)){
            Stop-Process -Id $recWordPid
        }
    }
}
