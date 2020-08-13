"""## Imports"""

import joblib
import wget
import transformers
import tika
import torchvision
#import spacy
#import Flask
import flask_cors
import joblib
#import scikit_learn
import torch
import markdown
import tqdm
import sentencepiece
import prettytable
import sacremoses
import sys
import pandas as pd
from ast import literal_eval
import re

from cdqa.utils.converters import pdf_converter
from cdqa.utils.filters import filter_paragraphs
from cdqa.pipeline import QAPipeline

from cdqa.utils.download import download_model
from cdqa.pred_clean import clean_pred
from cdqa.summary_clean import trimmed_para, trimmed_summary, extractive_summary

import textwrap
my_wrap = textwrap.TextWrapper(width = 130)

"""## dataframe of documents"""
#change the path accordingly
df=pd.read_csv('df_test5.csv')

"""## formatting paras in df"""

## converting all rows into lists of strings

for i in range(len(df['paragraphs'])):
  df['paragraphs'][i]=eval(df['paragraphs'][i])

## removing other language text and encodings

df['paragraphs']=df['paragraphs'].apply(lambda row: [re.sub(r'[^\x00-\x7F]+', '',string) for string in row])
df['paragraphs']=df['paragraphs'].apply(lambda row: [string.encode('ascii',errors='ignore').decode() for string in row])
df['paragraphs']=df['paragraphs'].apply(lambda x: [re.sub(r"^\s+", "", sentence, flags=re.UNICODE) for sentence in x])
df['paragraphs']=df['paragraphs'].apply(lambda row: [string.replace("\t","•") for string in row])

## separating links from other words

for j in df.iterrows():
  list1=j[1]['paragraphs']
  for i in range(len(list1)):
    list1[i]=re.sub('https:',' https:',list1[i])
    list1[i]=re.sub('http:',' http:',list1[i])

del i,j,list1

## putting full stops in strings that are ending with links

for i in df.iterrows():
  j=i[1]['paragraphs'] 
  for k in range(len(j)):  
    x = j[k].split()  
    if x[-1].startswith('https://') or x[-1].startswith('http://'):  
      x[-1] = x[-1]+" "+"."  
    j[k] = ' '.join(i for i in x)

del x,j,k,i

## removing the strings with 3 or more than 3 full stops(for removing table of contents)

for i in df.iterrows():  
  temp = i[1]['paragraphs']  
  for j in range(0,len(temp)):
    if(re.search("(\.|\-){3,}",temp[j])):  
      temp[j] = ""

del i,j,temp

## removing heading with lesser length

for i in df.iterrows():
  list1=i[1]['paragraphs']
  for i in range(len(list1)):
    if len(list1[i])<=50 and not(list1[i].endswith(".")):
      list1[i]=""

del i,list1

## stripping the empty spaces in the strings 

# df['paragraphs']=df['paragraphs'].apply(lambda x: [string.strip() for string in x if (string != "" and string !=" " and string != "  ")])

"""## Model implementation"""
#change the path accordingly
pipeline = QAPipeline(reader='C:\\Users\\bhavesh.sanwal01\\Desktop\\New folder (2)\\distilbert_qa.joblib', max_df=1.0)
# Commented out IPython magic to ensure Python compatibility.
pipeline.fit_retriever(df=df)

"""## Predictions"""

my_wrap = textwrap.TextWrapper(width = 130)

query = "No of Customers who provided feedback in July2018 for CXPEE CPE"
print('\033[1m'+'Query: '+'\033[0m'+format(query))

query = re.sub("[\(\[].*?[\)\]]\s", "", query)

prediction = pipeline.predict(query)
pred=prediction[0]

best_title = prediction[0]['title']
# best_paras=df[df['title']==best_title]
for i in df.iterrows():
  if i[1]['title']==best_title:
    best_paras=i[1]['paragraphs']


## TITLE
print('\033[1m'+'Title of the document: '+'\033[0m'+format(pred.get('title')))

## SHORT ANSWER
print('\033[1m'+'Short Answer:'+'\033[0m')
wrap_list = my_wrap.wrap(text=pred.get('text'))

for line in wrap_list:
   print(line)

## PROBABILITY
print('\033[1m'+'Confidence score: '+'\033[0m'+format(pred.get('probability')))

para_summary=clean_pred(prediction,best_paras)

## CONTEXT PARAGRAPH
print('\033[1m'+'Context:'+'\033[0m'+'\033[0m')

wrap_list = my_wrap.wrap(text=' '.join(trimmed_para(para_summary,pred)))
for line in wrap_list:
   print(line)

##SUMMARY
print('\033[1m'+'Summary:'+'\033[0m')

wrap_list = my_wrap.wrap(text=trimmed_summary(para_summary, trimmed_para(para_summary,pred)))
for line in wrap_list:
   print(line)

## EXTRACTIVE SUMMARY
print('\033[1m'+'Extractive Summary:'+'\033[0m')

wrap_list = my_wrap.wrap(text=' '.join(extractive_summary(para_summary, query)))
for line in wrap_list:
   print(line)











'''
#Sample Questions

List down the different file formats does Microsoft generates scan results?  
what is the percentage of total risks when the risk category is high?  
who is responsible for translating a website or service name to its IP address in Paas?  
what are the requirements of FedRAMP to update the SSP and related documents on an annual basis  
How many Pulse entries reviewed in Jan 2019 CXPEE CPE?  
which Act comes in Effect after ! january 2020 in california  
No of Customers who provided feedback in July2018 for CXPEE CPE  
Do you require multi-factor authentication and network address restrictions be used for any accounts with full or privileged access to manage systems (i.e., servers, operating systems, applications, databases, networking, storage, virtualization and security) that are used to provide cloud services  
'''
