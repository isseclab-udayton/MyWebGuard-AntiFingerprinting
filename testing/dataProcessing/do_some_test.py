# for testing
import pandas as pd
from sklearn.externals import joblib
import init_data2 as id

def load_model(filepath,name):
	result = joblib.load(filepath+"\\" + name+"test.pkl")
	return result

def cal_accuracy(despath,model,target_class):
	dataset = pd.read_excel(despath+"\\train_data.xls",sheet_name='train_data',header=0)

	pres = model.predict(dataset.values)
	print(pres)
	count = 0
	for pre in pres :
		if pre == target_class:
			count=count+1
	accuracy_rate = count/len(pres)
	print(accuracy_rate)

filepath = r"D:\Designer\TEST_HASH\2_classes_model_for_analysis"
svm = load_model(filepath,"svm")
tree = load_model(filepath,"tree")
bayes = load_model(filepath,"bayes")
knn = load_model(filepath,"knn")
random_forest = load_model(filepath,"random_forest")

window=25
srcpath = r"D:\Designer\analysis\ip"
despath = r"D:\Designer\analysis\dataset"
id.init_data(window,srcpath,despath,True)

target_class = 0
cal_accuracy(despath,svm,target_class)
cal_accuracy(despath,tree,target_class)
cal_accuracy(despath,bayes,target_class)
cal_accuracy(despath,knn,target_class)
cal_accuracy(despath,random_forest,target_class)


