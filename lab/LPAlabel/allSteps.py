import re
from pyspark import *
import os
import LPA

os.environ["SPARK_HOME"] = "D:\spark-2.4.3-bin-hadoop2.7"
os.environ["HADOOP_HOME"] = "D:\winutil"

#preprocess：把每一项的关键词格式化，去掉无用的标点符号
#eg：25 IDEA|95644|Support|console|input|filtering
def extractWord():
	with open('../data/pr_title.txt',encoding='gbk') as f:
		lines=f.readlines()
	r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^`{|}~]+'
	res=list()
	for line in lines:
		line=re.sub(r,' ',line) #把标点符号用空格代替
		line=line.split()			
		res.append(line[0]+' '+'|'.join(line[1:])+'\n') #以name+空格+word1|word2……的格式输出
	with open('0.txt','w',encoding='utf-8') as f1:
		f1.writelines(res)

#step1：以word为索引，每行存放关键词对应的所有pr的id
#eg：make出现在了6 30 58 104 129 486 518 569 652 915 995 1107 1126的pr里
#ps：后来在结果中我手动删去了IDEA in to for四个频率过高且没有实际意义的词
def step1():
	d=dict()
	with open('0.txt',encoding='utf-8') as f:
		lines=f.readlines()
	for line in lines:
		line=line.split()
		id,wordlist=line[0],line[1]
		for word in wordlist.split('|'):
			d[word]=d.get(word,'')+' '+id
	with open('1.txt','w',encoding='utf-8') as f:
		for k,v in d.items():
			f.write(v+'\n')
			
#step2：统计任意两个pr之间的联系形成键值对
#eg：('99,102', 5)说明99号pr和102号pr有五个word相同
def step2():
	#cooccurence统计一行里的id共现次数
	def cooccurrence(line):
		mapRes = []
		words = line.split(" ")
		words = set(words)
		for word1 in words:
			for word2 in words:
				if word1 != word2:
					mapRes.append(word1 + "," + word2)
		return mapRes
	sc = SparkContext('local')
	datas = [x.strip() for x in open('1.txt',encoding='utf-8').readlines()]
	rdd = sc.parallelize(datas)
	# WordCount
	wordcount = rdd.flatMap(cooccurrence) \
		.map(lambda word: (word, 1)) \
		.reduceByKey(lambda a, b: a + b)
	wordcount.sortBy(lambda x: x[0], False, 1).saveAsTextFile("./step2")
			
#step3：统计每个与之链接的pr在本pr占的比例
#eg：('94', '918,0.037037037037037035|887,0.037037037037037035|838,0.037037037037037035|799,0.037037037037037035|719,0.037037037037037035|680,0.037037037037037035|664,0.037037037037037035|651,0.037037037037037035|625,0.037037037037037035|426,0.037037037037037035|364,0.037037037037037035|361,0.037037037037037035|309,0.037037037037037035|308,0.037037037037037035|304,0.037037037037037035|302,0.037037037037037035|285,0.037037037037037035|238,0.037037037037037035|225,0.037037037037037035|194,0.037037037037037035|192,0.07407407407407407|181,0.037037037037037035|1210,0.037037037037037035|1208,0.037037037037037035|1059,0.037037037037037035|1003,0.037037037037037035')
def step3():
	#处理得到第一个单词为key的k，v
	def sumMapper(line):
		strIt = line.replace("(", "").replace("'", "").replace(")", "").split(", ")
		words = strIt[0].split(",")
		key = words[0]
		value = words[1] + "," + strIt[1]
		return key, value
	
	def normalizationMapper(args):
		if args[1].find(":") == -1:
			valueRes = args[1].split(",")[0] + "," + "1.0"
		else:
			items = args[1].split(":")[1].split("|")
			sum = int(args[1].split(":")[0])
			names = []
			values = []
			valueRes = ""
			for item in items:
				if item != items[0]:
					valueRes += "|"
				names.append(item.split(",")[0])
				count = int(item.split(",")[1])
				values.append(count / sum)
				valueRes = valueRes + item.split(",")[0] + "," + str(count / sum)
		return args[0], valueRes
	
	def normalizationReducer(valuesa, valuesb):
		reduceRes = ""
		if valuesa.find(":") != -1:
			counta = int(valuesa.split(":")[0])
			valuesa = valuesa.split(":")[1]
		else:
			counta = int(valuesa.split(",")[1])
		if valuesb.find(":") != -1:
			countb = int(valuesb.split(":")[0])
			valuesb = valuesb.split(":")[1]
		else:
			countb = int(valuesb.split(",")[1])
		sum = counta + countb
		reduceRes += str(sum)
		return reduceRes + ":" + valuesa + "|" + valuesb
	sc = SparkContext('local')
	# 从本地载入数据
	rdd = sc.textFile("./step2/part-00000")
	# WordCount
	wordcount = rdd.map(sumMapper) \
		.reduceByKey(normalizationReducer)
	normalization = wordcount.map(normalizationMapper)
	normalization.sortBy(lambda x: x[0], False, 1).saveAsTextFile("./step3")

#step4：使用LPA算法打标签
#eg：
def step4():
	LPA.run()

#最后总结，把id号对应的title都写出来
def summary():
	d=dict()
	with open('../data/pr_title.txt',encoding='gbk') as f1:
		lines1=f1.readlines()
	for line in lines1:
		words=line.strip().split()
		d[words[0]]=' '.join(words[1:])
	for i in range(10):
		with open('4'+str(i)+'.txt',encoding='utf-8') as f2:
			lines2=f2.readlines()
		with open('result'+str(i)+'.txt','w',encoding='utf-8') as f3:
			for line in lines2:
				for id in line.strip().split()[1].split(','):
					f3.write(id+'\t'+d[id]+'\n')
				f3.write('============================================================\n')
			
			
# extractWord()
# step1()
# step2()
# step3()
# step4()
summary()