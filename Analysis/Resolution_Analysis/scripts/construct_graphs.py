import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



data = pd.read_csv("../191218-hitCounts.txt",sep='\t',names=["Database", "Dataset", "Family", "Gene", "Variant", "Total Hits"])
data.head()


sns.set(style="whitegrid")
totComp = sns.barplot(x="Dataset", y="Total Hits", hue="Database", data=data).set_title('Database Search Comparative Analysis')
totCompFig = totComp.get_figure()
totCompFig.savefig("../plots/191218-comparative_analysis.png")




resData = data.loc[data['Dataset'] == "card"].drop(columns=['Total Hits'])
resData = pd.melt(resData, id_vars=['Database','Dataset'], var_name='Ontology Level')
resData = resData.rename({'value': 'Hits'},axis=1)
resComp = sns.barplot(x="Ontology Level", y="Hits", hue="Database", data=resData).set_title('Database Resolution Comparative Analysis')
resCompFig = totComp.get_figure()
resCompFig.savefig("../plots/191218-resolution_analysis.png")
