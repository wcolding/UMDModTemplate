Start-Process -NoNewWindow -FilePath "python" -ArgumentList "pack.py" -wait

$dir = (Get-Location).ToString()
$dirConfig = Get-Content -Path ./directory.ini
$configData = ConvertFrom-StringData -StringData $dirConfig
$systemDir = $configData["SystemFolder"]
$umdDir = $systemDir + "\UMDS"

if ($systemDir -ne "")
{
    Write-Host "Conviction System Folder found:"$systemDir
    $existingUMD = $umdDir + "\Conviction.umd"
    try 
    {
        $convictionFile = Get-Item $existingUMD
        if ($convictionFile.length/1MB -lt 5)
        {
            # Conviction.umd is compressed, so rename it as backup
            Rename-Item -Path $existingUMD -NewName $existingUMD".backup"
        }
        else
        {
            # Conviction.umd is uncompressed, so delete it
            Remove-Item -Path $existingUMD
        }
    } catch {}

    $buildFile = $dir + "\Build\Conviction.umd"
    Copy-Item -Path $buildFile -Destination $umdDir
    Write-Host "Done copying. Starting game..."
    $gameFile = $systemDir + "\conviction_game.exe"
    Start-Process -FilePath $gameFile
}
else
{
    Write-Host "Conviction System folder not configured in directory.ini"
}