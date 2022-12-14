# -*- coding: utf-8 -*-
"""Fakenews.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bZdqqjym1OJDBERbjBjtDx7cRWgshN67

# Importing Depedencies
"""

import numpy as np
import pandas as pd
import re # regular expression v imp for searching the text in the document
from nltk.corpus import stopwords # stopwords are words like 'of','in','the' which are removed to focus on the rare and potentially relevant words
from nltk.stem.porter import PorterStemmer # algortihm used for removing suffix or prefix of words for root words
from sklearn.feature_extraction.text import TfidfVectorizer # to convert text to vectors or numbers
from sklearn.model_selection import train_test_split # split data into training and testing
from sklearn.linear_model import LogisticRegression #does stat math
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

"""# Pre-processing the data

"""

news_dataset = pd.read_csv('/content/train.csv')

news_dataset.shape

news_dataset.head()

# news_dataset.isnull().sum()  # checking if there are empty entires in the dataset
news_dataset = news_dataset.fillna("") #filling empty areas

news_dataset['content'] = news_dataset['author']+' '+news_dataset['title']

news_dataset['content']

X = news_dataset.drop(columns='label', axis=1)
Y = news_dataset['label']

print(Y)

"""#Stemming

"""

port_stem = PorterStemmer()

def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]',' ',content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if word not in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content

news_dataset['content'] = news_dataset["content"].apply(stemming)

print(news_dataset['content'])

nd = news_dataset #because im lazy

X = nd['content'].values
Y = nd['label'].values

vectorizer = TfidfVectorizer()
vectorizer.fit(X)
X = vectorizer.transform(X)

"""#**Splitting into test and train**

"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, stratify=Y, random_state=5) # stratify will seperate 0s and 1s equally

print(X_train)

"""# Training the model

"""

model = LogisticRegression()

model.fit(X_train, Y_train)

"""##Evaluation"""

X_train_prediction = model.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
print('Accuracy score of the training data : ', training_data_accuracy)

X_test_prediction = model.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
print('Accuracy score of the test data : ', test_data_accuracy)

"""# Predictive System

"""

X_new = X_test[78]

prediction = model.predict(X_new)
print(prediction)
if (prediction[0]==0):
  print('This is correct news')
else:
  print('This is fake news')