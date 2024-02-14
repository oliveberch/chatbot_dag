from pinecone import Pinecone
import pinecone
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('PINECONE_API_KEY')
client = Pinecone(api_key=key)

index_name = 'index1'
def get_index(index_name:str):
    index = client.Index(index_name)
    return index