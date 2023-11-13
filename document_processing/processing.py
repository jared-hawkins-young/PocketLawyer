# processing.py

from langchain.document_loaders import OnlinePDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import pinecone
import os

# Initialize Pinecone
pinecone.init(api_key=os.getenv('PINECONE_API_KEY'), environment='gcp-starter')

# Setup 

def initialize_pinecone_index():
    loader = OnlinePDFLoader("https://www.govinfo.gov/content/pkg/USCODE-2011-title18/pdf/USCODE-2011-title18.pdf")
    data = loader.load()
    print(f'You have {len(data)} document(s) in your data')
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(data)
    
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
    index_name = 'lawyer'
    
    # Here we assume that Pinecone.from_texts is a valid method and that it returns something we can use later
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
    
    return docsearch

# Set up your index on import of this module
docsearch = initialize_pinecone_index()

# Running the QA chain
def run_qa_chain(query):
    llm = OpenAI(temperature=0, openai_api_key=os.getenv('OPENAI_API_KEY'))
    chain = load_qa_chain(llm, chain_type="stuff")  # Ensure 'stuff' is a valid chain_type
    docs = docsearch.similarity_search(query)
    answer = chain.run(input_documents=docs, question=query)
    return answer
