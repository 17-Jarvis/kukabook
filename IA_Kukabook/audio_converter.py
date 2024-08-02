from gtts import gTTS
import os

# Step 1: Convert Text to Speech and Save Audio Files
def save_audio(content, filename):
    tts = gTTS(text=content, lang='en-in', slow=False)
    tts.save(filename)

content = "Your text content here"
filename = "audio.mp3"
save_audio(content, filename)