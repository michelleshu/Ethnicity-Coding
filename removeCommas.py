import csv
import sys
import os

# Remove all commas - use for 1-column CSV files with unnecessary commas
def removeCommas(fileDir):
    fileNames = os.listdir(fileDir)
    for fileName in fileNames:
        with open(fileName, mode="rU") as inFile:
            filereader = csv.reader(infile, dialect=csv.excel_tab)
            with open("_" + fileName, mode="w") as outfile:
                for rows in filereader:
                    filewriter = csv.writer(outfile, delimiter='"')
                    filewriter.writerows(rows)

def main():
    removeCommas(sys.argv[1])