import os
from dotenv import load_dotenv
from langchain_unstructured import UnstructuredLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Load environment variables from .env if present
load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'contracts')
VECTORSTORE_DIR = os.path.join(os.path.dirname(__file__), '..', 'vectorstore', 'faiss_index')

os.makedirs(VECTORSTORE_DIR, exist_ok=True)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise EnvironmentError('OPENAI_API_KEY environment variable not set.')

# Load documents
def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.startswith('.'):
            continue
        path = os.path.join(directory, filename)
        print(f"Loading: {filename}")
        loader = UnstructuredLoader(path)
        documents.extend(loader.load())
    return documents

def main():
    print("Loading documents from:", DATA_DIR)
    docs = load_documents(DATA_DIR)
    print(f"Loaded {len(docs)} documents.")

    print("Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    split_docs = splitter.split_documents(docs)
    print(f"Split into {len(split_docs)} chunks.")

    print("Creating embeddings and vector store...")
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    print(f"Saving vector store to {VECTORSTORE_DIR} ...")
    vectorstore.save_local(VECTORSTORE_DIR)
    print("Export complete.")

if __name__ == "__main__":
    main() 