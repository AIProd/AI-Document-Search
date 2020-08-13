

import os
import docx
import docx2txt
import sys
import pandas as pd
from ast import literal_eval

from cdqa.utils.converters import pdf_converter


from cdqa.doc_converter import docxtopdf , ppttopdf
docxtopdf("C:\\Users\\CCD\\Desktop\\Documents_Sample\\Documents") #path to documents 
ppttopdf("C:\\Users\\CCD\\Desktop\\Documents_Sample\\Documents\\PPT Documents") #path to documents 


import os
import docx
import docx2txt
import sys
import pandas as pd
from ast import literal_eval
#import win32com.client

from cdqa.utils.converters import pdf_converter

#convertDocxToText('/databricks/driver/Blob Documents')


#ppt tp pdf
#ppttopdf(path = './')

df_1 = pdf_converter(directory_path= 'C:\\Users\\CCD\\Desktop\\Documents_Sample\\Documents') #path for documents
df_1.head()

#df_1.dropna(axis = 0, how = 'any')
df_1 = df_1[df_1['paragraphs'].notna()]

df_1['paragraphs']=df_1['paragraphs'].apply(lambda x: [string.strip() for string in x if (string != "" and string !=" " and string != "  ")])
  
for i in df_1.iterrows():
  j=i[1]['paragraphs'] 
  for k in range(len(j)):  
    x = j[k].split()  
    if x[-1].startswith('https://') or x[-1].startswith('http://'):  
      x[-1] = x[-1]+" "+"."  
    j[k] = ' '.join(i for i in x)

del x,j,k,i


# create a csv file
df_1.to_csv("Dataset_1.csv", index = False)

