import re
import streamlit
from settings import settings

def search(st: streamlit, column, query):
    
    st.session_state.queries = {
        column: {"$regex": re.compile(re.escape(query), re.IGNORECASE)}
    }
    
    st.session_state.page = 1

def search_with_field(st: streamlit, mongo_client):
    collection = mongo_client[settings.MONGO_DB]["people"]
    document = collection.find_one()
    column_names = [
        key for key in list(document.keys())
        if not key.endswith('embedding') 
        and key != '_id'
        and key != 'products'
    ]

    option = st.selectbox("Choose the property", column_names)

    query = st.text_input("Your query", key="name")

    button = st.button(
        "Search&nbsp;&nbsp;🔍",
        type="primary",
        use_container_width=True,
    )
    
    if button:
        search(st, option, query)
