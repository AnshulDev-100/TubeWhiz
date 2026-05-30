import os
import streamlit as st
from dotenv import load_dotenv

from utils.model_loader import load_embedding_model, load_llm_clients, load_groq_transcriber
from core.downloader import download_audio
from core.splitter import split_audio
from core.transcriber import transcribe_and_summarize
from core.embedder import build_faiss_index
from chat.chatbot import chat_with_llm
from utils.cleanup import cleanup_files

load_dotenv()


def main():
    st.set_page_config(
        page_title="TubeWhiz - AI Learning Assistant",
        page_icon="🎓",
        layout="wide"
    )

    # ── Sidebar ───────────────────────────────────────────────────────────────
    with st.sidebar:
        st.title("🎓 TubeWhiz")
        st.markdown("##### Your AI-powered Educational Assistant")
        st.divider()

        st.markdown("**🔗 Enter a YouTube URL**")
        url = st.text_input("YouTube Link:", placeholder="Paste your video link here...")

        st.markdown("**🤖 Select LLM Provider**")
        provider = st.selectbox(
            "Summarization & Chat:",
            options=["groq", "openai", "gemini"],
            index=0,
            help="Groq = fastest free | OpenAI = best quality | Gemini = balanced"
        )

        st.markdown("**⚙️ Actions**")
        start_btn = st.button("🚀 Start Processing")
        cleanup_btn = st.button("🧹 Clear Temporary Files")

        st.divider()
        st.caption("💡 Transcription always uses Groq Whisper for speed. LLM provider only affects summarization and chat.")

    # ── Main Area ─────────────────────────────────────────────────────────────
    st.title("📚 TubeWhiz — Conversational Learning Bot")
    st.markdown("#### _Ask, Learn, and Explore educational content from YouTube effortlessly._")
    st.markdown("---")

    # Load API keys
    groq_key    = os.getenv("GROQ_API_KEY")
    openai_key  = os.getenv("OPENAI_API_KEY")
    gemini_key  = os.getenv("GOOGLE_API_KEY")

    if not groq_key:
        st.error("❌ GROQ_API_KEY not found — required for transcription. Please set it in .env")
        st.stop()

    if provider == "openai" and not openai_key:
        st.error("❌ OPENAI_API_KEY not found. Please set it in .env or choose a different provider.")
        st.stop()

    if provider == "gemini" and not gemini_key:
        st.error("❌ GOOGLE_API_KEY not found. Please set it in .env or choose a different provider.")
        st.stop()

    # Load models
    embedder         = load_embedding_model()
    llm_clients      = load_llm_clients(groq_key, openai_key, gemini_key)
    groq_transcriber = load_groq_transcriber(groq_key)
    llm_client       = llm_clients[provider]

    # ── Process Video ─────────────────────────────────────────────────────────
    if start_btn:
        if not url:
            st.warning("⚠️ Please enter a valid YouTube URL in the sidebar.")
        else:
            # Reset session on new video
            st.session_state.processed = False
            st.session_state.conversation_history = []

            with st.spinner("⬇️ Downloading audio..."):
                audio_path = download_audio(url)

            with st.spinner("🎧 Splitting audio into chunks..."):
                chunk_files = split_audio(audio_path)

            full_text, summary_text, text_chunks = transcribe_and_summarize(
                groq_transcriber, llm_client, provider, chunk_files
            )

            index = build_faiss_index(embedder, text_chunks)

            st.session_state.index        = index
            st.session_state.text_chunks  = text_chunks
            st.session_state.processed    = True
            st.session_state.provider     = provider

            st.success(f"✅ Video processed successfully using **{provider}**!")

            st.markdown("### 🧾 Video Summary")
            st.markdown(summary_text)
            st.markdown("---")

    # ── Chat Section ──────────────────────────────────────────────────────────
    if st.session_state.get("processed"):
        active_provider = st.session_state.get("provider", provider)
        st.markdown(f"### 💬 Chat with TubeWhiz `({active_provider})`")
        st.markdown("_Ask any question related to your video content below:_")
        chat_with_llm(
            llm_client,
            active_provider,
            embedder,
            st.session_state.index,
            st.session_state.text_chunks
        )

    # ── Cleanup ───────────────────────────────────────────────────────────────
    if cleanup_btn:
        cleanup_files()


if __name__ == "__main__":
    main()