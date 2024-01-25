import os

PROJECT_ID = os.getenv("PROJECT_ID")

# "asia-northeast1"
ME_REGION = os.getenv("ME_REGION")
ME_EMBEDDING_DIR = f"{PROJECT_ID}-me-bucket"
GCS_BUCKET_DOCS = f"{PROJECT_ID}-documents"
MODEL_NAME = "textembedding-gecko@001"

doc_folder_prefix = "documents/samples/"
index_folder_prefix = "index/db"

template = """
sample
"""

ME_INDEX_NAME = f"{PROJECT_ID}-me-sample"
ME_DIMENSIONS = 768  # when using Vertex PaLM Embedding