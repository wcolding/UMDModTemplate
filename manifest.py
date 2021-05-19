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

def SwapFile(filestring):
    f = open(filestring, "rb")
    fData = f.read()
    newData = utilities.Xor(fData)
    f.close()

    e = open(filestring, "wb")
    e.write(newData)
    e.close()


def ReadFiles(files, umdData, subdir=""):
    for file in files:
        dirstring = settings.srcDir + subdir
        filestring = dirstring + file
        if "." in file:
            # This is a file, add it to the manifest

            # If this is not a Conviction file, xor it
            if not settings.game == settings.Game.Conviction:
                SwapFile(filestring)

            curFile = open(filestring, "rb")
            curData = curFile.read()
            offset = GetOffset(umdData, curData)
            if offset > -1:
                AddEntry(subdir + file, offset, curData)
            else:
                if not settings.useOptimizedManifest:
                    AddEntry(subdir + file, offset, curData)
                else:
                    print("%s not found in Uncompressed.umd, skipping"%(subdir + file))
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
    count = 0
    for line in filelist:
        count += 1
        manifest.write(line)
        if count < len(filelist):
            manifest.write("\n")

    manifest.close()
    print("All done!")