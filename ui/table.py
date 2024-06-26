import math

from management_data.load_csv import people_data
import streamlit as st

def table_from_csv():

    rows_per_page = 3
    total_pages = math.ceil(people_data.shape[0] / rows_per_page)

    if 'page' not in st.session_state:
        st.session_state.page = 1

    def increment():
        st.session_state.page = st.session_state.page + 1 

    def decrement():
        st.session_state.page = st.session_state.page - 1 
        
    start_row = (st.session_state.page - 1) * rows_per_page
    end_row = start_row + rows_per_page

    st.table(data=people_data.iloc[start_row:end_row])

    column1, column2, column3 = st.columns(3)
    if st.session_state.page  > 0:
        column1.button("Anterior", on_click=decrement,use_container_width=True)

    column2.markdown(f"<center>Page {st.session_state.page} of {total_pages}</center>",unsafe_allow_html=True)

    if st.session_state.page  < (people_data.shape[0] - 1) // rows_per_page:
        column3.button("Siguiente", on_click=increment, use_container_width=True)
