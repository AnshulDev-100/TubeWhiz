import os
import streamlit as st
from yt_dlp import YoutubeDL


def download_audio(youtube_url: str, output_file: str = "./audio/audio_file") -> str:
    os.makedirs("audio", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_file,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        duration = info.get("duration", None)
        mins = duration // 60 if duration else "Unknown"
        st.info(f"✅ Audio downloaded — Duration: {mins} minutes")

    return output_file + ".mp3"