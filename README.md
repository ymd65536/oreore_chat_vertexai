# オレオレChatVertexAIを作る

## SetUp

```bash
pip install chainlit==1.0.200
```

## quick-start

```bash
cd quick_start
chainlit run main.py
```

```bash
pip install langchain-google-vertexai==0.0.1.post1
```

## Upload data to GCS

```bash
PROJECT_ID=`gcloud config list --format 'value(core.project)'`
ME_EMBEDDING_DIR="$PROJECT_ID-me-bucket"
index="documents/samples"
json_file="sample.txt"
set -x && gsutil cp $json_file gs://$ME_EMBEDDING_DIR/$index/$json_file
```
