from sklearn import svm, datasets
import csv
import itertools

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
count_vect = CountVectorizer()
data = []
target = []
with open('../data/Combined_News_DJIA.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in itertools.islice(spamreader, 200):
        data.append(' '.join(row[2:]))
        target.append(row[1:2][0])

data[200]
target[198:200]
X_train_counts = count_vect.fit_transform(data[1:])
tfidf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

svc = svm.SVC(kernel='linear')
svc.fit(X_train_tfidf, target[1:])

new_docs = data[198:200]
X_new_counts = count_vect.transform(new_docs)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

svc.predict(X_new_tfidf)
