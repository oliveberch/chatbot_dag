from pinecone import Pinecone
import os
from dotenv import load_dotenv
load_dotenv()

key = os.getenv('PINECONE_API_KEY')
client = Pinecone(api_key=key)

def get_index(index_name:str):
    index = client.Index(index_name)
    return index