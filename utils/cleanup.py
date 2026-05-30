import os
import streamlit as st


def cleanup_files(audio_path: str = "./audio/audio_file.mp3", chunks_dir: str = "chunks") -> None:
    """Delete downloaded audio and chunk files; keep the folders."""
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)

        if os.path.exists(chunks_dir):
            for fname in os.listdir(chunks_dir):
                os.remove(os.path.join(chunks_dir, fname))

        st.success("🧹 Cleanup complete — temporary files removed.")
    except Exception as e:
        st.error(f"Cleanup error: {e}")