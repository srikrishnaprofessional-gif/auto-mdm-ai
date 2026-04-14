import chromadb
from datetime import datetime

client = chromadb.Client()
collection = client.get_or_create_collection(name="memory")

def store_memory(text):
    collection.add(
        documents=[text],
        ids=[str(hash(text + str(datetime.now())))]
    )

def query_memory(query):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return results.get("documents", [])