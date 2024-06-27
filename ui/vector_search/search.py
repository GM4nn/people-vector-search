import streamlit


def search(st: streamlit, column, query):
    
    st.session_state.query_search = query
    st.session_state.column = column
    st.session_state.page_v = 1

def search_with_field(st: streamlit, mongo_client):
    column_names = [
        'ean',
        'name',
        'description'
    ]

    option = st.selectbox("Choose the property", column_names, key='choose_property_v')

    query = st.text_input("Your query", key="query_v")

    button = st.button(
        "Search&nbsp;&nbsp;🔍",
        type="primary",
        use_container_width=True,
        key="search_v"
    )
    
    if button:
        search(st, option, query)
