import os
import shutil
import directory as dir
import manifest

umdFiles = os.listdir('UMD')
unumdPath = dir.baseDir + "\\Tools\\unumd.exe"
fileCount = 0

for file in umdFiles:
    if "Conviction.umd" in file:
        filestring = dir.umdDir + file
        curUMD = open(filestring, "rb")
        curData = curUMD.read()
        UMDsize = len(curData)
        print("Found " + file + " - " + str(UMDsize) + " bytes")
        if UMDsize < 5000000:
            # UMD is compressed
            fileCount += 1
            shutil.copyfile(unumdPath, dir.umdDir + "unumd.exe")
            os.chdir(dir.umdDir)
            os.system("unumd -unpack -out=Temp Conviction.umd")
            os.system("unumd -out=src Conviction.umd")
            shutil.copyfile(dir.umdDir + "Temp/Conviction.umd", dir.umdDir + "Uncompressed.umd")
            shutil.move(dir.umdDir + "src", dir.baseDir + "\\src")
            shutil.rmtree(dir.umdDir + "Temp")
            os.remove("unumd.exe")
            os.chdir(dir.baseDir) 
        else:
            print("File in directory is uncompressed. Please place an uncompressed umd")
        curUMD.close()

if fileCount > 0:
    manifest.Generate()       