# Telegram bot integration
# Bot telegram 
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pydub import AudioSegment
import whisper
from TTS.api import TTS

# -------------------------------
# Load models
# -------------------------------
print("Loading Whisper model for Telegram Bot...")
whisper_model = whisper.load_model("medium")

print("Loading TTS model for Telegram Bot...")
tts = TTS("tts_models/en/ljspeech/glow-tts")  # ស៊ីមលុយ, ប្ដូរជាមួយ TTS ខ្មែរ នៅពេលមាន

# Chatbot responses (ដូច main.py)
chatbot_responses = {
    "សួស្តី": "សួស្តី! តើអ្នកចង់សួរអ្វី?",
    "hello": "Hello! How can I help you?",
}

def speech_to_text(audio_path):
    result = whisper_model.transcribe(audio_path)
    return result["text"]

def text_to_speech(text, output_wav="output.wav"):
    tts.tts_to_file(text=text, file_path=output_wav)
    return output_wav

def chatbot_reply(text):
    key = text.strip().lower()
    return chatbot_responses.get(key, "ខ្ញុំមិនយល់ទេ។ / I don't understand.")

# -------------------------------
# Telegram Bot Handlers
# -------------------------------
TELEGRAM_BOT_TOKEN = "8105243416:AAHlq-Sdck3_Vrct8KMA4fiZOL2sBKS2Ib8"  # ជំនួស token របស់អ្នក

def start(update: Update, context: CallbackContext):
    update.message.reply_text("សួស្តី! សូមផ្ញើសំឡេងរបស់អ្នក។")

def voice_handler(update: Update, context: CallbackContext):
    voice = update.message.voice
    file = voice.get_file()
    file.download("voice.ogg")

    # បម្លែង OGG ទៅ WAV
    audio = AudioSegment.from_file("voice.ogg", format="ogg")
    audio.export("voice.wav", format="wav")

    text = speech_to_text("voice.wav")
    update.message.reply_text(f"អត្ថបទ៖ {text}")

    reply = chatbot_reply(text)
    output_file = text_to_speech(reply)
    update.message.reply_voice(voice=open(output_file, "rb"))
    update.message.reply_text(f"🤖 Bot: {reply}")

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
