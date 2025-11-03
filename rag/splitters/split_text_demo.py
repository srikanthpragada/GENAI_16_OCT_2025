# Load document from Text File

from langchain_community.document_loaders.text import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load the text file
loader = TextLoader("./docs/mlk.txt")
# Load the documents
docs = loader.load()
print("Document Count : ", len(docs))
print("First Document Size : ", len(docs[0].page_content))

text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=100,
      chunk_overlap=20)

chunks = text_splitter.split_text(docs[0].page_content)

print('Chunks Count :', len(chunks))
