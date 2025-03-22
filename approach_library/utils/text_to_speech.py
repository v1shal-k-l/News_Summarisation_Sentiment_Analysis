# Importing Libraries
from gtts import gTTS
from deep_translator import GoogleTranslator

# Function
def text_to_speech(text):
    """ Converts text into both English and Hindi speech using gTTS (Cloud-based TTS). """
    
    # Translate English content to Hindi
    translated_text = GoogleTranslator(source="en", target="hi").translate(text)

    # Generate Hindi Voice (Using gTTS)
    hindi_tts = gTTS(text=translated_text, lang="hi")
    hindi_file = "output_hindi.mp3"
    hindi_tts.save(hindi_file)

    return hindi_file
