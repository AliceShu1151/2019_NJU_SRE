file_name = "../data/pr_title.txt"

text = open(file_name)
text_string = text.read()
keywords = text_string.split()
text.close()

dict = {}
for word in keywords:
    if dict.__contains__(word):
        dict[word]=dict[word]+1
    else:
        dict[word]=1

keywords_set = dict.items()
keywords_list=[]
for key,word in keywords_set:
    keywords_list.append((key,word))
keywords_list.sort(key=lambda element: element[1],reverse = True)
# print(keywords_list)

target_file_name = "keywords_list.csv"
target_file = open(target_file_name,mode='w')
target_file.write('keyword')
target_file.write(',')
target_file.write('frequency')
target_file.write('\n')
for word,frequency in keywords_list:
    target_file.write(word)
    target_file.write(',')
    target_file.write(str(frequency))
    target_file.write('\n')

target_file.close()

#读取pr标题存入列表
pr_title_list = []
with open(file_name) as f:
    for line in f:
        # print(line.__len__())
        pr_title_list.append(line)

#根据关键字将pr标题分类
classified_file = open("classified_pull_request.txt",mode='w')
for word,frequency in keywords_list:
    if frequency<5:
        break
    classified_file.write(word)
    classified_file.write(':')
    classified_file.write('\n')
    for line in pr_title_list:
        word_in_line_list=line.split()
        if word in word_in_line_list:
            classified_file.write('\t')
            classified_file.write(line)
    classified_file.write('\n')
classified_file.close()

    