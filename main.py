import streamlit as st
from ui.search import search_with_field
from ui.table import table_from_csv

st.set_page_config(layout="wide")
st.title("Mi streamlit")

search_with_field()
table_from_csv()