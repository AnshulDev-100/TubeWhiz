import os
import streamlit as st
from core.summarizer import summarize_text


def transcribe_and_summarize(groq_transcriber, llm_client, provider: str, chunk_files: list[str]) -> tuple[str, str, list[str]]:
    """
    Transcribes each chunk via Groq Whisper API (near-instant),
    then summarizes using the selected LLM provider.

    Returns:
        full_transcription : str   — complete joined transcript
        summarized_text    : str   — per-chunk summaries joined
        text_chunks        : list  — individual chunk transcripts (for FAISS)
    """
    full_transcription = ""
    summaries = []
    text_chunks = []
    n = len(chunk_files)

    st.markdown("#### 🎙️ Transcription Progress")
    transcribe_progress = st.progress(0, text="Starting transcription...")

    for i, chunk_path in enumerate(chunk_files):
        transcribe_progress.progress(
            (i) / n,
            text=f"Transcribing chunk {i+1} of {n}..."
        )
        with open(chunk_path, "rb") as f:
            result = groq_transcriber.audio.transcriptions.create(
                file=(os.path.basename(chunk_path), f),
                model="whisper-large-v3-turbo",
                response_format="text"
            )
        chunk_text = result.strip() if isinstance(result, str) else result.text.strip()
        text_chunks.append(chunk_text)
        full_transcription += chunk_text + " "

    transcribe_progress.progress(1.0, text="✅ Transcription complete!")

    st.markdown("#### 📝 Summarization Progress")
    summarize_progress = st.progress(0, text="Starting summarization...")

    for i, chunk_text in enumerate(text_chunks):
        summarize_progress.progress(
            (i) / n,
            text=f"Summarizing chunk {i+1} of {n} using {provider}..."
        )
        chunk_summary = summarize_text(llm_client, provider, chunk_text)
        summaries.append(f"### ✳️ Summary — Chunk {i + 1}\n{chunk_summary}\n")

    summarize_progress.progress(1.0, text="✅ Summarization complete!")

    return full_transcription.strip(), "\n".join(summaries).strip(), text_chunks