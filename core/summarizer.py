def summarize_text(client, provider: str, text: str) -> str:
    """
    Summarize transcript text using the selected provider.
    Supports: 'groq', 'openai', 'gemini'
    """
    prompt = f"Provide a detailed, clear summary of the following transcript:\n\n{text}"

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

    return "Summarization failed — unknown provider."