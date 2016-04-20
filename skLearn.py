from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
import numpy as np
import pickle

ds = load_files ('pubMed/learn')
dsTest = load_files('pubMed/test')



text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge',
penalty='l2', alpha=1e-3, n_iter=5, random_state=42))])

_ = text_clf.fit(ds.data, ds.target)
pickle.dump(text_clf, open("pickled/trained.p", 'wb'))


predicted = text_clf.predict(dsTest.data)

print(np.mean(predicted == dsTest.target))


''''works well with only two categories of CT'''