import sys
import os
from CSVParser import *

# Remove all commas - use for 1-column CSV files with unnecessary commas
def removeCommas(fileDir):
    fileNames = os.listdir(fileDir)
    for fileName in fileNames:
        with open(fileDir + '/' + fileName, mode="rU") as inFile:
            with open(fileDir + '/_' + fileName, mode="w") as outFile:
                for line in inFile:
                    outFile.write(stripPunctuation(line))
            inFile.close()
            outFile.close()
        os.remove(fileDir + '/' + fileName)
        os.rename(fileDir + '/_' + fileName, fileDir + '/' + fileName)

def main():
    removeCommas(sys.argv[1])

if __name__ == '__main__':
    main()