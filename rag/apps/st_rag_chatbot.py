from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts.prompt import PromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chat_models import init_chat_model
import streamlit as st 
import os 
from langchain_core.messages import SystemMessage, HumanMessage , AIMessage


loader = PyPDFLoader(
    r"../docs/courses_offered.pdf",
    mode="page")

docs = loader.load()

# Split docs into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=100)

chunks = splitter.split_documents(docs)

# Embeddings model and LLM 
embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001")
llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")


folder_path = "./course_vectors"

if os.path.exists(folder_path):
    db = FAISS.load_local(folder_path, embeddings_model,
                          allow_dangerous_deserialization=True)
    print("Loaded FAISS index")
else:
    db = FAISS.from_documents(chunks, embeddings_model)
    print('Created FAISS index')
    db.save_local(folder_path)

prompt_template = """:
Consider the following context and give a short answer for the given question.
Context : {context}
Question:{question}
"""

def new_chat():
    print("Handling the button!")
    st.session_state.prompt = ""
    st.session_state.messages = []

prompt  = PromptTemplate.from_template(prompt_template)

retriever = db.as_retriever()

if 'messages' not in st.session_state:
    st.session_state.messages = [
        SystemMessage("You are an assistant that answers based on provided context. ")
    ]
   

st.title("Courses RAG Demo")
query = st.text_input("Enter your query :", key = "prompt" , autocomplete = 'false')
st.button("New Chat", on_click=new_chat)
   

if len(query) > 0:
    results = retriever.invoke(query)
    matching_docs_str = "\n".join([doc.page_content for doc in results])
    final_prompt = prompt.format(context=matching_docs_str, question=query)
    st.session_state.messages.append(HumanMessage(final_prompt))
    result =  llm.invoke(st.session_state.messages)
    st.write(result.content)
    st.session_state.messages.append(result)
    