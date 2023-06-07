import requests
from bs4 import *
import pandas as pd
from fastapi import FastAPI
import numpy as np
#import pyspark.pandas
import seaborn as sns
#from pyspark.sql import SparkSession
#import spark
import matplotlib.pyplot as plt
#import pyarrow
import nltk
#from newspaper import Article, ArticleException
#%matplotlib inline
from wordcloud import WordCloud
import os
from spacy import displacy
import spacy
from textblob import TextBlob
from datetime import datetime,timedelta
from fastapi.middleware.cors import CORSMiddleware
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


nlp = spacy.load('en_core_web_sm')

origins = [
        "http://localhost:4200",
        "http://44.202.124.251:4200",
         "http://3.87.210.60:8000",
]
app = FastAPI()

app.add_middleware(
     CORSMiddleware,
     allow_origins=origins,
     allow_credentials=True,
     allow_methods=["*"],
     allow_headers=["*"],
)


def get_filename_by_date(date,hr=None):

    #hrs 24 format so 1-9 convert it double digit
    hours = ["0"+str(i) for i in range(10)] + [str(i) for i in range(10,24)]

    #GDELT side has generate 15 min interval file we diveded hrs 15 min interval
    min = ["0000","1500","3000","4500"]

    suffix = "export.CSV.zip"
    filenames = []
    if hr:
        for k in min:
            filenames.append(f"{date}{hr}{k}.{suffix}")
    else:
        for hr in hours:
            for k in min:
                filenames.append(f"{date}{hr}{k}.{suffix}")

    return filenames



def get_dates(date1, date2):
  """
  Get the dates in a week.

  Args:
    date1: .dd-mm-yyyy
    date2: dd-mm-yyyy.
    date1: The first date.
    date2: The last date.

  Returns:
    A list of dates.
  """

  # Get the start and end of the week.
  start_date = datetime.strptime(date1, '%d-%m-%Y')
  end_date = datetime.strptime(date2, '%d-%m-%Y')
  diff_date = end_date - start_date
  diff_days = diff_date.days

  # Get the days in the week.
  days = [start_date + timedelta(days=i) for i in range(diff_days+1)]

  # Return the list of dates.
  return [day.strftime("%Y%m%d") for day in days]


def download_gdelt_file(filename):

    url = "http://data.gdeltproject.org/gdeltv2/"

    # Create the download directory if it doesn't exist.
    if not os.path.exists("./gdelt"):
        os.mkdir("./gdelt")

    # Download the file.
    with requests.get(url + filename, stream=True) as response:
        response.raise_for_status()
        with open(f"./gdelt/{filename}", "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

def get_filename_between_dates(date1,date2):
    file_list = []
    date_list = get_dates(date1,date2)
    for date1 in date_list:
        file_ = get_filename_by_date(date1)
        file_list+=file_
    return file_list


def append_existing_file(df,csv_filename):
    df.to_csv(csv_filename,mode="a",index=False,header=False)
    return df

def filter_data(file_name):
    try:
        url = "http://data.gdeltproject.org/gdeltv2/" + file_name
        df = pd.read_csv(url, compression="zip", header=None, sep="\t")
    except:
        return pd.DataFrame()
     # Filter the data for events in India.
    df = df[df[53]=="IN"].reset_index(drop=True)
    return df

def get_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    text = soup.get_text()
    clean_text= text.replace("\n", " ")
    clean_text= clean_text.replace("\t", " ")
    clean_text= clean_text.replace("/", " ")
    clean_text= ''.join([c for c in clean_text if c != "'"])
    return clean_text


def find_Sentiment(val):
    if val<=0.1 and val>-0.1:
        return 'Neutral'
    elif val>0.1:
        return 'Positive'
    else:
        return 'Negative'

def newsAnalysis(clean_text):
    sent = []
    sentVal = []
    analysis = TextBlob(clean_text)
    sentiment = find_Sentiment(analysis.sentiment.polarity)
    qq = analysis.sentiment.polarity
    sentVal.append(qq)
    sent.append(sentiment)
    return sent, sentVal


@app.get("/filedata/{start_date}&{end_date}")
async def root(start_date,end_date):
                file_list = get_filename_between_dates(start_date,end_date)
                new_file = start_date+'_'+end_date+'.csv'
                for name in file_list:
                    df = filter_data(name)
                    if not df.empty:
                        print("saving file" + "->"+ name)
                        append_existing_file(df,new_file)
                df1=pd.read_csv(new_file,header=None)
                list_sentiment=[]
                list2 = []
                status= []
                url = df1[60][3]
                r = requests.get(url,verify=False)
                htmlcontent = r.content
                soup = BeautifulSoup(htmlcontent)
                text = soup.get_text()
                df = text.replace("\n", " ")
                textblob_sentiment=[]
                sentence=[]
                tokens = nlp(df)
                for sent in tokens.sents:
                    sentence.append((sent.text.strip()))
                person = None
                location = None
                for ent in tokens.ents:
                    if ent.label_ == "PERSON" and person is None:
                        person = ent.text
                    elif (ent.label_ == "GPE" or ent.label_ == "LOC") and location is None:
                        location = ent.text
                    if person is not None and location is not None:
                        break
                list2.append([person,location])
                for s in sentence:
                    txt= TextBlob(s)
                    a= txt.sentiment.polarity
                    b= txt.sentiment.subjectivity
                    textblob_sentiment.append([s,a,b])
                df_text = pd.DataFrame(textblob_sentiment,columns=['sentence','polarity','subjectivity'])
                mean_polarity = df_text['polarity'].mean()
                mean_subjectivity = df_text['subjectivity'].mean()
                if mean_polarity >0:
                    status.append('positive')
                elif mean_polarity <0:
                    status.append('negative')
                else:
                    status.append('Neutral')
                list_sentiment.append([mean_polarity,mean_subjectivity,person,location,status])
                return list_sentiment

