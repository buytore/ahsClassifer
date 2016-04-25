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

print(metrics.classification_report(dsTest.target, predicted,target_names=dsTest.target_names))
print (metrics.confusion_matrix(dsTest.target, predicted))



from sklearn.metrics import precision_score
print precision_score(dsTest.target, predicted, average = None)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(ds.data)
count_vect.vocabulary_.get(u'cancer')

http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html
