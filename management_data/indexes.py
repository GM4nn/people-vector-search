import time
import faiss

from .transformer_embeddings import embedding_function
from .embeddings import embeddings


d = embeddings.shape[1]  # Dimension of embeddings
index = faiss.IndexFlatL2(d)
index.add(embeddings)

faiss.write_index(index, 'faiss_index')
index = faiss.read_index('faiss_index')
