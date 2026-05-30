import faiss
import streamlit as st


@st.cache_resource
def build_faiss_index(_embedder, text_chunks: list[str]):
    """
    Encodes text_chunks into embeddings and builds a FAISS L2 index.
    The leading underscore on _embedder prevents Streamlit from hashing it.
    """
    embeddings = _embedder.encode(text_chunks, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index