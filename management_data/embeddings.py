from sentence_transformers import SentenceTransformer

from .load_csv import people_data

# Initialize the sentence transformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Generate embeddings for each row

text_to_embeddings = people_data['people_births_date'].tolist()
embeddings = model.encode(text_to_embeddings, show_progress_bar=True)