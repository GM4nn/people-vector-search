from pymongo import MongoClient
import streamlit as st

from ui.vector_search.search import search_with_field as search_with_field_vector
from ui.vector_search.table import table_from_people as table_from_people_vector
from ui.normal_search.search import search_with_field
from ui.normal_search.table import table_from_people
from settings import settings

# Set page config (only once)
st.set_page_config(layout="wide")

st.title("Searchs")

def init_connection():
    mongo_client = MongoClient(settings.MONGO_URI)
    return mongo_client

client = init_connection()

tab1, tab2, tab3 = st.tabs(
    [
        "Normal Search with people", 
        "Vector Search with products", 
        "Vector Search with PDF's"
    ]
)

with tab1:
    search_with_field(st, client)
    table_from_people(st, client)

with tab2:
    search_with_field_vector(st, client)
    table_from_people_vector(st, client)

with tab3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
