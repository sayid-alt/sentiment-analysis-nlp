import streamlit as st
import time


def stream_text(sentence):
    for word in sentence.split(' '):
        yield word + " "
        time.sleep(0.05)


st.title('Check the sentence sentiment')
input_sentence = st.text_input('Your sentence')
st.write_stream(stream_text(input_sentence))
