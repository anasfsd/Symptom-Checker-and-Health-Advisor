# Import libraries
import streamlit as st
import os
from groq import Groq
import speech_recognition as sr
from gtts import gTTS
import tempfile
from pyngrok import ngrok

# Set the Groq API key
os.environ["GROQ_API_KEY"] = ""

# Initialize Groq Client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to process text input
def analyze_symptoms(symptoms):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": f"Analyze these symptoms and suggest possible causes: {symptoms}"}
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# Function for voice input handling
def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        return "Sorry, could not understand the audio."

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)
    return temp_file.name

# Streamlit UI
def app():
    st.title("Symptom Checker and Health Advisor")
    st.markdown("""
    This app helps you analyze symptoms and get health advice. 
    Enter symptoms via text or voice input, and receive potential causes and recommendations.
    """)

    # Input options
    input_mode = st.radio("Choose Input Method", ("Text", "Voice"))

    if input_mode == "Text":
        symptoms = st.text_area("Enter your symptoms:")
        if st.button("Analyze Symptoms"):
            if symptoms:
                response = analyze_symptoms(symptoms)
                st.subheader("AI Response")
                st.write(response)
            else:
                st.warning("Please enter symptoms.")

    elif input_mode == "Voice":
        uploaded_file = st.file_uploader("Upload an audio file with your symptoms (e.g., WAV format):")
        if uploaded_file is not None:
            st.audio(uploaded_file)
            transcribed_text = transcribe_audio(uploaded_file)
            st.subheader("Transcribed Symptoms")
            st.write(transcribed_text)
            if st.button("Analyze Symptoms"):
                response = analyze_symptoms(transcribed_text)
                st.subheader("AI Response")
                st.write(response)

    # Doctor recommendation
    st.markdown("### Doctor Recommendation")
    st.markdown("If symptoms persist, we recommend consulting a doctor.")

    # Text-to-Speech Output
    if st.button("Hear the AI's Advice"):
        advice = "Make sure to take the provided suggestions seriously and consult a healthcare professional if needed."
        audio_file = text_to_speech(advice)
        st.audio(audio_file)

