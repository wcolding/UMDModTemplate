import os
import directory as dir
import hashlib

filelist = []

def GetOffset(umd, file):
    if file in umd:
        return umd.index(file)
    else:
        return -1

def ReadFiles(files, umdData, subdir=""):
    for file in files:
        dirstring = dir.srcDir + subdir
        filestring = dirstring + file
        if "." in file:
            # This is a file, add it to the manifest
            curFile = open(filestring, "rb")
            curData = curFile.read()
            md5 = hashlib.md5(str(curData).encode('utf-8')).hexdigest()
            newEntry = str(subdir + file + "," + str(GetOffset(umdData, curData)) + "," + str(curFile.tell()) + "," + md5)
            filelist.append(newEntry)
            print(newEntry)
            curFile.close()
        else:
            # This is a folder, search its contents
            nextLevel = os.listdir(filestring)
            nextDir = subdir + file + "\\"
            ReadFiles(nextLevel, umdData, nextDir)

def Generate():
    print("Generating manifest. Please be patient...")

    baseLevel = os.listdir(dir.srcDir)
    uncompressed = dir.umdDir + "Uncompressed.umd"
    umdFile = open(uncompressed, "rb")
    data = umdFile.read()
    ReadFiles(baseLevel, data)
    umdFile.close()

    manifest = open("manifest.txt", "w")

    for line in filelist:
        manifest.write(line + "\n")

    manifest.close()
    print("All done!")