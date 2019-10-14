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
print(keywords_list)

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