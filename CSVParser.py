import csv
import string

# Read attributes of training instances, save to lists of names, confidences, ethnicities
def parseTrainingData(trainFile):
    names, ethnicities, confidences = [], [], []
    with open(trainFile, 'rU') as csvfile:
        filereader = csv.reader(csvfile, dialect=csv.excel_tab)
        for row in filereader:
            data = row[0].split(',')
            rawName = stripPunctuation(data[0].strip())
            delimitedName = "$" + rawName + "$"
            names.append(delimitedName)
            ethnicities.append(stripPunctuation(data[1].strip()))
            confidences.append(data[2].strip())
    csvfile.close()
    return names, ethnicities, confidences


# Get names of test instances to make predictions on
def parseTestData(testFile):
    names, trueLabels = [], []
    with open(testFile, 'rU') as csvfile:
        filereader = csv.reader(csvfile, dialect=csv.excel_tab)
        for row in filereader:
            data = row[0].split(',')
            rawName = stripPunctuation(data[0].strip())
            delimitedName = "$" + rawName + "$"
            names.append(delimitedName)
            if len(data) == 2:
                trueLabels.append(stripPunctuation(data[1].strip()))
    csvfile.close()
    return names, trueLabels


# Strip all punctuation symbols out of name
def stripPunctuation(s):
    return s.translate(string.maketrans("",""), string.punctuation)