from cProfile import label
from .config import BEARER_TOKEN
import re
from transformers import AutoModelForSequenceClassification,AutoTokenizer
from scipy.special import softmax
import numpy as np
import urllib.request
import csv 

def getSentimentalAnalysis(tweets):
  

  try:
    task='sentiment'
    MODEL = f"cardiffnlp/twitter-roberta-base-{task}"

    tokenizer = AutoTokenizer.from_pretrained(MODEL)

    # download label mapping
    labels=[]
    mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
    with urllib.request.urlopen(mapping_link) as f:
        html = f.read().decode('utf-8').split("\n")
        csvreader = csv.reader(html, delimiter='\t')
    labels = [row[1] for row in csvreader if len(row) > 1]

# PT
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    model.save_pretrained(MODEL)
    tokenizer.save_pretrained(MODEL)
    sentiments = []
    if type(tweets) == list :
      for tweet in tweets:
        text = preprocess(tweet.text)
        encoded_input = tokenizer(text, return_tensors='pt')
        output = model(**encoded_input)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        ranking = np.argsort(scores)
        ranking = ranking[::-1]
        newSentiment = {
          'sentiment' : str(labels[ranking[0]]),
          'score' : float(scores[ranking[0]])
        }
        sentiments.append(newSentiment)
      return sentiments
    else :
      text = preprocess(tweets)
      encoded_input = tokenizer(text, return_tensors='pt')
      output = model(**encoded_input)
      scores = output[0][0].detach().numpy()
      scores = softmax(scores)
      ranking = np.argsort(scores)
      ranking = ranking[::-1]
      newSentiment = {
        'sentiment' : str(labels[ranking[0]]),
        'score' : round(float(scores[ranking[0]]),2)
      }
      return newSentiment['sentiment'],newSentiment['score']
  except Exception as e:
    print(str(e))

def preprocess(text):
    text = re.sub(r'RT[\s]\@[\w]+\:[\s]',"",text)
    text = re.sub(r'#',"",text)
    text = re.sub(r'\@[\w]+',"",text)
    text = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)',"",text)
    return text
    

if __name__ == "__main__":
  getSentimentalAnalysis()