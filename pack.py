import os
import hashlib
import csv

dir = os.getcwd()
manifestFile = open("manifest.txt", "r")
manifest = csv.reader(manifestFile)

changedFiles = []

def Xor(data):
    dataArray = bytearray(data)
    encrypted = dataArray
    size = len(dataArray)
    for i in range(size):
        encrypted[i] = dataArray[i] ^ 183 # Key is 0xB7
    return encrypted


for file in manifest:
    filepath = dir + "\\src\\" + file[0]
    print(filepath)
    try:
        f = open(filepath, "rb")
        fdata = f.read()
        if f.tell() == int(file[2]):
            print("Passed size check (" + file[2] + " bytes)")
            md5 = hashlib.md5(str(fdata).encode('utf-8')).hexdigest()
            if md5 in file[3]:
                print("Passed md5 check. No change in file.\n")
            else:
                changedFiles.append(file)
        f.close()
    except:
        print(file[0] + " was unable to be opened")

manifestFile.close()

numFiles = len(changedFiles)
print(str(numFiles) + " file(s) will be changed")

if (numFiles > 0):
    try:
        unpackedPath = dir + "\\UMD\\Uncompressed.umd"
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
       filepath = dir + "\\src\\" + file[0]
       f = open(filepath, "rb")
       fdata = f.read()
       #patchedBackup = bytes(patchedData)
       fileEndOffset = int(file[1]) + int(file[2])
       patchedData = patchedData[0:int(file[1])] + fdata + patchedData[fileEndOffset:unpackedSize]
       f.close()

    print("Encoding data...")
    encryptedData = Xor(patchedData)

    patchedPath = dir + "\\Build\\Conviction.umd"
    patched = open(patchedPath, "wb")
    patched.write(encryptedData)
    patched.close()
    print("\nAll finished!")
