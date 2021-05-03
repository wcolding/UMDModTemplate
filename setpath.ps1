Add-Type -AssemblyName System.Windows.Forms
$foldername = New-Object System.Windows.Forms.FolderBrowserDialog
$foldername.Description = "Select Splinter Cell Conviction System Folder"
$foldername.rootfolder = "MyComputer"
$foldername.SelectedPath = ""
$directory = ""

if($foldername.ShowDialog() -eq "OK")
{
    $directory = $foldername.SelectedPath
    $directory = $directory.Replace("\","\\")
    $fileContents = "SystemFolder = " + $directory
    
    Set-Content -Path ./directory.ini -Value $fileContents
}

