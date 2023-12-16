import streamlit as st
from googletrans import Translator
from gtts import gTTS
from tempfile import NamedTemporaryFile
from audio_recorder_streamlit import audio_recorder
import pygame
import speech_recognition as sr

# Function to play audio
def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def main():
    st.title("Speech-to-Text and Translation App")

    # Streamlit UI components
    input_mode = st.radio("Select Input Mode:", ("Text", "Audio"))

    # Define dest_lang with an empty string
    dest_lang = ""

    if input_mode == "Text":
        get_sentence = st.text_area("Enter the sentence to be translated:")

        # Dropdown for destination language selection
        dest_lang_options = {'en': 'English', 'hi': 'Hindi', 'gu': 'Gujarati', 'mr': 'Marathi', 'bn': 'Bengali', 'pa': 'Punjabi', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada', 'ml': 'Malayalam', 'ur': 'Urdu'}
        dest_lang = st.selectbox("Select destination language:", list(dest_lang_options.keys()), format_func=lambda x: dest_lang_options[x])

        if st.button("Translate and Play Audio"):
            try:
                # Translator method for translation
                translator = Translator()

                print("Phrase to be Translated: " + get_sentence)

                # Using translate() method to convert text
                text_to_translate = translator.translate(get_sentence, dest=dest_lang)

                # Storing the translated text
                text = text_to_translate.text
                st.write("Translated text: ", text)

                # Using gTTS to convert the translated text to speech
                tts = gTTS(text=text, lang=dest_lang, slow=False)
                audio_file_path = NamedTemporaryFile(delete=False, suffix=".mp3").name
                tts.save(audio_file_path)

                # Playing the generated audio
                play_audio(audio_file_path)

            except Exception as e:
                st.error("An error occurred: {}".format(e))

    elif input_mode == "Audio":
        audio_bytes = audio_recorder(pause_threshold=2.0, sample_rate=41_000)
        if audio_bytes:
            # st.audio(audio_bytes, format="audio/wav")

            # Save the audio file as output_audio.wav
            with open("output_audio.wav", "wb") as audio_file:
                audio_file.write(audio_bytes)

            # Use the saved audio file for translation and text-to-speech
            try:
                dest_lang_options = {'en': 'English', 'hi': 'Hindi', 'gu': 'Gujarati', 'mr': 'Marathi', 'bn': 'Bengali', 'pa': 'Punjabi', 'ta': 'Tamil', 'te': 'Telugu', 'kn': 'Kannada', 'ml': 'Malayalam', 'ur': 'Urdu'}
                dest_lang = st.selectbox("Select destination language:", list(dest_lang_options.keys()), format_func=lambda x: dest_lang_options[x])

                # Translator method for translation
                translator = Translator()

                # Recognize the speech in the saved audio file
                recognizer = sr.Recognizer()
                with sr.AudioFile("output_audio.wav") as source:
                    audio_data = recognizer.record(source)

                # Translate the recognized text
                text_to_translate = translator.translate(recognizer.recognize_google(audio_data), dest=dest_lang)
                if st.button("Translate and Play Audio"):
                    # Storing the translated text
                    text = text_to_translate.text
                    st.write("Translated text: ", text)

                    # Using gTTS to convert the translated text to speech
                    tts = gTTS(text=text, lang=dest_lang, slow=False)
                    translated_audio_file_path = NamedTemporaryFile(delete=False, suffix=".mp3").name
                    tts.save(translated_audio_file_path)

                    # Playing the translated audio
                    play_audio(translated_audio_file_path)

            except Exception as e:
                st.error("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()
