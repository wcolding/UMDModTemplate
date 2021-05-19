import os
import shutil
import settings
import manifest

# Mops up anything unumd unpacks to the base directory
def MoveExtraFiles():
    os.chdir(settings.baseDir)
    rootFiles = os.listdir()
    srcExists = False
    movedExists = False

    if 'src' in rootFiles:
        srcExists = True

    for file in rootFiles:
        if file not in settings.allowedFilesList:
            print("File %s is not supposed to be here! Moving it to src folder."%(file))
            curPath = settings.baseDir + "\\" + file
            movedPath = settings.baseDir + "\\src\\MOVED\\"
            newPath = movedPath + file
            #print("%s -> %s"%(curPath, newPath))
            
            if not srcExists:
                os.mkdir('src')
                srcExists = True
            
            if not movedExists:
                os.chdir(settings.srcDir)
                srcFiles = os.listdir()
                
                if 'MOVED' not in srcFiles: 
                    os.mkdir('MOVED')
                movedExists = True
                os.chdir(settings.baseDir)
                
            shutil.move(curPath, newPath)

def UnpackAndExtract():
    umdFiles = os.listdir('UMD')
    unumdPath = settings.baseDir + "\\Tools\\unumd.exe"
    fileCount = 0
    matches = 0
    
    for file in umdFiles:
        if (settings.umdName in file) & (matches < 1):
            print("Match found for %s"%(settings.umdName))
            filestring = settings.umdDir + file
            curUMD = open(filestring, "rb")
            curData = curUMD.read()
            curUMD.close()
            UMDsize = len(curData)
            print("Found " + file + " - " + str(UMDsize) + " bytes")
            fileCount += 1
            matches += 1

            shutil.copyfile(unumdPath, settings.umdDir + "unumd.exe")
            os.chdir(settings.umdDir)
            noxorString = ""
            if not (settings.game == settings.Game.Conviction):
                noxorString = "-noxor "
            os.system("unumd -unpack %s-out=Temp %s"%(noxorString, settings.umdName))
            os.system("unumd -out=src %s"%(settings.umdName))
            shutil.copyfile(settings.umdDir + "Temp/%s"%(settings.umdName), settings.umdDir + "Uncompressed.umd")
            shutil.move(settings.umdDir + "src", settings.baseDir + "\\src")
            shutil.rmtree(settings.umdDir + "Temp")
            os.remove("unumd.exe")

            MoveExtraFiles()
            os.chdir(settings.baseDir)
            

    if matches > 0:
        if fileCount > 0:
            manifest.Generate()
        else:
            print("No files were extracted.")
    else:
        print("No match found for %s. Checking settings.py and UMDs folder."%(settings.umdName))

UnpackAndExtract()