import csv
from enum import Enum


# title是初始需求，最开始的commit是需求实现
#随后的discuss是需求变更的讨论文本，discuss之后的commit是本次变更对应的实现。
#以此类推，后面还有可能多次变更
	
class item: #每个item可能包含若干条record，比如初始commit有好几条的话，都算作初始需求实现
	def __init__(self,ty):
		self.typ=ty #类型为需求讨论系列（多条讨论）或需求实现系列（多条commit）
		self.records=list()
	def addRecord(self,r):
		self.records.append(r)
	def show(self):
		print('************************************************************************')
		print('* type:',self.typ)
		print('*-----------------------------------------------------------------------')
		for x in self.records:
			x.show()
		print('************************************************************************')

	def save(self,f):
		f.write('************************************************************************\n')
		f.write('* type: '+self.typ+'\n')
		f.write('*-----------------------------------------------------------------------\n')
		for x in self.records:
			x.save(f)
		f.write('************************************************************************\n')


class record: #每个record是一次发言/一次提交。
	def __init__(self,t,c,l,u):
		self.time=t
		self.content=c
		self.label=l
		if(len(u)!=0):
			self.url=u
		else:
			self.url=''
			
	def show(self):
		print('* time:',self.time)
		print('* content:',self.content)
		if(self.url!=''):
			print('* codeUrl:',self.url)
		# print('------------------------------------------')
	def save(self,f):
		f.write('* time: '+self.time+'\n')
		f.write('* content: '+self.content+'\n')
		if(self.url!=''):
			f.write('* codeUrl: '+self.url+'\n')
		

class Transaction:
	def __init__(self,filename):
		self.timeline = list()  # 一个list包括若干个item，每个item可能是初始需求，初始提交，改变需求，改变提交
		try:
			with open(filename,'r',encoding='gbk') as f:
				csvReader = csv.reader(f)
				csvReader=list(csvReader)
				self.id=csvReader[0][0]
				self.title=csvReader[0][1]
				csvReader=csvReader[1:]
				csvReader.sort(key=lambda x:x[0])
				i=0
				while(i<len(csvReader)-1):
					if(csvReader[i][1]=='discuss'):
						tempList=item('discussion')
					else:
						tempList=item('implements')
					while(1):
						t,l,c,u=csvReader[i][0],csvReader[i][1],csvReader[i][2],''
						c=c.replace('\n',' ')
						if(l=='commit'): #如果类型为commit，则记录url
							u=csvReader[i][3]
						r=record(t,c,l,u)
						tempList.addRecord(r)
						i+=1
						if(i==len(csvReader)-1 or csvReader[i][1]!=csvReader[i-1][1]):
							break
					self.timeline.append(tempList)
		except UnicodeDecodeError:
			print(filename)
			
	def show(self):
		print('************************************************************************')
		print('* id:',self.id)
		print('* requirement:',self.title)
		if(len(self.timeline)==0): #没有具体内容
			print('timeline of '+self.id+' is empty.')
		elif(len(self.timeline)==1): #只有一次提交或者一次讨论，没有形成完整时间线
			if(self.timeline[0].typ!='implements'):
				print('the requirement of '+self.id+' has no implements.')
			else:
				print('the requirement of '+self.id+' only has implements, no discussion.')
		elif(len(self.timeline)==2): #只有一次提交和一次讨论，也没有形成完整时间线
			print('*=======================================================================')
			print('* no changes, only the initial requirement, implements, and discussion.')
			print('*=======================================================================')
			for x in self.timeline:
				x.show()
		else: #有多次commit和discussion交互的时间线
			i=0
			while(i<len(self.timeline)):
				print('*=======================================================================')
				print('* round '+str(int(i/2)))
				print('*=======================================================================')
				self.timeline[i].show()
				try:
					self.timeline[i+1].show()
				except:
					pass
				i+=2

	
	def save(self):
		with open('./timelineResult/timeline_'+self.id+'.txt','w',encoding='utf=8') as f:
			print(self.id, 'has', len(self.timeline), 'items.')
			f.write('************************************************************************\n')
			f.write('* id: '+self.id+'\n')
			f.write('* requirement: '+self.title+'\n')
			if (len(self.timeline) == 0):  # 没有具体内容
				f.write('timeline of ' + self.id + ' is empty.\n')
			elif (len(self.timeline) == 1):  # 只有一次提交或者一次讨论，没有形成完整时间线
				if (self.timeline[0].typ != 'implements'):
					f.write('the requirement of ' + self.id + ' has no implements.\n')
				else:
					f.write('the requirement of ' + self.id + ' only has implements, no discussion.\n')
			elif (len(self.timeline) == 2):  # 只有一次提交和一次讨论，也没有形成完整时间线
				f.write('*=======================================================================\n')
				f.write('* no changes, only the initial requirement, implements, and discussion.\n')
				f.write('*=======================================================================\n')
				for x in self.timeline:
					x.save(f)
			else:  # 有多次commit和discussion交互的时间线
				i = 0
				while (i < len(self.timeline)):
					f.write('*=======================================================================\n')
					f.write('* round ' + str(int(i / 2))+'\n')
					f.write('*=======================================================================\n')
					self.timeline[i].save(f)
					try:
						self.timeline[i + 1].save(f)
					except:
						pass
					i += 2
				
for i in range(2,1275):
	# print(i)
	try:
		t=Transaction('./data/pr_'+str(i)+'.csv')
		t.save()
	except FileNotFoundError:
		print(str(i)+".csv doesn't exist.")
		pass
	# t.save()