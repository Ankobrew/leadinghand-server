from flask import Flask
from langchain.vectorstores import VectorStore

from utils import get_sources, search_docs, get_answer
from typing import Dict, Any, List
import time

from langchain.llms import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document
import requests
import os
import faiss
import pickle
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

os.environ["OPENAI_API_KEY"] = "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"

index = faiss.read_index("docs.index")

with open("faiss_store.pkl", "rb") as f:
    store: VectorStore = pickle.load(f)

store.index = index

with open("my_list.pkl", "rb") as f:
    documents: List[Document] = pickle.load(f)




@app.route("/")
def getAnswerTest():
    thisDict = {}
    source_List = []
    page_list = []
    answers = {
        'output_text': " The punishment for taking drugs depends on the type of drug, the quantity, and the jurisdiction. For example, under the Defence Force Discipline Act 1982, the punishment for taking a prohibited drug other than cannabis is imprisonment for 2 years, and for taking cannabis the punishment for a defence member is a fine of the amount of the member's pay for 14 days for a first offence, and dismissal from the Defence Force for a second or later offence.\nSource: 88, 89, 60, 90"}
    source = get_sources(answers, documents)
    thisDict['answers'] = answers['output_text']
    for i in source:
        source_List.append(i.page_content)
        page_list.append(i.metadata['source'])
    thisDict['source'] = source_List
    thisDict['page'] = page_list
    time.sleep(5)

    return thisDict


@app.route('/<question>')
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


if __name__ == "__main__":
    app.run(debug=True)
