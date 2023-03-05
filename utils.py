import pickle
from typing import Dict, Any, List

from langchain import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS, VectorStore



def search_docs(index: VectorStore, query: str) -> List[Document]:
    """Searches a FAISS index for similar chunks to the query
    and returns a list of Documents."""

    # Search for similar chunks
    docs = index.similarity_search(query, k=5)
    return docs


def get_answer(docs: List[Document], query: str) -> Dict[str, Any]:
    """Gets an answer to a question from a list of Documents."""

    # Get the answer

    chain = load_qa_with_sources_chain(OpenAI(temperature=0, openai_api_key=""),
                                       chain_type="stuff")  # type: ignore

    # Cohere doesn't work very well as of now.
    # chain = load_qa_with_sources_chain(Cohere(temperature=0), chain_type="stuff", prompt=STUFF_PROMPT)  # type: ignore
    answer = chain(
        {"input_documents": docs, "question": query}, return_only_outputs=True
    )
    return answer


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


