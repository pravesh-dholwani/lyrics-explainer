import streamlit as st
from llm_utils import driver

song_name = st.text_input("Song Name")
artist_name = st.text_input("Artist Name")
music_lang = st.text_input("Music Language")

if st.button("Explain"):
    explaination = driver(song_name, artist_name, music_lang)
    st.markdown(explaination)
