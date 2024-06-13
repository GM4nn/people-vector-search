from sentence_transformers import SentenceTransformer

from .load_csv import people_data

# Initialize the sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Generate embeddings for each row
embeddings = model.encode(people_data['combined_text'].tolist(), show_progress_bar=True)