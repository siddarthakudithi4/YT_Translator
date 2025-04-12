# import os
# import re
# import streamlit as st
# from youtube_transcript_api import YouTubeTranscriptApi
# from agno.agent import Agent
# from agno.models.groq import Groq
# from google.cloud import texttospeech

# # ✅ Set API Keys and Google TTS Credentials
# os.environ["GROQ_API_KEY"] = "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"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "text_to_speech.json"

# # ✅ Initialize Translator Agent
# translator_agent = Agent(model=Groq(id="gemma2-9b-it"), markdown=True)

# # ✅ Extract Video ID
# def extract_video_id(video_url):
#     patterns = [r"v=([^&]+)", r"youtu\.be/([^?&]+)", r"embed/([^?&]+)"]
#     for pattern in patterns:
#         match = re.search(pattern, video_url)
#         if match:
#             return match.group(1)
#     return None

# # ✅ Get Transcript
# def get_video_transcript(video_url):
#     video_id = extract_video_id(video_url)
#     if not video_id:
#         return "❌ Invalid YouTube URL."
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         return " ".join([t["text"] for t in transcript])[:1500]
#     except Exception as e:
#         return f"❌ Error fetching transcript: {str(e)}"

# # ✅ Translate
# def translate_text(text, target_language):
#     prompt = f"Translate the following transcript into {target_language}:\n{text} and give the summary in 3 lines"
#     try:
#         response = translator_agent.run(prompt)
#         return response.content
#     except Exception as e:
#         return f"❌ Error translating text: {str(e)}"

# # ✅ Text to Speech
# def text_to_speech(text, output_file="output.wav"):
#     client = texttospeech.TextToSpeechClient()

#     synthesis_input = texttospeech.SynthesisInput(text=text)
#     voice = texttospeech.VoiceSelectionParams(
#         language_code="te-IN", name="te-IN-Chirp3-HD-Puck", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
#     )
#     audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

#     response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

#     with open(output_file, "wb") as out:
#         out.write(response.audio_content)

#     return output_file

# # ✅ Streamlit UI
# st.title("🎙️ YouTube Translator + Text-to-Speech (Telugu)")

# video_url = st.text_input("Enter YouTube video URL:")
# language = st.text_input("Translate to (e.g., Hindi, Telugu)", value="Telugu")

# if st.button("🔄 Process"):
#     with st.spinner("Fetching transcript..."):
#         transcript = get_video_transcript(video_url)
#     st.subheader("📝 Transcript")
#     st.write(transcript)

#     if "Error" not in transcript:
#         with st.spinner("Translating..."):
#             translation = translate_text(transcript, language)
#         st.subheader(f"🌍 Translated to {language}")
#         st.write(translation)

#         with st.spinner("Generating speech..."):
#             audio_path = text_to_speech(translation)
#             st.audio(audio_path, format="audio/wav")

import os
import re
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from agno.agent import Agent
from agno.models.groq import Groq
from google.cloud import texttospeech

# ✅ Set API keys and Google Cloud credentials
os.environ["GROQ_API_KEY"] = "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"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "text_to_speech.json"  # Make sure this file is in the project directory

# ✅ Initialize Groq-based translator agent
translator_agent = Agent(model=Groq(id="gemma2-9b-it"), markdown=True)

# ✅ Voice mapping dictionary for supported languages
VOICE_MAPPING = {
    "Telugu": {"language_code": "te-IN", "voice_name": "te-IN-Chirp3-HD-Puck"},
    "Hindi": {"language_code": "hi-IN", "voice_name": "hi-IN-Wavenet-D"},
    "English": {"language_code": "en-US", "voice_name": "en-US-Wavenet-D"},
    "Spanish": {"language_code": "es-ES", "voice_name": "es-ES-Wavenet-D"},
    "Tamil": {"language_code": "ta-IN", "voice_name": "ta-IN-Wavenet-A"},
    "Kannada": {"language_code": "kn-IN", "voice_name": "kn-IN-Wavenet-A"},
    "Gujarati": {"language_code": "gu-IN", "voice_name": "gu-IN-Wavenet-A"},
}

# ✅ Extract YouTube video ID
def extract_video_id(video_url):
    patterns = [r"v=([^&]+)", r"youtu\.be/([^?&]+)", r"embed/([^?&]+)"]
    for pattern in patterns:
        match = re.search(pattern, video_url)
        if match:
            return match.group(1)
    return None

# ✅ Fetch YouTube transcript
def get_video_transcript(video_url):
    video_id = extract_video_id(video_url)
    if not video_id:
        return "❌ Invalid YouTube URL."
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])[:1500]
    except Exception as e:
        return f"❌ Error fetching transcript: {str(e)}"

# ✅ Translate and summarize
def translate_text(text, target_language):
    prompt = f"""
You are a professional translator. First, translate the following transcript into {target_language}, maintaining the tone and meaning.
Then, provide a 3-line summary in the same language.

Transcript:
{text}
"""
    try:
        response = translator_agent.run(prompt)
        return response.content
    except Exception as e:
        return f"❌ Error translating text: {str(e)}"

# ✅ Convert text to speech (based on language selection)
def text_to_speech(text, language, output_file="output.wav"):
    if language not in VOICE_MAPPING:
        return f"❌ Voice for {language} not supported. Choose from: {', '.join(VOICE_MAPPING.keys())}"

    voice_params = VOICE_MAPPING[language]
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_params["language_code"],
        name=voice_params["voice_name"],
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    return output_file

# ✅ Streamlit UI
st.set_page_config(page_title="🎙️ YouTube Translator & TTS", layout="centered")
st.title("🎙️ YouTube Translator + Text-to-Speech")

video_url = st.text_input("📺 Enter YouTube video URL:")
language = st.selectbox("🌍 Translate and Convert To", list(VOICE_MAPPING.keys()))

if st.button("🔄 Translate & Speak"):
    with st.spinner("📥 Fetching transcript..."):
        transcript = get_video_transcript(video_url)
    st.subheader("📝 Transcript")
    st.write(transcript)

    if "Error" not in transcript:
        with st.spinner(f"🌐 Translating to {language}..."):
            translation = translate_text(transcript, language)
        st.subheader(f"🌍 Translated + Summary ({language})")
        st.write(translation)

        with st.spinner("🔊 Generating speech..."):
            audio_path = text_to_speech(translation, language)
            if "❌" not in audio_path:
                st.audio(audio_path, format="audio/wav")
                st.success("✅ Speech generated successfully!")
            else:
                st.error(audio_path)
