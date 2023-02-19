from flask import Flask, jsonify
from utils import get_sources
from typing import Dict, Any, List
import time
from gtts import gTTS
from langchain.llms import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document
import requests
import os
import faiss
import pickle
from flask_cors import CORS
from playsound import playsound

app = Flask(__name__)
CORS(app)

with open("my_list.pkl", "rb") as f:
    documents: list[Document] = pickle.load(f)


@app.route("/")
def hello_world():
    thisDict = {}
    source_List = []
    page_list = []
    answers = {
        'output_text': " The punishment for taking drugs depends on the type of drug, the quantity, and the jurisdiction. For example, under the Defence Force Discipline Act 1982, the punishment for taking a prohibited drug other than cannabis is imprisonment for 2 years, and for taking cannabis the punishment for a defence member is a fine of the amount of the member's pay for 14 days for a first offence, and dismissal from the Defence Force for a second or later offence.\nSource: 88, 89, 60, 90"}
    source = get_sources(answers,documents)
    thisDict['answers'] = answers['output_text']
    for i in source:
        source_List.append(i.page_content)
        page_list.append(i.metadata['source'])
    thisDict['source'] = source_List
    thisDict['page'] = page_list
    tts = gTTS(thisDict['answers'], lang='en', tld='com.au')
    tts.save('hello.mp3')
    playsound('hello.mp3')
    return thisDict


answers = {
    'output_text': " The punishment for taking drugs depends on the type of drug, the quantity, and the jurisdiction. For example, under the Defence Force Discipline Act 1982, the punishment for taking a prohibited drug other than cannabis is imprisonment for 2 years, and for taking cannabis the punishment for a defence member is a fine of the amount of the member's pay for 14 days for a first offence, and dismissal from the Defence Force for a second or later offence.\nSource: 88, 89, 60, 90"}

if __name__ == "__main__":
    app.run(debug=True)