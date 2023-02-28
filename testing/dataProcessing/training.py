#coding:utf-8
#import tensorflow as tf
print("Loading Components Now...")
import numpy as np
import pandas as pd
import os
import k_fold_split as kfs
import init_data2 as id
import time

from sklearn import svm
from sklearn import linear_model
from sklearn import tree
from sklearn import naive_bayes
from sklearn import neighbors
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from sklearn.externals import joblib

print("Loading Over...")

def train_mod(function,name,result):
	accuracy_vector = []
	for i in range(0,10):
		train,test,train_y,test_y=get_data(i)
		f = function.fit(train,train_y)
		# start_time = time.time()
		pre = function.predict(test)
		# end_time = time.time()
		# time_cost = end_time-start_time
		# print(time_cost)
		accuracy=accuracy_score(test_y,pre)
		accuracy_vector.append(accuracy)
	joblib.dump(f,  r"D:\Designer\TEST_HASH\\" + name+"test.pkl")
	print(name+"_accuracy:",np.mean(accuracy_vector))
	result.append(np.mean(accuracy_vector))
	print(name+"_all_window:",result)

def get_data(i):
	train_path = r"D:\Designer\TEST_HASH\data\train_{}.csv".format(i)
	test_path = r"D:\Designer\TEST_HASH\data\val_{}.csv".format(i)

	#Read the data of the COLUMN column specified in the csv file, the header indicates the number of valid data to read from, and the default is 0
	train = pd.read_csv(train_path)
	test = pd.read_csv(test_path)

	#In real training, there is no need to add labels to train together, so Species is not a feature column
	train_y = train.pop("SPECIES")          #Here the value of train_y is the data vector of the Species column, and there is no such value in train, in other words, train_y is the label value, and train is the training data
	test_y = test.pop("SPECIES")
	return train,test,train_y,test_y


SVM_result = []
tree_result=[]
bayes_result = []
knn_result = []
random_forest_result=[]
for window in range(25,26):
	id.init_data(window,r"D:\Designer\hash",r"D:\Designer\TEST_HASH",False)

	kfs.run_k_fold_split(10)
	print("generate dataset and trainset OK!")

	#load dataset


	train_mod(svm.SVC(),"svm",SVM_result)
	train_mod(tree.DecisionTreeClassifier(criterion='entropy'),"tree",tree_result)
	train_mod(naive_bayes.GaussianNB(),"bayes",bayes_result)
	train_mod(neighbors.KNeighborsClassifier(n_neighbors = 3),"knn",knn_result)
	train_mod(RandomForestClassifier(),"random_forest",random_forest_result)


