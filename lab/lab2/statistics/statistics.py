from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix

y_true = [0]*10000

y_pred = [0]*10000

file_name = "../refined_data/refinedeclipse_bugs_310000.csv"
with open(file_name) as f:
    for line in f:
        temp_list = line.split(',')
        if temp_list[0]=="id":
            continue
        no = int(temp_list[0])-310000
        if temp_list[3][0:2] == "P1":
            y_pred[no]=1
        elif temp_list[3][0:2] == "P2":
            y_pred[no]=2
        elif temp_list[3][0:2] == "P3":
            y_pred[no]=3
        elif temp_list[3][0:2] == "P4":
            y_pred[no]=4
        elif temp_list[3][0:2] == "P5":
            y_pred[no]=5

level_flag = 1
classified_file = "test_classified.txt"
with open(classified_file) as cf:
    for line in cf:
        if line=="P1:\n":
            level_flag=1
            continue
        elif line=="P2:\n":
            level_flag=2
            continue
        elif line=="P3:\n":
            level_flag=3
            continue
        elif line=="P4:\n":
            level_flag=4
            continue
        elif line=="P5:\n":
            level_flag=5
            continue
        else:
            temp_list = line.split(',')
            no = int(temp_list[0])-310000
            y_true[no]=level_flag

accuracy = accuracy_score(y_true,y_pred)
print("Accuracy Rate: "+str(accuracy))
matrix = confusion_matrix(y_true,y_pred)
print("confusion matrix: ")
print("    P1   P2   P3   P4   P5")
print(matrix)

recall1 = matrix[0][0]/sum(matrix[0])
recall2 = matrix[1][1]/sum(matrix[1])
recall3 = matrix[2][2]/sum(matrix[2])
recall4 = matrix[3][3]/sum(matrix[3])
recall5 = matrix[4][4]/sum(matrix[4])
print("P1 recall score: "+ str(recall1))
print("P2 recall score: "+ str(recall2))
print("P3 recall score: "+ str(recall3))
print("P4 recall score: "+ str(recall4))
print("P5 recall score: "+ str(recall5))
# recall = recall_score(y_true,y_pred,None,1,None)
# print("recall score: "+recall)

