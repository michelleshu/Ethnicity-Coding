import csv

# Read attributes of training instances, save to lists of names, confidences, ethnicities
def parseTrainingData(trainFile):
    names, ethnicities, confidences = [], [], []
    with open(trainFile, 'rb') as csvfile:
        filereader = csv.reader(csvfile)
        for row in filereader:
            names.append(row[0].strip())
            ethnicities.append(row[1].strip())
            confidences.append(row[2].strip())
    csvfile.close()
    return names, ethnicities, confidences


# (names, ethnicities, confidences) = parseTrainingData('MTest.csv')
# for i in range(10):
#     print "Name: " + names[i]
#     print "Ethnicity: " + ethnicities[i]
#     print "Confidences: " + confidences[i]


# Get names of test instances to make predictions on
def parseTestData(testFile):
    names = []
    with open(testFile, 'rb') as csvfile:
        filereader = csv.reader(csvfile)
        for row in filereader:
            names.append(row[0].strip())
    csvfile.close()
    return names