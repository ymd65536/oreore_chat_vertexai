from ai_config import config as config

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import GCSDirectoryLoader
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import MatchingEngine
from utils.matching_engine_utils import MatchingEngineUtils
from google.cloud import aiplatform

# インデックス作成
mengine = MatchingEngineUtils(
    config.PROJECT_ID,
    config.ME_REGION,
    config.ME_INDEX_NAME
)

index = mengine.create_index(
    embedding_gcs_uri=f"gs://{config.ME_EMBEDDING_DIR}/{config.index_folder_prefix}",
    dimensions=config.ME_DIMENSIONS,
    index_update_method="streaming",
    index_algorithm="tree-ah",
)
if index:
    print(index.name)

index_endpoint = mengine.deploy_index()
if index_endpoint:
    print(f"Index endpoint resource name: {index_endpoint.name}")
    print(
        f"Index endpoint public domain name: {index_endpoint.public_endpoint_domain_name}"
    )
    print("Deployed indexes on the index endpoint:")
    for d in index_endpoint.deployed_indexes:
        print(f"    {d.id}")

# GCS保存場所
doc_folder_prefix = config.doc_folder_prefix
index_folder_prefix = config.index_folder_prefix

# ドキュメントを読み込む
loader = GCSDirectoryLoader(
    project_name=config.PROJECT_ID,
    bucket=config.GCS_BUCKET_DOCS,
    prefix=doc_folder_prefix
)

documents = loader.load()

# テキスト分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=20,
    chunk_overlap=0,
    separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
)

split_documents = text_splitter.split_documents(documents)
texts = [doc.page_content for doc in split_documents]
metadatas = [
    [
        {"namespace": "source", "allow_list": [doc.metadata["source"]]},
        {"namespace": "document_name", "allow_list": [doc.metadata["document_name"]]},
        {"namespace": "chunk", "allow_list": [str(doc.metadata["chunk"])]},
    ]
    for doc in split_documents
]

ME_INDEX_ID, ME_INDEX_ENDPOINT_ID = mengine.get_index_and_endpoint()

aiplatform.init(project=config.PROJECT_ID, location=config.ME_REGION)
vector_store = MatchingEngine.from_components(
    embedding=VertexAIEmbeddings(model_name=config.MODEL_NAME),
    project_id=config.PROJECT_ID,
    region=config.ME_REGION,
    gcs_bucket_name=config.GCS_BUCKET_NAME,
    index_id=ME_INDEX_ID,
    endpoint_id=ME_INDEX_ENDPOINT_ID,
)

doc_ids = vector_store.add_texts(texts=texts, metadatas=metadatas)

similar_doc = doc_ids.similarity_search("国民の祝日とはなんですか？", k=2)[0]
print(similar_doc.page_content)

print("Create Database")
