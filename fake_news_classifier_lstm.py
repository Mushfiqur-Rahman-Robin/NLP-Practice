# -*- coding: utf-8 -*-
"""fake_news_classifier_lstm.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SxnGT0eYGAzgl-iKqWGNnXahp1ihwHAg
"""

from google.colab import files
files.upload()

# Let's make sure the kaggle.json file is present.
!ls -lha kaggle.json

!pip install -q kaggle

# The Kaggle API client expects this file to be in ~/.kaggle,
# so move it there.
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/

# This permissions change avoids a warning on Kaggle tool startup.
!chmod 600 ~/.kaggle/kaggle.json

!pip install kaggle==1.5.6

!kaggle competitions download -c fake-news

!unzip fake-news.zip -d FakeNews

import pandas as pd
df = pd.read_csv('/content/FakeNews/train.csv')
df.head()

df.count()

df.isnull().sum()

df = df.dropna()
df.shape

df = df.drop('id', axis=1)
df.head()

news = df.copy()
news.head(10)

news.reset_index(inplace=True)
news.head(10)

## Get the Independent Features

Z=df.drop('label',axis=1)
Z.shape

X = df.iloc[ : , 0:3]
X.head()

X.shape

y = df.iloc[:, 3]
y

y.shape

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords
import re
from nltk.stem.porter import PorterStemmer

corpus = []
ps = PorterStemmer()

for i in range(0, len(news)):
  check = re.sub('[^a-zA-Z]', ' ', news['title'][i])
  check = check.lower()
  check = check.split()
  check = [ps.stem(word) for word in check if not word in stopwords.words('english')]
  check = ' '.join(check)
  corpus.append(check)

corpus[1]

corpus

from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense

voc_size = 10000

onehot_repr = [one_hot(words,voc_size)for words in corpus] 
onehot_repr[0]

sent_length= 20
embedded_docs=pad_sequences(onehot_repr,padding='pre',maxlen=sent_length)
embedded_docs

embedded_docs[0]

embedding_features=40
model=Sequential()
model.add(Embedding(voc_size,embedding_features,input_length=sent_length))
model.add(LSTM(100))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
print(model.summary())

import numpy as np
X_final=np.array(embedded_docs)
y_final=np.array(y)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_final, y_final, test_size=0.33, random_state=42)

model.fit(X_train, y_train, validation_data= (X_test,y_test), epochs=10, batch_size=64)

from tensorflow.keras.layers import Dropout
embedding_vector_features= 100
model=Sequential()
model.add(Embedding(voc_size,embedding_vector_features,input_length=sent_length))
model.add(Dropout(0.3))
model.add(LSTM(100))
model.add(Dropout(0.3))
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])

model.fit(X_train, y_train, validation_data= (X_test,y_test), epochs=10, batch_size=64)

y_test

pred = model.predict(X_test)
pred

y_test.shape

pred.shape

pred = pred.flatten()
pred.shape

pred

pred = (pred > 9.00e-01).astype(int)
pred

from sklearn.metrics import confusion_matrix, classification_report
cm = confusion_matrix(y_test, pred)
cm

print(classification_report(y_test, pred))

from sklearn.metrics import accuracy_score
accuracy_score(y_test, pred)