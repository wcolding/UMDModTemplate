import os
from enum import Enum

class Game(Enum):
    Conviction = 5
    Blacklist = 6

# Change this to your umd
umdName = "Conviction.umd"

# Change this to your game
game = Game.Conviction

# If this is set to true then objects that cannot be found in the decompressed UMD will not be logged in the manifest
# This will have the effect of speeding up the build time as it will check fewer files
useOptimizedManifest = True

# If this is set to true then it will *attempt* to resize files to conform with the manifest
# This only triggers if there is a mismatch with the file size and the size in the manifest 
tryResizeFiles = True

# Directory macros for the other scripts, do not modify
SystemFolder = ""
baseDir = os.getcwd()
umdDir = baseDir + "\\UMD\\"
srcDir = baseDir + "\\src\\"