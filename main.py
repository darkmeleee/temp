import streamlit as st
import pandas as pd
import numpy as np
import tempfile
import requests
import time

st.title('mindbrain')

url = "https://nw7u9kzbl.localto.net/transcribe" # временный айпи, как только сервак дадут - исправим на нормальный.
url2 = "https://nw7u9kzbl.localto.net/get_answer_mistral/"
url3 = "https://nw7u9kzbl.localto.net/synthesize_answer/"
url4 = "https://nw7u9kzbl.localto.net/get_emotion"




f = st.audio_input("Записать аудио:")

    
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("или:")
uploaded_file = st.file_uploader("Загрузить аудио:", type=['mp3','wav'])



def load_data(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    response = requests.post(url,headers={"localtonet-skip-warning": "true"},files={"file": bytes_data})
    jsonResponse = response.json()
    return jsonResponse["transcription"]

def load_answer(uploaded_text):
    response = requests.get(url2, headers={"localtonet-skip-warning": "true"}, params = {"question": uploaded_text})
    jsonResponse = response.json()
    print(jsonResponse)
    return jsonResponse["answer"]

def load_speech(text):
    response = requests.get(url3, headers={"localtonet-skip-warning": "true"}, params = {"text": text})
    audio_bytes = response.content
    print("------------")
    print(response)
    print(response.content)
    with open("debug_audio.wav", "wb") as f:
        f.write(audio_bytes)

    
    return audio_bytes

def load_emotion(uploaded_file):
    bytes_data = uploaded_file.getvalue()
    response = requests.post(url4,headers={"localtonet-skip-warning": "true"},files={"file": bytes_data})
    jsonResponse = response.json()
    return jsonResponse["client_emotion"]



if st.button('Отправить'):
    if f is not None:
        with st.spinner('Загрузка...'):
            textfin = load_data(f)
            emotion = load_emotion(f)
            st.write("Эмоция: злой")
            textfinally = load_answer(textfin)
            st.text(textfinally)
            audio = load_speech(textfinally)
            st.audio(audio, format="audio/wav", loop=False)

    if uploaded_file is not None:
        with st.spinner('Загрузка...'):
            textfin = load_data(uploaded_file)
            textfinally = load_answer(textfin)
        st.text(textfinally)
