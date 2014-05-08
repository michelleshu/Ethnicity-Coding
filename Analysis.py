from numpy import *                                         # for array representation
from sklearn.ensemble import RandomForestClassifier         # for random forest implementation
from CSVParser import *                                     # parse data from CSV files
import sys

MIN_N = 3   # minimum n-gram length
MAX_N = 3   # maximum n-gram length

# Create a map from ethnicities to integers (class labels) for enumerating classes
def createEthnicityMapping(ethnicity):
    classes = unique(ethnicity)   # the number of classes observed
    ethnicityToClassLabel = {}
    for i in range(len(classes)):
        ethnicityToClassLabel[classes[i]] = i
    return ethnicityToClassLabel


# Convert ethnicity names to class labels
def getClassLabel(ethnicity, ethnicityToClassLabel):
    label = zeros(len(ethnicity))
    for i in range(len(ethnicity)):
        label[i] = ethnicityToClassLabel[ethnicity[i]]
    return label


# Get all the unique n-grams found in training set
def collectNGrams(names):
    # Make a set of unique n-grams found in names
    ngrams = set()
    for n in range(MIN_N, MAX_N + 1):   # number of characters per n-gram
        for name in range(len(names)):
            for j in range(len(names[name]) - n + 1):
                gram = names[name][j:j+n]
                if gram not in ngrams:
                    ngrams.add(gram)
    return ngrams


# Convert names to binary vector representing the n-grams present
def getVectorRep(names, ngrams):
    # Initialize vector representation of names of dimensionality (# of names) x (# of n-grams)
    rep = zeros((len(names), len(ngrams)))
    for name in range(len(names)):
        i = 0
        for gram in ngrams:
            # if that ngram appears in the name, then "activate" that element of the name's vector representation
            if gram in names[name]:
                rep[name, i] = 1
            i += 1
    return rep

# Convert integer encoding of class label back to string
def retrieveClass(prediction, dinv):
    l = []
    for i in range(len(prediction)):
        l.append(dinv[int(prediction[i].astype(int))])
    return l


def checkCorrectness(predictedLabels, trueLabels):
    correct = []
    numCorrect = 0
    for i in range(len(predictedLabels)):
        if predictedLabels[i] == trueLabels[i]:
            correct.append(1)
            numCorrect += 1
        else:
            correct.append(0)

    return correct, numCorrect


# to obtain results from the classifiers, we output the results to a file, as specified by the input variable "f".
# pass into the function the individual's names and the classifications
def writeResults(names, testPredictedLabels, testTrueLabels, correct, testClassConfidences, filename):
    # Remove delimiters from names
    for i in range(len(names)):
        names[i] = names[i][1:-1]

    if len(testTrueLabels) > 0: # true labels provided
        d = [names, testPredictedLabels, testTrueLabels, correct, testClassConfidences]
        length = len(d[1])   # length along the top of array - will have to loop over this in order to write file
        header = ['Surname', 'Predicted', 'True', 'Correct', 'Confidence']  # headers
        with open(filename, 'wb') as f:      # create file with name as specified as input
            write = csv.writer(f)    # generate object to write to the file
            write.writerow(header)   # first write the header
            for i in range(length):  # for each column thereafter write the corresponding element of the list
                write.writerow([x[i] for x in d])
    else:
        d = [names, testPredictedLabels, testClassConfidences]
        length = len(d[1])
        header = ['Surname', 'Predicted', 'Confidence']
        with open(filename, 'wb') as f:
            write = csv.writer(f)
            write.writerow(header)
            for i in range(length):
                write.writerow([x[i] for x in d])


def runClassifier(trainDataFile, testDataFile, resultsFile):
    # load information from CSV files into lists in our environment
    trainNames, trainEthnicities, trainConfidences = parseTrainingData(trainDataFile)
    testNames, testTrueLabels = parseTestData(testDataFile)

    print 'Loaded training and testing data'

    # create mapping from ethnicities to numerical class labels and vice versa
    ethnicityToClassLabel = createEthnicityMapping(trainEthnicities)
    classLabelToEthnicity = {v: k for k, v in ethnicityToClassLabel.items()}

    ngrams = collectNGrams(trainNames)

    # Convert names to binary vector representations with ngrams
    trainRepresentations = getVectorRep(trainNames, ngrams)
    testRepresentations = getVectorRep(testNames, ngrams)

    print 'Created vector representations of names'
    trainLabels = getClassLabel(trainEthnicities, ethnicityToClassLabel)

    print 'Learning random forest...'

    rfClassifier = RandomForestClassifier(n_estimators=100, n_jobs=-1, max_depth=None, min_samples_split=7,
                                          random_state=0).fit(trainRepresentations, trainLabels)

    testPredictions = atleast_2d(rfClassifier.predict(testRepresentations)).T

    # Get confidence in predictions
    testClassProbabilities = atleast_2d(rfClassifier.predict_proba(testRepresentations))    # probabilities of all
    testClassConfidences = []   # probabilities of predicted class

    for i in range(len(testNames)):
        conf = '{0:.4g}'.format(testClassProbabilities[i][int(testPredictions[i][0])])
        testClassConfidences.append(conf)

    print 'Test predictions generated'
    testPredictedLabels = retrieveClass(testPredictions, classLabelToEthnicity)

    correct = []
    if len(testTrueLabels) > 0:
        correct, numCorrect = checkCorrectness(testPredictedLabels, testTrueLabels)

        print 'Accuracy: ' + str(float(numCorrect)/float(len(testPredictedLabels))) + ' (' + str(numCorrect) + '/' + \
          str(len(testPredictedLabels)) + ') correct'

    writeResults(testNames, testPredictedLabels, testTrueLabels, correct, testClassConfidences, resultsFile)

    print 'Random forest test predictions written to file'


def main():
    runClassifier(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
