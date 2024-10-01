# Airflow DAG for Uploading Docs to Vector Space

This project is an Airflow-based pipeline designed to automate the process of uploading documents from Google Cloud Storage (GCS) to a Pinecone Vector Store for vector-based semantic search and document retrieval. It uses LangChain for document processing, HuggingFace for generating embeddings, and Pinecone for storing the embeddings.

## Project Structure

```
airflow/
│
├── dags/
│   └── upload_docs.py                # DAG definition for document upload and processing
├── logs/                             # Airflow logs directory
│   ├── dag_processor_manager/
│   │   └── dag_processor_manager.log
│   └── scheduler/2024-02-22/
│       └── upload_docs.py.log
├── airflow.cfg                       # Airflow configuration file
├── airflow.db                        # Airflow metadata database (SQLite by default)
├── standalone_admin_password.txt     # Airflow admin password (for standalone mode)
├── webserver_config.py               # Airflow webserver configuration
├── .gitignore                        # Git ignore file
├── README.md                         # Project README
├── docker-compose.yaml               # Docker Compose setup for Airflow
├── Dockerfile                        # Dockerfile for setting up the Airflow environment
└── requirements.txt                  # Python dependencies
```

## Features

- **Google Cloud Storage Integration**: Uses a GCS sensor to detect file changes and trigger DAG runs.
- **Document Processing**: The DAG uses LangChain to load and split text documents into smaller chunks.
- **Vector Store**: Documents are transformed into embeddings using HuggingFace's model and uploaded to Pinecone for semantic search and retrieval.
- **Airflow Tasks**:
  - **Sensor Task**: Monitors GCS for new or updated files.
  - **Processing Task**: Reads the file, processes it, and uploads it to Pinecone.
  - **Bash Task**: A simple bash task that prints a message based on the DAG's runtime configuration.

## How it Works

1. **GCS Sensor**: The DAG uses `GoogleCloudStorageObjectUpdatedSensor` to monitor a specific file in a GCS bucket.
2. **Document Processing**: Once a new document is detected, it is processed using LangChain's `TextLoader` and `CharacterTextSplitter` to split it into smaller, manageable chunks.
3. **Embeddings**: The HuggingFace `thenlper/gte-large` model is used to generate embeddings for the document chunks.
4. **Pinecone Upload**: These embeddings are then uploaded to a specified Pinecone index and namespace.
5. **Logging**: The system logs success messages and task progress.

## Requirements

- **Airflow**: Version 2.0+
- **Google Cloud**: GCS credentials and bucket access
- **Pinecone**: An active Pinecone account and an index created
- **LangChain**: For document loading and text processing
- **HuggingFace**: For embedding generation
- **Docker**: Docker and Docker Compose to run Airflow in containers

## Setup Instructions

### Prerequisites

- Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
- Set up Google Cloud credentials to access your GCS bucket.
- Sign up for Pinecone and create an index.

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd airflow
   ```

2. **Set up Airflow with Docker Compose**:
   ```bash
   docker-compose up -d
   ```

3. **Configure GCS and Pinecone**:
   - Add your GCS bucket name and file name to `upload_docs.py`:
     ```python
     bucket='your-gcs-bucket'
     object='your-file-name.txt'
     ```
   - Update `.env` file with Pinecone API keys and index details.

4. **Install dependencies**:
   If not using Docker, install the dependencies using:
   ```bash
   pip install -r requirements.txt
   ```

5. **Trigger the DAG**:
   Once the Airflow webserver is up, access the UI at `http://localhost:8080` and trigger the `dag_conf` DAG.

### Docker Compose Commands

- **Start Airflow**:
  ```bash
  docker-compose up -d
  ```

- **Stop Airflow**:
  ```bash
  docker-compose down
  ```

### Configuration

- **Airflow Configuration**: Modify `airflow.cfg` as needed for custom setups.
- **Pinecone and HuggingFace**: Ensure your environment variables are properly set for Pinecone API keys and HuggingFace embeddings.

## DAG Configuration

- **DAG ID**: `dag_conf`
- **Schedule Interval**: This DAG runs manually (no set schedule).
- **Default Arguments**:
  - `owner`: airflow
  - `start_date`: UTC now
  - `retries`: 1
  - `retry_delay`: 5 minutes
