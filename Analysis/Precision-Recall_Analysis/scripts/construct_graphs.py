import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools


#Import Data
mbhmms_card = pd.read_csv("../s01-card/MBhmms/201006-MBhmms_pr_analysis.txt",sep='\t',skiprows=2,usecols=[0,4,5],names=["Family","Precision", "Recall"])
mbhmms_card["Database"] = "Resfams 2.0"
oldres_card = pd.read_csv("../s01-card/OldRes/201006-res_pr_analysis.txt",sep='\t',skiprows=2,usecols=[0,4,5],names=["Family","Precision", "Recall"])
oldres_card["Database"] = "Resfams 1.0"
mbhmms_ncbi = pd.read_csv("../s02-ncbi/MBHmms/201007-MBHmms_pr_analysis.txt",sep='\t',skiprows=2,usecols=[0,4,5],names=["Family","Precision", "Recall"])
mbhmms_ncbi["Database"] = "Resfams 2.0"
oldres_ncbi = pd.read_csv("../s02-ncbi/OldRes/201007-OldRes_pr_analysis.txt",sep='\t',skiprows=2,usecols=[0,4,5],names=["Family","Precision", "Recall"])
oldres_ncbi["Database"] = "Resfams 1.0"


# #Parse Data
ncbi_frames = [mbhmms_ncbi,oldres_ncbi]
ncbi_data = pd.concat(ncbi_frames,ignore_index=True, sort=False)
ncbi_temp = pd.merge(mbhmms_ncbi,oldres_ncbi,on='Family')
mbhmms_ncbi = ncbi_temp[["Family", "Precision_x", "Recall_x","Database_x"]]
mbhmms_ncbi.columns = ["Family", "Precision", "Recall","Database"]
oldres_ncbi = ncbi_temp[["Family", "Precision_y", "Recall_y","Database_y"]]
oldres_ncbi.columns = ["Family", "Precision", "Recall","Database"]

ncbi_data = pd.concat(ncbi_frames,ignore_index=True, sort=False).fillna(value=0.0).round(4)
ncbi_data['Precision'] = ncbi_data[['Precision']] * 100
ncbi_data['Recall'] = ncbi_data[['Recall']] * 100
ncbi_pData = ncbi_data[['Family','Database','Precision']]
ncbi_pData["Analysis"] = "Precision"
ncbi_pData.columns = ['Family','Database','Value','Analysis']
ncbi_rData = ncbi_data[['Family','Database','Recall']]
ncbi_rData["Analysis"] = "Precision"
ncbi_rData.columns = ['Family','Database','Value','Analysis']



## Make Graphs
#Precision
f, ax = plt.subplots(figsize=(18,25))

ncbi_gpData = ncbi_pData.pivot('Family','Database','Value')
pHeatMap = sns.heatmap(ncbi_gpData,cmap="Spectral",ax=ax,linewidths=0.01,linecolor='black',annot=True,fmt='g')
pHeatMap.set_title('Database Precision Comparative Analysis')
pHeatMap.get_figure().savefig("../plots/201010-ncbi_precision.png",bbox_inches='tight')

#Recall
f, ax = plt.subplots(figsize=(18,25))

ncbi_grData = ncbi_rData.pivot('Family','Database','Value')
rHeatMap = sns.heatmap(ncbi_grData,cmap="Spectral",ax=ax,linewidths=0.01,linecolor='black',annot=True,fmt='g')
rHeatMap.set_title('Database Recall Comparative Analysis')
rHeatMap.get_figure().savefig("../plots/201010-ncbi_recall.png",bbox_inches='tight')
