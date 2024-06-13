from management_data.embeddings import model
from management_data.indexes import index
from management_data.load_csv import people_data
# Perform a similarity search
query = "What is Calvin Ramsey's job?"
query_embedding = model.encode([query])

D, I = index.search(query_embedding, 5)  # Get top 5 similar entries

# Print the results
for idx in I[0]:
    print(f"Content: {people_data['combined_text'].iloc[idx]}")