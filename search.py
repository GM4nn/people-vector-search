from management_data.embeddings import model
from management_data.indexes import index
from management_data.load_csv import people_data

# Perform a similarity search
query = "What is the date of James's Phillips birthday?"
query_embedding = model.encode([query])
model.encode([query])[0].tolist()
d, i = index.search(query_embedding, 5)  # Get top 5 similar entries

all_columns = list(people_data.columns.values)

if i.any():
    index = i[0][0]
    for column in all_columns:
        if column.startswith('people_'):
            continue
        print(f"Column {column}: value: {people_data[column].iloc[index]}")
else:
    print("Not found")


