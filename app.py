import streamlit as st
import pandas as pd
import numpy as np
from utils import *


def show_result(summary):
    prob, label = summary.values()
    st.write('Sentiment prediction:', label)
    st.bar_chart(prob)


random_sentence = load_random_data()
st.title('Check the sentence sentiment')
st.caption("🚀 This project checks sentiment categories from your input sentences")
input_sentence = st.text_area('Your sentence')

if input_sentence:
    st.write_stream(stream_text(input_sentence))
    with st.spinner('Predict...'):
        summary = predict_model(input_sentence)
    show_result(summary)

if st.button("Random Sentence"):
    st.write_stream(stream_text(random_sentence))
    with st.spinner('Predict...'):
        summary = predict_model(input_sentence)
    show_result(summary)
