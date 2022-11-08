import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df_ls = pd.read_json('outputs/poliMediaAnalysis.json')
# df_pm = pd.read_json('/outputs/poliMediaAnalysis.json')

df_ls = df_ls.sort_values(['auc'], ascending=False)
print(df_ls.head(25))

# a = [8.9616, 8.9911, 9.5353, 9.8339]
# b = [20,15,9,2]

# plt.plot(b,a)
# plt.title('Logistic regression CER over PCA')
# plt.ylabel('CER in %')
# plt.xlabel('PCA components')
# plt.show()
