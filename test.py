from utils import get_sources
from langchain.docstore.document import Document
import pickle

with open("my_list.pkl", "rb") as f:
    documents: list[Document] = pickle.load(f)


thisDict = {}
source_List = []
answers = {
    'output_text': " The punishment for taking drugs depends on the type of drug, the quantity, and the jurisdiction. For example, under the Defence Force Discipline Act 1982, the punishment for taking a prohibited drug other than cannabis is imprisonment for 2 years, and for taking cannabis the punishment for a defence member is a fine of the amount of the member's pay for 14 days for a first offence, and dismissal from the Defence Force for a second or later offence.\nSource: 88, 89, 60, 90"}
source = get_sources(answers, documents)
thisDict['answers'] = answers['output_text']
for i in source:
    source_List.append(i.page_content)
    print(i.metadata['source'])
thisDict['source'] = source_List

print(thisDict)