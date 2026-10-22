# Ejecutar en PowerShell de Windows. Requiere Git instalado.
$ErrorActionPreference = 'Stop'
$repoUrl = 'https://github.com/yovoyTecSRL/iBloom-chef-By-orbix.git'
$desktopPath = [Environment]::GetFolderPath('Desktop')
if ([string]::IsNullOrWhiteSpace($desktopPath)) { throw 'No se encontro el Escritorio de Windows.' }
$destinationPath = Join-Path $desktopPath 'iBloom-chef-By-orbix'
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Instale Git para Windows y vuelva a abrir PowerShell antes de continuar.'
}
if (Test-Path -LiteralPath $destinationPath) {
    throw "La carpeta ya existe. No se ha modificado: $destinationPath"
}
& git clone -- $repoUrl $destinationPath
if ($LASTEXITCODE -ne 0) { throw 'No se pudo clonar. Revise acceso a GitHub. Un clon incompleto puede requerir revision manual.' }
Write-Host "Clon creado: $destinationPath"
Write-Host 'GitHub es el origen remoto. No se ha conectado por SSH ni desplegado en Hetzner.'
Write-Host 'Los enlaces del sitio estan en enlaces/sitio.json.'
