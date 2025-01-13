import streamlit as st
import pandas as pd
import numpy as np
import tempfile
import requests
import time

st.title('mindbrain')

url = "http://0.0.0.0:8000/transcribe" # временный айпи, как только сервак дадут - исправим на нормальный.



f = st.audio_input("Записать аудио:")

    
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("или:")
uploaded_file = st.file_uploader("Загрузить аудио:", type=['mp3','wav'])



def load_data(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    response = requests.post(url,files={"file": bytes_data})
    jsonResponse = response.json()
    return jsonResponse["transcription"]



if st.button('Отправить'):
    if f is not None:
        with st.spinner('Загрузка...'):
            textfin = load_data(f) # не тестировалось на голосовых
        st.text(textfin)
    if uploaded_file is not None:
        with st.spinner('Загрузка...'):
            textfin = load_data(uploaded_file)
        st.text(textfin)
