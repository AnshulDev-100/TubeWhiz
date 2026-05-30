import streamlit as st
from sentence_transformers import SentenceTransformer
from groq import Groq
from openai import OpenAI
from google import genai


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


def load_llm_clients(groq_key: str, openai_key: str, gemini_key: str) -> dict:
    """Returns all LLM clients. Each is optional — only loaded if key exists."""
    clients = {}
    if groq_key:
        clients["groq"] = Groq(api_key=groq_key)
    if openai_key:
        clients["openai"] = OpenAI(api_key=openai_key)
    if gemini_key:
        clients["gemini"] = genai.Client(api_key=gemini_key)
    return clients


def load_groq_transcriber(groq_key: str):
    """Separate client for Groq Whisper transcription."""
    return Groq(api_key=groq_key)