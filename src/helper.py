from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List
from langchain_core.documents import Document
from dotenv import load_dotenv
load_dotenv()
import os

#Extract Data From the PDF File
def load_pdf_file(data):
    documents = []
    for filename in os.listdir(data):
        if filename.endswith('.pdf'):
            file_path = os.path.join(data, filename)
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            
            documents.append(Document(
                page_content=text,
                metadata={"source": file_path}
            ))
    
    return documents



def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    """
    Given a list of Document objects, return a new list of Document objects
    containing only 'source' in metadata and the original page_content.
    """
    minimal_docs: List[Document] = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs



#Split the Data into Text Chunks
def text_split(extracted_data):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks




print("Initializing Google Embeddings...")
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    task_type="RETRIEVAL_DOCUMENT",
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)
print("Embeddings model loaded.")