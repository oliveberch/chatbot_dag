from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStorageObjectUpdatedSensor
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import logging

load_dotenv()

def process_and_upload_to_pinecone(**kwargs):
    print("Remotely received value of {} for key=message".format(kwargs['dag_run'].conf['file_name']))

    # Load text from GCS
    file_name = kwargs['dag_run'].conf['file_name']
    loader = TextLoader(file_name)
    pages = loader.load_and_split()

    # Split text into chunks
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=10)
    documents = text_splitter.split_documents(pages)

    # Initialize HuggingFace embeddings model
    embeddings_model = HuggingFaceEmbeddings(
        model_name="thenlper/gte-large",
        encode_kwargs={"normalize_embeddings": True},
    )

    # Upload embeddings to Pinecone
    index = "starter"
    namespace = 'documents'
    Pinecone.from_documents(documents, embeddings_model, index_name=index, namespace=namespace)

    # Log a message indicating successful upload
    logging.info("Document successfully uploaded to Pinecone.")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.utcnow(),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='dag_conf',
    default_args=default_args,
    description='uploading data into pinecone',
    schedule_interval=None,
)

with dag:
    gcs_sensor = GoogleCloudStorageObjectUpdatedSensor(
        task_id='gcs_sensor',
        bucket='bucket_name',
        object='file_name.txt',
        google_cloud_storage_conn_id='google_cloud_default',
        timeout=600,
    )

    process_and_upload_task = PythonOperator(
        task_id='process_and_upload_to_pinecone',
        python_callable=process_and_upload_to_pinecone,
        provide_context=True,
    )

    bash_task = BashOperator(
        task_id="bash_task",
        bash_command='echo "Here is the message: {{ dag_run.conf["message"] if dag_run else "" }}" ',
        dag=dag,
    )

    gcs_sensor >> process_and_upload_task
