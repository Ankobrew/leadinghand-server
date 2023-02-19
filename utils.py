import pickle
from typing import Dict, Any, List
from langchain.docstore.document import Document


def get_sources(answer: Dict[str, Any], docs: List[Document]) -> List[Document]:
    """Gets the source documents for an answer."""

    # Get sources for the answer
    reversed_text = answer['output_text'][::-1]
    source_index = reversed_text.find('ecruoS')

    # Extract the values after the "Source" string and reverse them back to their original order
    source_values = reversed_text[:source_index][::-1].strip()

    source_docs = []
    for doc in docs:
        if doc.metadata["source"] in source_values:
            source_docs.append(doc)

    return source_docs


with open("my_list.pkl", "rb") as f:
    documents: list[Document] = pickle.load(f)