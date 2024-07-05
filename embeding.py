from logging import error
from chromadb.api.models.Collection import Embedding
import ollama
import chromadb
from langchain_community.document_loaders import PyPDFDirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
import re
from sentence_transformers import SentenceTransformer

# model = SentenceTransformer("hkunlp/instructor-xl")


def create_db():
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.create_collection("data")


def get_embd(document):
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_or_create_collection("data")

    for i in document:
        id = i["id"]
        prompt = i["prompt"]
        responce = ollama.embeddings(model="mxbai-embed-large", prompt=prompt)
        embedding = responce["embedding"]
        # embedding = model.encode(prompt).tolist()
        collection.add(ids=[str(id)], embeddings=embedding)


def get_query(prompt):
    client = chromadb.HttpClient(host="localhost", port=8000)
    collecttion = client.get_collection("data")
    responce = ollama.embeddings(model="mxbai-embed-large", prompt=prompt)
    # embedding = model.encode(prompt).tolist()
    embedding = responce["embedding"]
    # embedding = query()
    results = collecttion.query(query_embeddings=embedding, n_results=5)
    return results["ids"][0]


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )

    return text_splitter.split_documents(documents)


def chunks_ids(chunks):
    current_chunk = 0
    data = []
    for i in chunks:
        source = i.metadata.get("source")
        ids = f"{source}:{current_chunk}"
        i.metadata["id"] = ids
        current_chunk += 1
        data.append({"prompt": i.page_content, "id": str(ids)})

    return data


def load_document(dir):
    try:
        document_loader = PyPDFLoader(dir)
        return document_loader.load_and_split(), False
    except Exception as e:
        return None, True


def process(dir):
    document, error = load_document(dir)
    if not error:
        chunks = split_documents(document)
        data = chunks_ids(chunks)
        get_embd(data)
        return error
    else:
        return error


def delete(exp):
    client = chromadb.HttpClient(host="localhost", port=8000)
    collection = client.get_or_create_collection("data")
    pattern = re.compile(re.escape(exp) + r".*")
    offset = 0
    while True:
        batch = collection.get(limit=1000, offset=offset)
        if not batch["ids"]:
            break

        match_doc = [doc for doc in batch["ids"] if pattern.search(doc)]

        if match_doc:
            match_ids = [doc for doc in match_doc]
            collection.delete(ids=match_ids)

        offset += 1000
