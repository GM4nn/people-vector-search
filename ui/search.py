from management_data.load_csv import people_data
import streamlit as st

def hgello():
    print("gello")

def search_with_field():
    st.selectbox("Choose the property", list(people_data.columns.values))

    st.text_input("Your query", key="name")

    st.button(
        "Search&nbsp;&nbsp;🔍",
        type="primary",
        on_click=hgello,
        use_container_width=True,
    )
