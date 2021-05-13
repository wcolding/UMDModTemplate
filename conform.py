#import os

# targetINI = os.getcwd() + "\\src\\pec.ini"
# targetSize = 78919 # hardcoding this for now, will use manifest later

def TryResize(targetINI, targetSize):
    curFile = open(targetINI, "rb")
    curFileData = curFile.read()
    curFileSize = len(curFileData)
    curFile.seek(0)
    curFileLines = curFileData.splitlines(True)
    curFile.close()

    print("File size:         " + str(curFileSize))
    print("Target file size:  " + str(targetSize))

    difference = curFileSize - targetSize

    if difference == 0:
        print("File is the correct size")
        return 0
    else:
        if difference > 0:
            print("New file is " + str(difference) + " bytes bigger than the original")
        else:
            print("New file is " + str(difference*-1) + " bytes smaller than the original")

    count = 0
    newFileData = b''

    for rawline in curFileLines:
        line = rawline
        lineLen = len(line)
        #print("Line " + str(count) + " is of length " + str(lineLen)) 

        if difference != 0:
            # Check if this is an empty line
            # if line.find(b'\r\n') == 0 & difference > 0:
            #     line = b''
            #     difference -= 2

            # Check if this is a comment line
            if line.find(b'\x2f\x2f') == 0:
                if difference > 0:
                    # We need to remove characters to hit the target size
                    if lineLen > 2:
                        # We can remove some from this line
                        allowedRemoval = lineLen - 2
                        line = line[0:lineLen-2]
                        while (allowedRemoval > 0) & (difference > 0):
                            line = line[0:len(line)-1]
                            allowedRemoval -= 1
                            difference -= 1
                        line += bytes('\r\n', 'utf-8')
                        lineLen = len(line)
                    # if lineLen == 2 & difference > 0:
                    #     # We can only remove the slashes if we have more than 1 byte to lose
                    #     if difference > 1: 
                    #         line = line[0:lineLen-4]
                    #         line += bytes('\r\n', 'utf-8')
                    #         difference -= 2  # Remove the comment slashes
                    #         lineLen = len(line)
                else:
                    # We need to add characters to hit the target size
                    line = line[0:lineLen-2]
                    while (difference) < 0:
                        line += b'\x2f'
                        difference += 1 
                    line += bytes('\r\n', 'utf-8')
            

        newFileData += line
        count += 1

    print("New file size: " + str(len(newFileData)))
    if len(newFileData) == targetSize:
        newFile = open(targetINI, "wb")
        newFile.write(newFileData)
        newFile.close()
        return 0
    else:
        print("Could not auto resize file")
        return -1