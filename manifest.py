import os
import settings
import utilities

filelist = []

def GetOffset(umd, file):
    if file in umd:
        return umd.index(file)
    else:
        return -1

def AddEntry(path, offset, data):
    md5 = utilities.GetMD5(data)
    newEntry = "%s,%i,%i,%s"%(path, offset, len(data), md5)
    #newEntry = str(subdir + file + "," + str(offset) + "," + str(curFile.tell()) + "," + md5)
    filelist.append(newEntry)
    print(newEntry)


def ReadFiles(files, umdData, subdir=""):
    for file in files:
        dirstring = settings.srcDir + subdir
        filestring = dirstring + file
        if "." in file:
            # This is a file, add it to the manifest
            curFile = open(filestring, "rb")
            curData = curFile.read()
            offset = GetOffset(umdData, curData)
            if offset > -1:
                AddEntry(subdir + file, offset, curData)
            else:
                if not settings.useOptimizedManifest:
                    AddEntry(subdir + file, offset, curData)
            curFile.close()
        else:
            # This is a folder, search its contents
            nextLevel = os.listdir(filestring)
            nextDir = subdir + file + "\\"
            ReadFiles(nextLevel, umdData, nextDir)

def Generate():
    print("Generating manifest. Please be patient...")

    baseLevel = os.listdir(settings.srcDir)
    uncompressed = settings.umdDir + "Uncompressed.umd"
    umdFile = open(uncompressed, "rb")
    data = umdFile.read()
    ReadFiles(baseLevel, data)
    umdFile.close()

    manifest = open("manifest.txt", "w")

    for line in filelist:
        manifest.write(line + "\n")

    manifest.close()
    print("All done!")