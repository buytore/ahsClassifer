# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:48:52 2016

@author: markbannan
"""
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
import numpy as np
import os

categories = ['Addiction', 'AIDS', 'Alcohol_Alcohol', 'Allergy', 'Arthritis', 
              'Blood', 'Brain', 'Cancer', 'Cardiovasc_Res', 'Diabetes', 'Heart']
# categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']

pmcData = load_files('_learn/', description=None, categories=categories, load_content=True, 
                            shuffle=True, encoding=None, decode_error='strict', random_state=0)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(pmcData.data)
X_train_counts.shape

print "X_train_counts: ", X_train_counts
print "X_train Shape: ", X_train_counts.shape

tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_train_tf.shape

print "X_trainTF Counts: ", X_train_counts
print "X_trainTF Shape: ", X_train_counts.shape


tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape
print "X_trainTFidf counts: ", X_train_counts
print "X_trainTFidf Shape: ", X_train_counts.shape

# Training the classifier
testData = load_files('_test/', description=None, categories=None, load_content=True, 
                            shuffle=True, encoding=None, decode_error='strict', random_state=0)
                            
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, pmcData.target)
text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),('clf', MultinomialNB()),])
text_clf = text_clf.fit(testData.data, testData.target)
print text_clf



docs_test = testData.data
predicted = text_clf.predict(docs_test)
print np.mean(predicted == testData.target)

from sklearn import metrics
print(metrics.classification_report(twenty_test.target, predicted,
    target_names=twenty_test.target_names))