import streamlit as st

image_file = st.file_uploader("Upload Image", type=['jpeg', 'png', 'jpeg'])
st.write('hello world')
