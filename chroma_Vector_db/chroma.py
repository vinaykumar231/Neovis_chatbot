import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer

csv_path = r'D:\Neovis Chatbot\chroma_Vector_db\units_info.csv'
df = pd.read_csv(csv_path)
df['combined_info'] = df.apply(lambda row: ' '.join(row.fillna('').astype(str)), axis=1)

# Function to chunk text
def chunk_text(text, chunk_size=200, overlap=50):
    """Chunk text into smaller segments with overlap."""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

# Process and chunk the text data
chunked_texts = []
metadata = []
ids = []

for i, doc in enumerate(df['combined_info']):
    chunked = chunk_text(doc)
    chunked_texts.extend(chunked)
    metadata.extend([{'id': i}] * len(chunked))
    ids.extend([f"doc_{i}_{j}" for j in range(len(chunked))])

# Load sentence transformer model and encode texts
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunked_texts)

# Initialize ChromaDB client and collection
client = chromadb.Client()
collection_name = "chunked_text_data_collection"

def get_or_create_collection(client, collection_name):
    """Retrieve or create a ChromaDB collection."""
    try:
        return client.get_collection(name=collection_name)
    except chromadb.errors.InvalidCollectionException:
        return client.create_collection(name=collection_name)

collection = get_or_create_collection(client, collection_name)

# Add documents to ChromaDB in batches
batch_size = 5461
for start in range(0, len(chunked_texts), batch_size):
    end = min(start + batch_size, len(chunked_texts))
    collection.add(
        ids=ids[start:end],
        documents=chunked_texts[start:end],
        metadatas=metadata[start:end],
        embeddings=embeddings[start:end]
    )

print("Documents successfully added to ChromaDB!")
   