import streamlit as st
from apps import beng_app

st.set_page_config(page_title="BEng GPA", layout="wide")

beng_app.app()