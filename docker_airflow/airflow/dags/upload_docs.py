from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.transfers.gcs_to_local import GCSToLocalFilesystemOperator
from airflow.operators.python_operator import PythonOperator
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

import os
from dotenv import load_dotenv
load_dotenv()

# Define your DAG settings
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'gcs_to_pinecone',
    default_args=default_args,
    description='A DAG to transfer data from GCS to Pinecone',
    schedule_interval='@daily',  # Set your preferred schedule
)

# Define the function to upload data to Pinecone
def upload_to_pinecone(**kwargs):
    pinecone_index = os.getenv('PINECONE_INDEX')  # Replace with your Pinecone index name
    gcs_file_path = kwargs['ti'].xcom_pull(task_ids='download_from_gcs')['output_path']

    # Initialize Pinecone client
    pinecone = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))  # Replace with your Pinecone API key

    # Initialize Sentence Transformer model
    embeddings_model = SentenceTransformer('thenlper/gte-large')

    # Read text data from file
    with open(gcs_file_path, 'r') as fp:
        lines = fp.readlines()

    # Generate embeddings for each line of text
    embeddings = [embeddings_model.encode(line) for line in lines]

    # Prepare vectors for Pinecone index
    vectors = [{'id': str(i), 'values': embeddings[i], 'metadata': {'text': lines[i]}} for i in range(len(lines))]

    # Upload embeddings to Pinecone
    try:
        pinecone.upsert(
            vectors=vectors,
            namespace='service-namespace'
        )
        print('Success')
    except Exception as e:
        print(e)



# Define the tasks

# Task to download data from GCS
download_from_gcs_task = GCSToLocalFilesystemOperator(
    task_id='download_from_gcs',
    bucket_name='your_gcs_bucket',  # Replace with your GCS bucket name
    object_name='your_gcs_object',  # Replace with your GCS object name
    destination_path='/tmp/data',
    dag=dag,
)

# Task to upload data to Pinecone
upload_to_pinecone_task = PythonOperator(
    task_id='upload_to_pinecone',
    python_callable=upload_to_pinecone,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
download_from_gcs_task >> upload_to_pinecone_task