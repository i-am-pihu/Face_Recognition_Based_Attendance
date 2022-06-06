import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import os


x1,x2,x3,x4=[],[],[],[]

required_df = pd.read_csv('Attendance_2020-02-22.csv')


Id = 1

print(required_df)

flag = len(required_df[required_df['Id']==Id])



if flag:
   pass
else:
   
   required_df.loc['1'] = [3, 'Shivam', '2020-02-22', '11:22:30']


print(required_df)
print(len(required_df))
