import streamlit as st

with open("markdown/about.md", "r") as f:
    st.markdown(f.read())
