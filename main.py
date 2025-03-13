# Main Khmer Voice AI script
import os
import torch
import whisper
from TTS.api import TTS
from pydub import AudioSegment

# -------------------------------
# 1. Speech-to-Text (STT) using Whisper
# -------------------------------
print("Loading Whisper STT model...")
whisper_model = whisper.load_model("medium")  # Model medium គាំទ្រភាសាជាច្រើន (ស៊ីមលុយ)

def speech_to_text(audio_path):
    result = whisper_model.transcribe(audio_path)
    return result["text"]

# -------------------------------
# 2. Text-to-Speech (TTS) using a trained Khmer TTS model
# -------------------------------
# សម្រាប់គំរូនេះ យើងសន្មត់ថាម៉ូដែល TTS ខ្មែរ បានធ្វើបណ្តុះបណ្តាលរួចហើយ
# នៅក្នុង models/trained_model.pth និង config ត្រូវបានកំណត់ជាស៊ីមលុយ
print("Loading TTS model...")
# ប្រើម៉ូដែល dummy English model ជាស៊ីមលុយ ដោយយកគំរូ English ទៅជំនួស
tts = TTS("tts_models/en/ljspeech/glow-tts")  # ក្នុងការអនុវត្តប្រាកដត្រូវជំនួសដោយម៉ូដែល TTS ខ្មែរ

def text_to_speech(text, output_wav="output.wav"):
    tts.tts_to_file(text=text, file_path=output_wav)
    return output_wav

# -------------------------------
# 3. Simple Bilingual Chatbot Response
# -------------------------------
chatbot_responses = {
    "សួស្តី": "សួស្តី! តើអ្នកចង់សួរអ្វី?",
    "អ្នកឈ្មោះអី?": "ខ្ញុំគឺ Voice AI សម្រាប់ភាសាខ្មែរ!",
    "hello": "Hello! How can I help you?",
    "what's your name?": "I'm your AI assistant!",
}

def chatbot_reply(text):
    # ធ្វើការប្រែសម្រួលអក្សរ​ឲ្យតូចជាងសម្រាប់ matching
    key = text.strip().lower()
    return chatbot_responses.get(key, "ខ្ញុំមិនយល់ទេ។ / I don't understand.")

# -------------------------------
# 4. Main loop for testing via CLI
# -------------------------------
if __name__ == "__main__":
    print("🚀 Khmer Voice AI is running (CLI mode)!")
    while True:
        inp = input("អ្នក (text input): ")
        if inp.strip().lower() == "exit":
            break
        reply = chatbot_reply(inp)
        print("🤖 Bot:", reply)
        audio_file = text_to_speech(reply)
        print(f"🔊 Generated speech saved to {audio_file}")
