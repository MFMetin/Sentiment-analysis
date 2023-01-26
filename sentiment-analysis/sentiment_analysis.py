import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
import pandas as pd
import string
import re


def get_word_index(path: str):
    word_index = pd.read_csv(path)
    word_index = dict(zip(word_index.Words, word_index.Indexes))

    word_index["<PAD>"] = 0
    word_index["<START"] = 1
    word_index["<UNK>"] = 2
    word_index["<UNUSED>"] = 3

    return word_index

word_index = get_word_index("./word_indexes.csv")

def encode_sentiments(x):
    if x == 'positive':
        return 1
    else:
        return 0


def review_encoder(text):
    return [word_index[word] for word in text]


def get_model():
    try:
        model = keras.models.load_model("./model")
    except:
        imdb_reviews = pd.read_csv("./imdb_reviews.csv")
        test_reviews = pd.read_csv("./test_reviews.csv")

        train_data, train_labels = imdb_reviews['Reviews'], imdb_reviews['Sentiment']
        test_data, test_labels = test_reviews['Reviews'], test_reviews['Sentiment']

        train_data = train_data.apply(lambda review: review.split())
        test_data = test_data.apply(lambda review: review.split())

        train_data = train_data.apply(review_encoder)
        test_data = test_data.apply(review_encoder)

        train_labels = train_labels.apply(encode_sentiments)
        test_labels = test_labels.apply(encode_sentiments)

        train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=word_index["<PAD>"], padding='post',
                                                                maxlen=500)
        test_data = keras.preprocessing.sequence.pad_sequences(test_data, value=word_index["<PAD>"], padding='post',
                                                               maxlen=500)

        model = keras.Sequential([keras.layers.Embedding(10000, 16, input_length=500),
                                  keras.layers.GlobalAveragePooling1D(),
                                  keras.layers.Dense(16, activation='relu'),
                                  keras.layers.Dense(1, activation='sigmoid')])

        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        history = model.fit(train_data, train_labels, epochs=30, batch_size=512,
                            validation_data=(test_data, test_labels))

        loss, accuracy = model.evaluate(test_data, test_labels)

        model.save("./model")

    return model

def remove_punctuation(text):
  if(type(text)==float):
    return text
  ans=""  
  for i in text:     
    if i not in string.punctuation:
      ans+=i    
  return ans


def remove_words(text):
    df = pd.read_csv("./word_indexes.csv")
    temp_sentence = ""
    text = re.split("\s+", str(text))

    myWords = []
    for word in df.loc[:,'Words']:
        myWords.append(word)
    
    for word in text:
        for word2 in myWords:
            if word == str(word2):
                temp_sentence += word
                temp_sentence += " "
    return temp_sentence


def analyze(sentence: str):
    
    model = get_model()
    
    sentence = sentence.lower()
   
    sentence = remove_punctuation(sentence)

    sentence = remove_words(sentence)

    review_str = re.split("\s+", sentence)

    temp = []
    x = len(review_str)
    for i in range (x-1):
        temp.append(review_str[i])
    
    
    encoded_review = [review_encoder(temp)]

    user_review = keras.preprocessing.sequence.pad_sequences(encoded_review,
                                                             value=word_index["<PAD>"],
                                                             padding='post',
                                                             maxlen=500)

    prediction = model.predict(user_review)

    return(prediction > 0.5).astype("int32")


