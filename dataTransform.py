# coding: utf-8
from pandas import DataFrame
import pandas as pd
def DataTransform():
    df=pd.read_csv('data.txt',sep='\t')
    print df
    df.to_csv('new_data.csv',encoding='utf-8')
DataTransform()