# Exporta andre_becker_DR1_TP2.docx para PDF pelo proprio Word (mesma renderizacao do arquivo aberto).
#
#     powershell -NoProfile -File scripts/exportar_pdf.ps1
#
# DisplayAlerts = 0: um aviso numa janela invisivel nao segura a exportacao.
$raiz = Split-Path -Parent $PSScriptRoot
[string]$docx = Join-Path $raiz 'andre_becker_DR1_TP2.docx'
[string]$pdf  = Join-Path $raiz 'andre_becker_DR1_TP2.pdf'

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($docx, $false, $true, $false)   # sem conversao, somente leitura
    $doc.ExportAsFixedFormat($pdf, 17)                          # 17 = wdExportFormatPDF
    $doc.Close($false)
} finally {
    $word.Quit()
}
"gerado: $pdf"
