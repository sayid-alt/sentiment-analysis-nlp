
import time
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import pandas as pd
import streamlit as st


def load_data():
    data = pd.read_csv('./data/sentiment_data.csv')
    return data


# load data
sentiment_df = load_data()


def stream_text(sentence):
    for word in sentence.split(' '):
        yield word + " "
        time.sleep(0.05)


def prediction_summary(prediction, labels_encoder):
    pred_idx = np.argmax(prediction)
    pred_label = labels_encoder[pred_idx]
    return {
        'prob': {
            'positive': prediction[0],
            'neutral': prediction[1],
            'negative': prediction[2]
        },
        'label': pred_label
    }


def load_random_data():
    random_idx = np.random.choice(range(len(sentiment_df)), size=1)[0]
    random_data = sentiment_df.iloc[random_idx]['sentiment']
    return random_data


def labels_encoder():
    y_train = sentiment_df['label']
    label_tokenizer = Tokenizer()
    label_tokenizer.fit_on_texts(y_train)
    label_index_word = label_tokenizer.index_word
    # start encoder label from 0
    labels_encoder = {key - 1: value for key,
                      value in label_index_word.items()}
    return labels_encoder


def predict_model(sentence):
    # ==== SET HYPERPARAMETERS ====
    # Vocabulary size of the tokenizer
    vocab_size = 10000
    # Maximum length of the padded sequences
    max_length = 50

    # load data for tokenize
    df_train = pd.read_csv('./data/X_train.csv')
    X_train = df_train['sentiment'].tolist()

    # tokenize
    tokenizer = Tokenizer(num_words=vocab_size, oov_token='<OOV>')
    tokenizer.fit_on_texts(X_train)

    # load model
    loaded_model = load_model('./model/model.h5')

    # input for prediction
    input_sequences = tokenizer.texts_to_sequences([sentence])
    padded_input = pad_sequences(
        input_sequences, maxlen=max_length, padding='post', truncating='post')
    prediction = loaded_model.predict(
        padded_input)  # show softmax probabiliites, shape(1,m)

    encoded_labels = labels_encoder()  # label encoder for classification
    summary = prediction_summary(prediction[0], encoded_labels)

    return summary
