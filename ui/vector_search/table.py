import math

import streamlit

from management_data.load_csv import people_data
from settings import settings
import pandas as pd
from management_data.embeddings import model

# Initialize connection.
# Uses st.cache_resource to only run once.


def get_data(
    st: streamlit,
    mongo_client,
    field: str = "name",
    limit: int = 10,
    offset: int = 0,
):

    collection = mongo_client[settings.MONGO_DB]["products"]

    if "query_search" not in st.session_state:
        st.session_state.query_search = ""

    if st.session_state.query_search == "":
        total = collection.count_documents({})
        items = (
            collection.find(
                {},
                projection={
                    "_id": 0,
                    "store": 1,
                    "name": 1,
                    "ean": 1,
                    "current_price": 1,
                    "promo_price": 1,
                },
            )
            .limit(limit)
            .skip(offset)
        )
        items = list(items)
        return items, total

    query_embedding = model.encode([st.session_state.query_search])[0].tolist()
    vector_index = f"vector_index_{field}_embedding"

    percentage = 0.50
    limit_of_vectors_data = 100
    pipeline = [
        {
            "$vectorSearch": {
                "index": vector_index,
                "queryVector": query_embedding,
                "path": f"{field}_embedding",
                "numCandidates": 500,
                "limit": limit_of_vectors_data,
            }
        },
        {
            "$addFields": {
                "similarity": {"$meta": "vectorSearchScore"},
            }
        },
        {"$match": {"similarity": {"$gt": percentage}}},
        {"$sort": {"position": 1, "similarity": -1, "score": -1, "category": 1}},
        {
            "$project": {
                "_id": 0,
                "ean": 1,
                "name": 1,
                "current_price": 1,
                "promo_price": 1,
                "current_price": 1,
                "store": 1,
                "score": {"$meta": "vectorSearchScore"},
            }
        },
        {
            "$skip": offset,
        },
        {
            "$limit": limit,
        },
    ]

    results = collection.aggregate(pipeline)
    results_list = list(results)
    return results_list, limit_of_vectors_data


def table_from_people(st: streamlit, mongo_client):

    if "page_v" not in st.session_state:
        st.session_state.page_v = 1

    rows_per_page = 3
    start_row = (st.session_state.page_v - 1) * rows_per_page

    items, total = get_data(st=st, mongo_client=mongo_client, offset=start_row)
    total_pages = math.ceil(total / rows_per_page)

    def increment():
        st.session_state.page_v = st.session_state.page_v + 1

    def decrement():
        st.session_state.page_v = st.session_state.page_v - 1

    items_as_dt = pd.DataFrame(items)
    st.table(data=items_as_dt)

    column1, column2, column3 = st.columns(3)
    if st.session_state.page_v > 0:
        column1.button(
            "Anterior", on_click=decrement, use_container_width=True, key="prev_v"
        )

    column2.markdown(
        f"<center>Page {st.session_state.page_v} of {total_pages}</center>",
        unsafe_allow_html=True,
    )

    if st.session_state.page_v < (people_data.shape[0] - 1) // rows_per_page:
        column3.button(
            "Siguiente", on_click=increment, use_container_width=True, key="next_v"
        )
