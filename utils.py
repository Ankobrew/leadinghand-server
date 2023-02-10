import pickle
from typing import Dict, Any, List
from langchain.docstore.document import Document


def get_sources(answer: Dict[str, Any], docs: List[Document]) -> List[Document]:
    """Gets the source documents for an answer."""

    # Get sources for the answer
    source_keys = [s for s in answer["output_text"].split("SOURCES: ")[-1].split(", ")]

    source_docs = []
    for doc in docs:
        if doc.metadata["source"] in source_keys:
            source_docs.append(doc)

    return source_docs


with open("my_list.pkl", "rb") as f:
    documents: list[Document] = pickle.load(f)