from numpy import *                                         # for array representation
from sklearn.ensemble import RandomForestClassifier         # for random forest implementation
from CSVParser import *                                     # parse data from CSV files
import sys

# create a dictionary that maps ethnicities to an integer number - necessary for enumerating classes, but will be
# converted back at final output stage
def createDictionary(ethnicity):
    c = unique(ethnicity)   # the number of classes that were actually observed
    d = {}                  # set up dictionary - similar to a hashmap (takes keys to values)
    for i in range(len(c)): # for each observed ethnicity label
        d[c[i]] = i         # generate a mapping: label -> number
    return d                # return mapping


# it is necessary to convert the surnames into a vector representation that can be handled by a classifier.
# function takes a list of surnames and returns binary representation
def createVectors(names):
    n = 3           # number of character n-grams to consider in each name
    ngrams = set()  # initialize set of n-grams
    for name in range(len(names)):
        # proceed through the name in proper step sizes so as to consider all n-gram sequences
        for j in range(len(names[name]) - n + 1):
            gram = names[name][j:j+n]           # construct the n-gram
            if gram not in ngrams:              # if the n-gram has not been seen before, add it to the list of n-grams
                ngrams.add(gram)

    # initialize vector representation of names of dimensionality (# of names) x (# of n-grams)
    rep = zeros((len(names), len(ngrams)))
    for name in range(len(names)):
        i = 0
        for gram in ngrams:
            # if that ngram appears in the name, then "activate" that element of the name's vector representation
            if gram in names[name]:
                rep[name, i] = 1
            i += 1
    return rep, ngrams


# using the mapping created by the function createDictionary, convert the string labels of each name into an integer
# representation
def createLabels(ethnicity,d):
    label = zeros(len(ethnicity))   # every individual obtains a new integer label,
                                        # so initialize vector of that dimensionality
    for i in range(len(ethnicity)):     # for every individual
        label[i] = d[ethnicity[i]]      # index into the dictionary their ethnicity and obtain its corresponding

    #reshape(label, len(ethnicity))

                                        # integer label and assign it to that individual
    return label

# create vector representations using the n-grams found earlier for the unlabeled data
def evaluationVectors(evaluation,ngrams):
    # initialize matrix of representation of dimensionality (# of unlabeled names) x (# of ngrams)
    repEval = zeros((len(evaluation),len(ngrams)))
    for name in range(len(evaluation)):   # for each name in the list of names
        i = 0                             # initialize counter as before
        for gram in ngrams:               # for every ngram we saw in the training state
             # if it appears in the name, activate that component of the vector representation
            if gram in evaluation[name]:
                repEval[name,i] = 1
            i += 1
    return repEval  # return vector representation of the name

# for readability, in the output we reverse the encoding of the ethnicities as integer values and obtain their
# string values
def retrieveClass(prediction,dinv):

    l = []  # initialize list of labels
    for i in range(len(prediction)):                    # for every individual whose ethnicity we predicted
        l.append(dinv[int(prediction[i].astype(int))])      # reindex into the dictionary and extract the string using the
                                                        # integer prediction and add it to the list

    return l  # return the list


# to obtain results from the classifiers, we output the results to a file, as specified by the input variable "f".
# pass into the function the individual's names and the classifications
def writeResults(names, testLabels, filename):
    d = [names, testLabels]  # set up list to write to file - first column is surname, the gradient boosted and
                         # random forest classifications, respectively
    length = len(d[1])   # length along the top of array - will have to loop over this in order to write file
    header = ['Surname', 'Predicted Ethnicity (RF)']  # provide headers for the top of the generated csv
    with open(filename, 'wb') as f:      # create file with name as specified as input
        write = csv.writer(f)    # generate object to write to the file
        write.writerow(header)   # first write the header
        for i in range(length):  # for each column thereafter write the corresponding element of the list
            write.writerow([x[i] for x in d])


def runClassifier(trainDataFile, testDataFile, resultsFile):
    # load information from CSV files into lists in our environment
    trainNames, trainEthnicities, trainConfidences = parseTrainingData(trainDataFile)
    testNames = parseTestData(testDataFile)

    print 'Loaded training and testing data...'

    # create mapping from ethnicities to numerical class labels and vice versa
    ethnicityToClassLabel = createDictionary(trainEthnicities)
    classLabelToEthnicity = {v: k for k, v in ethnicityToClassLabel.items()}

    trainRepresentations, ngrams = createVectors(trainNames)

    print 'Created vector representations of names...'
    print 'The dimensionality of the representation... ', trainRepresentations.shape
    trainLabels = createLabels(trainEthnicities, ethnicityToClassLabel)

    testRepresentations = evaluationVectors(testNames, ngrams)

    print 'Learning random forest...'

    print trainLabels.shape
    rfClassifier = RandomForestClassifier(n_estimators=100, n_jobs=-1, max_depth=None, min_samples_split=7,
                                          random_state=0).fit(trainRepresentations, trainLabels)

    testPredictions = atleast_2d(rfClassifier.predict(testRepresentations)).T

    print 'Test predictions generated, size... ', testPredictions.shape
    testLabels = retrieveClass(testPredictions, classLabelToEthnicity)

    writeResults(testNames, testLabels, resultsFile)

    print 'Random forest test predictions written to file'


def main():
    runClassifier(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()