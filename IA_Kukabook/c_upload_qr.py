import qrcode
from gtts import gTTS
import os
import pygame

def generate_qr_code(url, filename):
    print(f"Generating QR code: {filename}")
    qr = qrcode.QRCode(version=1, box_size=5, border=4)
    qr.add_data(url)

    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print("QR code generated.")

def text_to_speech(text, speed=1.5):
    print("Converting text to speech...")
    tts = gTTS(text=text, lang='en-in', slow=False)
    audio_file = "speech.mp3"
    tts.save(audio_file)

    # Load the audio file with pydub
    audio = AudioSegment.from_file(audio_file)
    # Modify the speed
    new_audio = audio.speedup(playback_speed=speed)
    new_audio_file = "speed_speech.mp3"
    new_audio.export(new_audio_file, format="mp3")

    pygame.mixer.init()
    pygame.mixer.music.load(new_audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()
    os.remove(audio_file)
    os.remove(new_audio_file)
    print("Text-to-speech complete.")

if __name__ == "__main__":
    try:
        url = "https://drive.google.com/file/d/1FF2oj2b84_U2PmvCrmRG7RnfoU-Xyc77/view?usp=sharing"  # Replace with your file URL
        qr_filename = "qr_code.png"
        
        generate_qr_code(url, qr_filename)

        print(f"QR code generated: {qr_filename}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("Program execution complete.")
