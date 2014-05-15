import csv
import sys
import os

# Remove all commas - use for 1-column CSV files with unnecessary commas
def removeCommas(fileDir):
    fileNames = os.listdir(fileDir)
    for fileName in fileNames:
        with open(fileDir + '/' + fileName, mode="rU") as inFile:
            filereader = csv.reader(inFile, dialect=csv.excel_tab)
            with open(fileDir + '/_' + fileName, mode="w") as outfile:
                for rows in filereader:
                    filewriter = csv.writer(outfile, delimiter='"')
                    filewriter.writerows(rows)
            filewriter.close()
            filereader.close()
        os.remove(fileDir + '/' + fileName)

def main():
    removeCommas(sys.argv[1])

if __name__ == '__main__':
    main()