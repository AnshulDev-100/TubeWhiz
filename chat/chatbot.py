import streamlit as st
from core.retriever import retrieve_relevant_chunks


def chat_with_llm(llm_client, provider: str, embedder, index, text_chunks: list[str]) -> None:
    """
    RAG-based chat using the selected LLM provider.
    Supports: 'groq', 'openai', 'gemini'
    """
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Render existing history
    for msg in st.session_state.conversation_history:
        if msg.startswith("User:"):
            st.chat_message("user").markdown(msg.replace("User:", "").strip())
        else:
            st.chat_message("assistant").markdown(msg.replace("Assistant:", "").strip())

    user_input = st.chat_input("Ask something about the video...")

    if user_input:
        st.chat_message("user").markdown(user_input)

        relevant_texts = retrieve_relevant_chunks(embedder, user_input, index, text_chunks)
        context = "\n".join(relevant_texts)
        history = "\n".join(st.session_state.conversation_history[-6:])

        prompt = f"""You are an educational assistant that answers questions strictly based on the given transcript.

INSTRUCTIONS:
- Use ONLY the information from the provided CONTEXT and CHAT HISTORY.
- Do NOT use any outside knowledge.
- If the answer cannot be found in the context, clearly say "I don't have enough information to answer that."

Context:
{context}

Chat History:
{history}

User: {user_input}
Assistant:"""

        with st.spinner(f"Thinking ({provider})..."):
            reply = _generate(llm_client, provider, prompt)

        st.chat_message("assistant").markdown(reply)
        st.session_state.conversation_history.append(f"User: {user_input}")
        st.session_state.conversation_history.append(f"Assistant: {reply}")


def _generate(client, provider: str, prompt: str) -> str:
    """Unified generation call across all providers."""
    if provider == "gemini":
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text.strip()

    elif provider == "openai":
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    elif provider == "groq":
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

    return "Generation failed — unknown provider."