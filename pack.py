import os
import hashlib
import csv
import directory as dir

#dir = os.getcwd()
manifestFile = open("manifest.txt", "r")
manifest = csv.reader(manifestFile)

changedFiles = []
unchangedFiles = []
sizeChangedFiles = []

def Xor(data):
    dataArray = bytearray(data)
    encrypted = dataArray
    size = len(dataArray)
    for i in range(size):
        encrypted[i] = dataArray[i] ^ 183 # Key is 0xB7
    return encrypted

def MatchesMD5(manifestMD5, data):
    md5 = hashlib.md5(str(data).encode('utf-8')).hexdigest()
    return md5 == manifestMD5


for file in manifest:
    filepath = dir.srcDir + file[0]
    print(filepath)
    try:
        f = open(filepath, "rb")
        fdata = f.read()

        if int(file[1]) > -1:
            
            if f.tell() == int(file[2]):                
                if not MatchesMD5(file[3], fdata):
                    changedFiles.append(file)
                    
            else:
                print(file[0] + " failed size check and cannot be packed.\n")
                sizeChangedFiles.append(file)  

        else:
            
            if not MatchesMD5(file[3], fdata):
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
        unpackedPath = dir.umdDir + "Uncompressed.umd"
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
       filepath = dir.srcDir + file[0]
       f = open(filepath, "rb")
       fdata = f.read()
       fileEndOffset = int(file[1]) + int(file[2])
       patchedData = patchedData[0:int(file[1])] + fdata + patchedData[fileEndOffset:unpackedSize]
       f.close()

    print("\nEncoding data...")
    encryptedData = Xor(patchedData)

    patchedPath = dir.baseDir + "\\Build\\Conviction.umd"
    patched = open(patchedPath, "wb")
    patched.write(encryptedData)
    patched.close()
    print("\nAll finished!")
else:
    print("No files will be changed.")
