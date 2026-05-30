def retrieve_relevant_chunks(embedder, query: str, index, text_chunks: list[str], top_k: int = 3) -> list[str]:
    """
    Encodes the query and retrieves the top_k most semantically similar transcript chunks.
    """
    query_emb = embedder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_emb, top_k)
    return [text_chunks[i] for i in indices[0]]