from dotenv import load_dotenv
import os
from src.helper import load_pdf_file, filter_to_minimal_docs, text_split, embeddings
from pinecone import Pinecone
from pinecone import ServerlessSpec 
from langchain_pinecone import PineconeVectorStore
from tqdm import tqdm

# -------------------------
# API Keys (hardcoded here)
# -------------------------
PINECONE_API_KEY = "pcsk_2tXJEi_9oife2zxXQBKbPhqU9apc2M9Ai2h7Js8dMV4LyhKTHzVaebffuK38kEwN7BWeu7a"
GOOGLE_API_KEY = "AIzaSyCR6NXeebzPPbmMmFWVQAZlXRq-JLL77Gg"

# Set them into environment (so other libs can read)
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# -------------------------
# PDF Processing + Pinecone
# -------------------------
extracted_data = load_pdf_file(data='data/')
filter_data = filter_to_minimal_docs(extracted_data)
text_chunks = text_split(filter_data)

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"

if index_name not in pc.list_indexes().names():
    print(f"Creating index {index_name}...")
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

pinecone_index = pc.Index(index_name)

batch_size = 100
for i in tqdm(range(0, len(text_chunks), batch_size)):
    i_end = min(i + batch_size, len(text_chunks))
    batch = text_chunks[i:i_end]
    texts = [chunk.page_content for chunk in batch]
    metadatas = [chunk.metadata for chunk in batch]
    ids = [f"{index_name}-{i+j}" for j in range(len(batch))]
    embeds = embeddings.embed_documents(texts)
    vectors_to_upsert = list(zip(ids, embeds, metadatas))
    pinecone_index.upsert(vectors=vectors_to_upsert)
