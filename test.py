import pandas as pd
import os

#방법 1. 전체 경로 입력
df1=pd.read_table('problem.1', sep=' ', skiprows=3, header=None)

print(df1[[4, 9]])
# print(df1[df1.columns=[0,1]].values)

# win