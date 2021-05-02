import os
import hashlib

srcdir = "src"
files = os.listdir(srcdir)

uncompressed = os.getcwd() + "\\UMD\\Uncompressed.umd"
umdFile = open(uncompressed, "rb")
umdData = umdFile.read()

def GetOffset(umd, file):
    if file in umd:
        return umd.index(file)
    else:
        return -1

filelist = []

for file in files:
    if "." in file:
        filestring = os.getcwd() + "\\" + srcdir + "\\" + file
        curFile = open(filestring, "rb")
        curData = curFile.read()
        md5 = hashlib.md5(str(curData).encode('utf-8')).hexdigest()
        filelist.append(str(file + "," + str(GetOffset(umdData, curData)) + "," + str(curFile.tell()) + "," + md5))
        curFile.close()

umdFile.close()

manifest = open("manifest.txt", "w")

for line in filelist:
    print(line)
    manifest.write(line + "\n")

manifest.close()