import math

from management_data.load_csv import people_data
from settings import settings
import pandas as pd

# Initialize connection.
# Uses st.cache_resource to only run once.

def get_data(
    st,
    mongo_client,
    limit: int = 3,
    offset: int = 0,
):
    
    if 'queries' not in st.session_state:
        st.session_state.queries = {}
    
    collection = mongo_client[settings.MONGO_DB]["people"]
    total = collection.count_documents(st.session_state.queries)
    items = collection.find(
        st.session_state.queries, 
        projection={
            "_id":0, 
            "first_name": 1,
            "last_name": 1,
            "gender": 1,
            "email":1,
            "phone": 1,
            'birth_date':1,
            "job_title": 1
        }
    ).limit(limit).skip(offset)
    items = list(items)
    return items, total

def table_from_people(st, mongo_client):

    if 'page' not in st.session_state:
        st.session_state.page = 1

    rows_per_page = 3
    start_row = (st.session_state.page - 1) * rows_per_page

    items, total = get_data(
        st=st,
        mongo_client=mongo_client,
        offset=start_row
    )
    total_pages = math.ceil(total / rows_per_page)

    def increment():
        st.session_state.page = st.session_state.page + 1 

    def decrement():
        st.session_state.page = st.session_state.page - 1 
        
    items_as_dt = pd.DataFrame(items)
    st.table(data=items_as_dt)

    column1, column2, column3 = st.columns(3)
    if st.session_state.page  > 0:
        column1.button("Anterior", on_click=decrement,use_container_width=True)

    column2.markdown(f"<center>Page {st.session_state.page} of {total_pages}</center>",unsafe_allow_html=True)

    if st.session_state.page  < (people_data.shape[0] - 1) // rows_per_page:
        column3.button("Siguiente", on_click=increment, use_container_width=True)
