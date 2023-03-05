import os
from typing import List

from langchain.vectorstores import VectorStore
import faiss

from utils import get_sources, search_docs, get_answer
from langchain.docstore.document import Document
import pickle

os.environ["OPENAI_API_KEY"] = "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"

index = faiss.read_index("docs.index")

with open("faiss_store.pkl", "rb") as f:
    store: VectorStore = pickle.load(f)

store.index = index

with open("my_list.pkl", "rb") as f:
    documents: List[Document] = pickle.load(f)

def getAnswer(question: str):
    thisDict = {}
    source_List = []
    page_list = []
    sources = search_docs(store, question)
    answer = get_answer(sources, question)
    thisDict['answers'] = answer['output_text']
    for i in sources:
        source_List.append(i.page_content)
        page_list.append(i.metadata['source'])
    thisDict['source'] = source_List
    thisDict['page'] = page_list
    return thisDict


print(getAnswer("What is the punishment for treason"))