$dir = (Get-Location).ToString()
$umddir = $dir + "\UMD"
$src = $dir + "\src"
$unumd = $dir + "\Tools\unumd.exe"

New-Item $umddir\Temp -ItemType Directory -ea 0
Remove-Item $umddir\Temp\*.umd
Start-Process -NoNewWindow -FilePath $unumd -ArgumentList "-unpack -path=$umddir -out=$umddir\Temp" -wait
Rename-Item $umddir\Temp\Conviction.umd Uncompressed.umd
Start-Process -NoNewWindow -FilePath $unumd -ArgumentList "-path=$umddir -out=$src" -wait
Move-Item $umddir\Temp\Uncompressed.umd $umddir
Remove-Item $umddir\Temp
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "manifest.py"