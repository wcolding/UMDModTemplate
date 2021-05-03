import os
import hashlib

srcdir = "src"
baseLevel = os.listdir(srcdir)
baseDir = os.getcwd() + "\\" + srcdir + "\\"

uncompressed = os.getcwd() + "\\UMD\\Uncompressed.umd"
umdFile = open(uncompressed, "rb")
umdData = umdFile.read()

def GetOffset(umd, file):
    if file in umd:
        return umd.index(file)
    else:
        return -1

filelist = []

def ReadFiles(files, dir=""):
    for file in files:
        dirstring = baseDir + dir
        filestring = dirstring + file
        if "." in file:
            # This is a file, add it to the manifest
            curFile = open(filestring, "rb")
            curData = curFile.read()
            md5 = hashlib.md5(str(curData).encode('utf-8')).hexdigest()
            filelist.append(str(dir + file + "," + str(GetOffset(umdData, curData)) + "," + str(curFile.tell()) + "," + md5))
            curFile.close()
        else:
            # This is a folder, search its contents
            nextLevel = os.listdir(filestring)
            nextDir = dir + file + "\\"
            ReadFiles(nextLevel, nextDir)

ReadFiles(baseLevel)
umdFile.close()

manifest = open("manifest.txt", "w")

for line in filelist:
    print(line)
    manifest.write(line + "\n")

manifest.close()