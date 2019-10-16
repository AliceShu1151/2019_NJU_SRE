from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import DBSCAN

'''效果太差，舍弃
def tfIdf():
	# 进行tfidf提取
	with open('00.txt',encoding='utf-8') as f:
		lines=f.readlines()
	vectorizer = CountVectorizer()
	transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
	# 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
	tfidf = transformer.fit_transform(vectorizer.fit_transform(lines))
	# 获取词袋模型中的所有词语  
	word = vectorizer.get_feature_names()
	# 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
	weight = tfidf.toarray()
	print(lines.shape)

	# === Fit the DBSCAN model and get the classify labels === #
	# new_weight=[1 for i in range(len(words))]
	DBS_clf = DBSCAN(eps=1, min_samples=4)
	DBS_clf.fit(weight)
'''