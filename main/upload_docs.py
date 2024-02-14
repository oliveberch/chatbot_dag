from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
PINECONE_API_KEY='67c15152-6c07-44d1-b3ba-d2886d18b1d5'
client = Pinecone(api_key=PINECONE_API_KEY)



fp=open('C:/Users/krant/OneDrive/Documents/revature p2 project/GenAI_chatbot/assets/service.txt','r')
l=fp.readlines()

embeddings_model = SentenceTransformer('thenlper/gte-large')

embeddings=[embeddings_model.encode(i) for i in l]





vectors=[]

for i in range(len(l)):
    vectors.append({
        'id':str(i),
        'values':embeddings[i],
        'metadata':{'text':l[i]}
    })






index=client.Index('index1')

try:
    index.upsert(
    vectors=vectors,
    namespace='service-namespace')
    print('success')
except Exception as e:

    print(e)