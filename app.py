import streamlit as st

st.set_page_config(page_title="Letterboxd Recommender", layout="wide")

st.title("Letterboxd Recommender")
st.write("Upload your Letterboxd data and get personalized movie recommendations.")

uploaded_file = st.file_uploader("Upload your Letterboxd CSV", type=["csv"])

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    st.write("Filename:", uploaded_file.name)