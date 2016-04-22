# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 09:08:35 2016

@author: markbannan
"""
from nltk.metrics import *
from sklearn.datasets import load_files
from nltk import FreqDist, MLEProbDist, word_tokenize
from nltk.corpus import stopwords
import os

ds = load_files ('_learn')
dsTest = load_files('_test')

#print stopwords.words('english')
def getCategories():
    
    library='_test'
    basePath = os.getcwd()
    dataPath = next(os.walk(basePath))[1]
    libPath = os.path.join(basePath, library)                       #Get the current directory
    trainPath = os.path.join(basePath, dataPath[0])
    testPath = os.path.join(basePath, dataPath[1])
    print "Path: ", libPath
    categoryList = next(os.walk(libPath))[1]                        #Get all the files in current directory
    
    return categoryList, trainPath, testPath

categories, trainDir, testDir = getCategories()

#categories = ['Allergy']
docs_krs = []
totalTokens = 0
for category in categories:
    testingPath = os.path.join(testDir, category)
    filesInPath = next(os.walk(testingPath))[2]
    for file in filesInPath:
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".txt":
            krs_file = open(os.path.join(testingPath, file), "r")
            krs_file_content = krs_file.read().decode('latin-1')
            docs_krs.append(krs_file_content)
            krs_file.close()
            tokens = word_tokenize(krs_file_content)
            print "Filename: ", file
            print "Number of Tokens: ", len(tokens)
            no_stop_words = [w.lower() for w in tokens if w.lower() not in stopwords.words('english') and w.isalpha() and len(w) > 3]
            #calculate the most frequent occurences#
            fdist = FreqDist(no_stop_words)
            mostCommon = fdist.most_common(25)            
            #print "Frequency Distribution: ", fdist
            #print "Twenty Five Common Words: ", mostCommon
            totalTokens += len(tokens)
            tokens = []            
            no_stop_words = []
            fdist = ()
            mostCommon = []
    print category + " Total Words: " + str(totalTokens)
    print category + " Average Word Count: " + str(totalTokens/len(filesInPath))
    totalToken = 0