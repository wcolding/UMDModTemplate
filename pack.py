import os
import csv
import settings
import conform
import utilities
import shutil

manifestFile = open("manifest.txt", "r")
manifest = csv.reader(manifestFile)

changedFiles = []
unchangedFiles = []
sizeChangedFiles = []

for file in manifest:
    filepath = settings.srcDir + file[0]
    print(filepath)
    try:
        f = open(filepath, "rb")
        fdata = f.read()

        if int(file[1]) > -1:
            
            if f.tell() == int(file[2]):                
                if not utilities.MatchesMD5(file[3], fdata):
                    changedFiles.append(file)
                    
            else:
                if settings.tryResizeFiles:
                    result = conform.TryResize(filepath, int(file[2]))
                    if result != 0:
                        print(file[0] + " failed resize attempt and cannot be packed.\n")
                        sizeChangedFiles.append(file) 
                    else:
                        print(file[0] + " was resized successfully!\n") 
                        changedFiles.append(file)
                else:
                    print(file[0] + " failed size check and cannot be packed.\n")
                    sizeChangedFiles.append(file)  

        else:
            
            if not utilities.MatchesMD5(file[3], fdata):
                unchangedFiles.append(file)  

        f.close()

    except:
        print(file[0] + " was unable to be opened")

manifestFile.close()

if (len(unchangedFiles) > 0):
    print("The following files could not located in uncompressed UMD:")
    for file in unchangedFiles:
        print("- " + file[0])
    print("")

if (len(sizeChangedFiles) > 0):
    print("The following files failed size check and could not be packed:")
    for file in sizeChangedFiles:
        print("- " + file[0])
    print("")

numFiles = len(changedFiles)

if (numFiles > 0):
    print(str(numFiles) + " file(s) will be changed:")
    try:
        unpackedPath = settings.umdDir + "Uncompressed.umd"
        unpacked = open(unpackedPath, "rb")
    except:
        print("Unable to open uncompressed UMD. Did you run ./unpack first?")
        raise
    unpackedData = unpacked.read()
    unpackedSize = unpacked.tell()
    patchedData = unpackedData
    unpacked.close()
    
    for file in changedFiles:
       print("- " + file[0])
       filepath = settings.srcDir + file[0]
       f = open(filepath, "rb")
       fdata = f.read()
       fileEndOffset = int(file[1]) + int(file[2])
       patchedData = patchedData[0:int(file[1])] + fdata + patchedData[fileEndOffset:unpackedSize]
       f.close()

    if (settings.game == settings.Game.Conviction):
        print("\nEncoding data...")
        patchedData = utilities.Xor(patchedData)

    patchedPath = "%s\\Build\\%s"%(settings.baseDir, settings.umdName)
    patched = open(patchedPath, "wb")
    patched.write(patchedData)
    patched.close()
    if settings.CopyFolder != "":
        copyPath = settings.CopyFolder
        if (copyPath[-1] != '\\'):
            copyPath += '\\'
        copyPath += settings.umdName
        shutil.copyfile(patchedPath, copyPath)

    print("\nAll finished!")
else:
    print("No files will be changed.")
