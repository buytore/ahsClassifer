# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 13:50:09 2016

@author: markbannan
"""
import os, re
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB


ds = load_files ('_learn')
dsTest = load_files('_test')

from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', MultinomialNB()),])
                     
text_clf = text_clf.fit(pmcTrainData.data, pmcTrainData.target)
print "Targets: ", pmcTrainData.target

categories = pmcTrainData.target_names
docs_krs=[]
for category in categories:
    testingPath = os.path.join(testPath, category)
    filesInPath = next(os.walk(testingPath))[2]
    for file in filesInPath:
        krs_file = open(os.path.join(testingPath, file), "r")
        krs_file_content = krs_file.read()
        docs_krs.append(krs_file_content)
        krs_file.close()


import numpy as np
#twenty_test = load_files(trainPath, description=None, categories=None, load_content=True, 
#                            shuffle=True, encoding=None, decode_error='strict', random_state=0)
# docs_test = twenty_test.data
predicted = text_clf.predict(docs_krs)

for predict in predicted:
    print "The Predicted: ", predict
    
print "The Mean: ", np.mean(predicted == pmcTrainData.target)            


