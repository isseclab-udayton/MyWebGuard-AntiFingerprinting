# Load necessary libraries, including matplotlib, sklearn

import pandas as pd
import numpy as np
import init_data2 as id

import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, roc_auc_score, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier

from sklearn import svm
from sklearn import linear_model
from sklearn import tree
from sklearn import naive_bayes
from sklearn import neighbors
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load sklearn's own data
def plot_ROC(datapath,function,name,colors):
	dataset = pd.read_excel(data_path,sheet_name='train_data',header=0)

	dataset_y = dataset.pop("SPECIES")

	X = np.array(dataset)
	y = np.array(dataset_y)
	print(y)
	y = label_binarize(y, range(0,68))
	print(y.shape)


# Randomly divide the data into train set and test set
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.1, random_state=2019)
	# Build the svm model and calculate the probability y_score of each sample in the test set
	classifier = OneVsRestClassifier(function)
	y_score = classifier.fit(X_train, y_train).predict_proba(X_test)
	# Calculate the AUC of the micro method, and the average is set to macro, which is the macro method
	roc_auc_micro = roc_auc_score(y_test,y_score,average='micro')
	# Calculate the fpr and tpr needed to draw the roc curve
	fpr_micro, tpr_micro, _ = roc_curve(y_test.ravel(), y_score.ravel())
	# draw roc curve
	plt.figure
	plt.plot(fpr_micro, tpr_micro,
	label= name+' ROC curve (area = {0:0.4f})'.format(roc_auc_micro),
	color=colors, linestyle=':', linewidth=4)
	plt.plot([0, 1], [0, 1], 'k--', lw=2)
	plt.xlim([-0.05, 1.0])
	plt.ylim([0.0, 1.05])
	plt.xlabel('False Positive Rate')
	plt.ylabel('True Positive Rate')
	plt.title('Multi-Class ROC')
	plt.legend(loc="lower right")


data_path = r"D:\Designer\TEST_HASH\train_data.xls"
window = 20
#id.init_data(window)

plot_ROC(data_path,svm.SVC(probability=True),"svm",'blue')
plot_ROC(data_path,tree.DecisionTreeClassifier(criterion='entropy'),"tree",'red')
plot_ROC(data_path,naive_bayes.GaussianNB(),"bayes",'green')
plot_ROC(data_path,neighbors.KNeighborsClassifier(n_neighbors = 3),"knn",'orange')
plot_ROC(data_path,RandomForestClassifier(),"random_forest",'lightpink')

plt.show()





