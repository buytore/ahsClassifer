Created on Tue Apr 12 07:32:08 2016
@author: markbannan
"""
from sklearn.datasets import fetch_20newsgroups
import os

categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

twenty_train.target_names

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
X_train_counts.shape

from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_train_tf.shape

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape

# Training the classifier

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

docs_new = ['God is love', 'OpenGL on the GPU is fast']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))
    
# BUILD KRS CLASSIFIER AND TRAINING DATA
    
path = os.getcwd() + '\\text\\'                               #Get the current directory
#path = 'C:\Users\markbannan\python\py3\nlEg\krs\text\'
filenames = next(os.walk(path))[2]                  #Get all the files in current directory

docs_krs =[]
for f in filenames:
    filename, file_extension = os.path.splitext(f)
    #print "this is the file name: ", filename
    #print "this is the file extension: ", file_extension
    if file_extension == ".txt":
        krs_file = open('text\\'  + f, "r")
        krs_file_content = krs_file.read()
        docs_krs.append(krs_file_content)
        
X_new_counts = count_vect.transform(docs_krs)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))
