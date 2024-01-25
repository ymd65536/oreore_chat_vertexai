from ai_config import config as config

from langchain.document_loaders import GCSDirectoryLoader
from langchain.embeddings import VertexAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import chroma

# GCS保存場所
doc_folder_prefix = config.doc_folder_prefix
index_folder_prefix = config.index_folder_prefix

# ドキュメントを読み込む
loader = GCSDirectoryLoader(
    project_name=config.PROJECT_ID,
    bucket=config.GCS_BUCKET_DOCS,
    prefix=doc_folder_prefix
)

# テキスト分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
)

split_documents = text_splitter.split_documents(loader)

# embeddingを初期化
embeddings = VertexAIEmbeddings(
    model="text-bison@001"
)

# Chromaを初期化
chroma_db = chroma(
    persist_directory=f"gs://{config.ME_EMBEDDING_DIR}/{index_folder_prefix}",
    embeddings_function=embeddings
)

# ドキュメントを追加する
chroma_db.add_documents(
    split_documents
)

print("Create Database")
