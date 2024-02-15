from pinecone import Pinecone
from pinecone_index import get_index
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

# Load API key from environment variables
load_dotenv()
api_key = os.getenv('PINECONE_API_KEY')

# Initialize Pinecone client
client = Pinecone(api_key=api_key)

# Read text data from file
with open('assets\service.txt', 'r') as fp:
    lines = fp.readlines()

# Initialize Sentence Transformer model
embeddings_model = SentenceTransformer('thenlper/gte-large')

# Generate embeddings for each line of text
embeddings = [embeddings_model.encode(line) for line in lines]

# Prepare vectors for Pinecone index
vectors = [{'id': str(i), 'values': embeddings[i], 'metadata': {'text': lines[i]}} for i in range(len(lines))]

# Create or update Pinecone index
index = get_index('index1')

try:
    index.upsert(
        vectors=vectors,
        namespace='service-namespace'
    )
    print('Success')
except Exception as e:
    print(e)