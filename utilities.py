import hashlib

def Xor(data):
    dataArray = bytearray(data)
    encrypted = dataArray
    size = len(dataArray)
    for i in range(size):
        encrypted[i] = dataArray[i] ^ 183 # Key is 0xB7
    return encrypted

def GetMD5(data):
    return hashlib.md5(str(data).encode('utf-8')).hexdigest()

def MatchesMD5(manifestMD5, data):
    return GetMD5(data) == manifestMD5