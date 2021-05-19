import os
import shutil
import settings
import manifest

umdFiles = os.listdir('UMD')
unumdPath = settings.baseDir + "\\Tools\\unumd.exe"
fileCount = 0
matches = 0

for file in umdFiles:
    if (settings.umdName in file) & (matches < 1):
        filestring = settings.umdDir + file
        curUMD = open(filestring, "rb")
        curData = curUMD.read()
        UMDsize = len(curData)
        print("Found " + file + " - " + str(UMDsize) + " bytes")
        fileCount += 1
        matches += 1

        shutil.copyfile(unumdPath, settings.umdDir + "unumd.exe")
        os.chdir(settings.umdDir)
        os.system("unumd -unpack -out=Temp %s"%(settings.umdName))
        os.system("unumd -out=src %s"%(settings.umdName))
        shutil.copyfile(settings.umdDir + "Temp/%s"%(settings.umdName), settings.umdDir + "Uncompressed.umd")
        shutil.move(settings.umdDir + "src", settings.baseDir + "\\src")
        shutil.rmtree(settings.umdDir + "Temp")
        os.remove("unumd.exe")
        os.chdir(settings.baseDir) 
        curUMD.close()

if matches > 0:
    print("Match found for %s"%(settings.umdName))
    if fileCount > 0:
        manifest.Generate()
    else:
        print("No files were extracted.")
else:
    print("No match found for %s. Checking settings.py and UMDs folder."%(settings.umdName))