from sklearn import svm, datasets
svc = svm.SVC(kernel='linear')
iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target
clf = svc.fit(X,y)
clf.predict([[7,3]])
