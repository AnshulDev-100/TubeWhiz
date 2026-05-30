import os
import streamlit as st
from pydub import AudioSegment


def split_audio(file_path: str, chunk_length_ms: int = 5 * 60 * 1000) -> list[str]:
    """Split audio into chunks of chunk_length_ms milliseconds (default: 5 min)."""
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    os.makedirs("chunks", exist_ok=True)
    chunk_files = []

    for i, chunk in enumerate(chunks):
        chunk_path = f"chunks/chunk_{i}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunk_files.append(chunk_path)

    st.info(f"🎧 Audio split into {len(chunk_files)} chunk(s).")
    return chunk_files