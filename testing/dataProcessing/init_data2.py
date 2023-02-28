import matplotlib.pylab
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def label_data(window,label,filepath,if_analysis):

	df = pd.read_excel(filepath,sheet_name=1,header=None)
#	df = df.loc[1:10000,:]
	line = df.shape[0]
	group_num = line//window
	result = pd.DataFrame()
	for i in range(1,window*group_num,window):
		group = df.loc[i:i+window-1,:]

		max = group.max()
		max.columns=['max_baidu','max_sina','max_nju','max_iqiyi','max_douban','max_so','max_youku','max_qidian','max_2345','max_dianping','max_seu']
		min = group.min()
		min = min.dropna(axis=0,how='any')
		min.columns =['min_baidu','min_sina','min_nju','min_iqiyi','min_douban','min_so','min_youku','min_qidian','min_2345','min_dianping','min_seu']
#		rms = np.square((df **2).mean())
#		rms = rms.dropna(axis=0,how='any') 
		rms = group.mad()
		rms = rms.dropna(axis=0,how='any')
		rms.columns=['rms_baidu','rms_sina','rms_nju','rms_iqiyi','rms_douban','rms_so','rms_youku','rms_qidian','rms_2345','rms_dianping','rms_seu']  
		skew = group.skew()
		skew = skew.dropna(axis=0,how='any')
		skew.columns=['skew_baidu','skew_sina','skew_nju','skew_iqiyi','skew_douban','skew_so','skew_youku','skew_qidian','skew_2345','skew_dianping','skew_seu']  
		kurt = group.kurt()
		kurt = kurt.dropna(axis=0,how='any')
		kurt.columns=['kurt_baidu','kurt_sina','kurt_nju','kurt_iqiyi','kurt_douban','kurt_so','kurt_youku','kurt_qidian','kurt_2345','kurt_dianping','kurt_seu']  
		mean = group.mean()
		mean = mean.dropna(axis=0,how='any')
		mean.columns=['mean_baidu','mean_sina','mean_nju','mean_iqiyi','mean_douban','mean_so','mean_youku','mean_qidian','mean_2345','mean_dianping','mean_seu']  
		var = group.var()
		var = var.dropna(axis=0,how='any')
		var.columns=['var_baidu','var_sina','var_nju','var_iqiyi','var_douban','var_so','var_youku','var_qidian','var_2345','var_dianping','var_seu']  

		temp = pd.concat([max,min,rms,skew,kurt,mean,var],axis=1,join='outer')
		temp = pd.DataFrame(temp.values.reshape(1,7*11))
		result = pd.concat([result,temp],axis=0,join='outer')
	
	result = result.apply(lambda x : (x-np.min(x))/(np.max(x)-np.min(x)))
	result = result.dropna(axis=0,how='any')
	if if_analysis==False:
		result['SPECIES']=str(label)
	return result

def file_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        print("Current raw data path:",root) #current directory path  
       # print(dirs) #All subdirectories under the current path  
        print('Raw data lists:',files) #All non-directory subfiles in the current path
    return files

def init_data(window,srcpath,despath,if_analysis):
	print("Initiate Dataset Now...")
	files = file_name(srcpath)
	count=0
	df_list=[]
	classes = pd.DataFrame(columns=['hash', 'class'])
	for file in files:
		filepath = srcpath+'\\'+file
		temp = label_data(window,label=count,filepath=filepath,if_analysis=if_analysis)
		df_list.append(temp)
		classes = classes.append([{'hash':file,'class':count}])
		count=count+1
	result = pd.concat(df_list,axis=0,join='inner')
	print("Dataset has been initiated already!")
	# filepath0 = r"D:\Designer\TEST_HASH\29c766b048c0786ac2278b4637c4d495.xls"
	# a0 = label_data(window=window,label=0,filepath=filepath0)
	# filepath1 = r"D:\Designer\TEST_HASH\c5d9d939372416933222d371ac1242b5.xls"
	# a1 = label_data(window=window,label=1,filepath=filepath1)
	# filepath2 = r"D:\Designer\TEST_HASH\0c981dc68f0c23e4c2711350960b2e03.xls" 
	# a2 = label_data(window=window,label=2,filepath=filepath2)
	# filepath3 = r"D:\Designer\TEST_HASH\04fb1040ca87200b4b8012b68f91434c.xls" 
	# a3 = label_data(window=window,label=3,filepath=filepath3)
	# result = pd.concat([a0,a1,a2,a3],axis=0,join='inner') 

	result = result.sample(frac=1.0)
	result = result.reset_index(drop=True)
	if os.path.exists(despath+"\\train_data.xls"):
		os.remove(despath+"\\train_data.xls")
	writer = pd.ExcelWriter(despath+"\\train_data.xls")
	result.to_excel(writer,'train_data')
	writer.save()
	writer2 = pd.ExcelWriter(despath+"\\hash_classes.xls")
	classes.to_excel(writer2,'hash_classes')
	writer2.save()
