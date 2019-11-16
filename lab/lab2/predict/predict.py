from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

class dataFormat:
	def summary(end):
		allData=open('../refined_data/refinedeclipse_bugs_1.csv','r',encoding='utf-8').readlines()[1:]
		for i in range(10000,end,10000):
			allData.extend(open('../refined_data/refinedeclipse_bugs_'+str(i)+'.csv','r',encoding='utf-8',errors='ignore').readlines()[1:])
		with open('bugs_500000.csv','w',encoding='utf-8') as f:
			f.writelines(allData)
	def preprocess(fname):
		ids=list()
		titles=list()
		status=list()
		levels=list()
		with open(fname+'.csv',encoding='utf-8')as f:
			lines=f.readlines()
		for line in lines[1:]:
			l=line.split(',')
			# if len(l[1])!=0:
			ids.append(l[0]+'\n')
			titles.append(l[1]+'\n')
			status.append(l[2]+'\n')
			levels.append(l[3][1]+'\n')
		with open(fname+'.id','w',encoding='utf-8')as f:
			f.writelines(ids)
		with open(fname+'.t','w',encoding='utf-8')as f:
			f.writelines(titles)
		with open(fname + '.s', 'w', encoding='utf-8')as f:
			f.writelines(status)
		with open(fname+'.r','w',encoding='utf-8')as f:
			f.writelines(levels)

	def tfIdf(train_sample, test_sample):
		# stop = [k.strip() for k in open('mydata/stopwords-master/.txt', encoding='utf-8').readlines() if k.strip() != '']
		# tfidfvec = TfidfVectorizer(stop_words=stop)
		tfidfvec = TfidfVectorizer()
		# 进行tfidf提取
		train_sample_ = tfidfvec.fit_transform(train_sample)
		test_sample_ = tfidfvec.transform(test_sample)
		return (train_sample_, test_sample_)

class classify:
	def bayes(train_sample,train_solution):
		clf = MultinomialNB()
		# clf = BaggingClassifier(clf, n_estimators=5, max_samples=0.6, bootstrap=True, n_jobs=-1)
		clf.fit(train_sample, train_solution)
		joblib.dump(clf, 'bayes.m')
		return clf
	
	def decisionT(train_sample,train_solution):
		clf = DecisionTreeClassifier()
		clf.fit(train_sample,train_solution)
		joblib.dump(clf,'decisionT.m')
		return clf
	
	def randomF(train_sample,train_solution):
		clf = RandomForestClassifier(n_estimators=50)
		clf.fit(train_sample, train_solution)
		joblib.dump(clf,'randomF.m')
		return clf

	def knn(train_sample,train_solution):
		clf = KNeighborsClassifier(n_neighbors=15, algorithm='brute')
		clf.fit(train_sample,train_solution)
		joblib.dump(clf,'knn.m')
		return clf
		
	def svm(train_sample,train_solution):
		clf = LinearSVC(max_iter=80)
		clf.fit(train_sample,train_solution)
		joblib.dump(clf,'svm.m')
		return clf

# dataFormat.summary(int(500000))
# dataFormat.preprocess('../refinede_data/refinedeclipse_bugs_10000')
# dataFormat.preprocess('bugs_500000')
with open('bugs_overall.t', 'r', encoding='utf-8') as f:
	train_t = f.readlines()

with open('bugs_overall.r', 'r', encoding='utf-8') as f:
	train_r = f.readlines()

train_X, test_X, train_y, test_y = train_t[:500000],train_t[500000:510000],train_r[:500000],train_r[500000:510000]

train_X_, test_X_ = dataFormat.tfIdf(train_X, test_X)

#训练并保存模型
# mdlBayes=classify.bayes(train_X_,train_y)
# mdlDecisionT=classify.decisionT(train_X_[300000:500000],train_y[300000:500000])
# mdlRandomF=classify.randomF(train_X_[400000:500000],train_y[400000:500000])
# mdlKnn=classify.knn(train_X_,train_y)
# mdlSvm=classify.svm(train_X_,train_y)

#查看R2系数
# print('bayes',mdlBayes.score(test_X_, test_y))
# print('decisionTree',mdlDecisionT.score(test_X_,test_y))
# print('randomForest',mdlRandomF.score(test_X_,test_y))
# print('knn',mdlKnn.score(test_X_,test_y))
# print('svm',mdlSvm.score(test_X_,test_y))

#从事先训练好并存下来的模型文件中导入五种预测方法的模型
mdlBayes=joblib.load('bayes.m')
mdlDecisionT=joblib.load('decisionT.m')
mdlRandomF=joblib.load('randomF.m')
mdlKnn=joblib.load('knn.m')
mdlSvm=joblib.load('svm.m')

#五种预测方法的预测结果
bayes_y=mdlBayes.predict(test_X_)
dcsn_y=mdlDecisionT.predict(test_X_)
rdmf_y=mdlRandomF.predict(test_X_)
knn_y=mdlKnn.predict(test_X_)
svm_y=mdlSvm.predict(test_X_)




