import time
import faiss
from .embeddings import embeddings


d = embeddings.shape[1]
index = faiss.IndexFlatL2(d)
index.add(embeddings)

faiss.write_index(index, 'faiss_index')
index = faiss.read_index('faiss_index')
