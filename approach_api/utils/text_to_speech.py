# Importing Libraries
from gtts import gTTS
from deep_translator import GoogleTranslator

def text_to_speech(text):
    """ Converts text into both English and Hindi speech using gTTS (Cloud-based TTS). """
    
    # Translate English scraped Content to Hindi
    translated_text = GoogleTranslator(source="en", target="hi").translate(text)

    # Generating the Hindi Voice (Using gTTS)
    hindi_tts = gTTS(text=translated_text, lang="hi")
    hindi_file = "output_hindi.mp3"
    hindi_tts.save(hindi_file)

    return hindi_file
