import sqlite3
import qrcode
from gtts import gTTS
import uuid
import os
import pygame

conn = None

def initialize():
    global conn
    print("Initializing database...")
    conn = sqlite3.connect('pages.db')
    
    
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pages
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       content TEXT,
                       key TEXT UNIQUE)''')
    conn.commit()
    print("Initialization complete.")

def store_content(content):
    global conn
    print("Storing content in database...")
    cursor = conn.cursor()
    
    key = str(uuid.uuid4())
    cursor.execute("INSERT INTO pages (content, key) VALUES (?, ?)", (content, key))
    conn.commit()
    print("Content stored successfully.")
    return key

def generate_qr_code(key, filename):
    print(f"Generating QR code: {filename}")
    qr = qrcode.QRCode(version=1, box_size=5, border=4)
    qr.add_data(key)

    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)
    print("QR code generated.")


def text_to_speech(text):
    print("Converting text to speech...")
    tts = gTTS(text=text, lang='en-in', slow=False)
    audio_file = "speech.mp3"
    tts.save(audio_file)

    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()
    os.remove(audio_file)
    print("Text-to-speech complete.")

def get_content_by_key(key):
    global conn
    print(f"Retrieving content for key: {key}")
    cursor = conn.cursor()
    
    cursor.execute("SELECT content FROM pages WHERE key = ?", (key,))
    result = cursor.fetchone()
    
    if result:
        print("Content retrieved successfully.")
        return result[0]
    else:
        print("Content not found.")
        return None

def process_file(file_path):
    print(f"Processing file: {file_path}")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r') as file:
        content = file.read()
    print(f"File content read. Length: {len(content)} characters")
    
    key = store_content(content)
    
    qr_filename = f"qr_{key}.png"
    generate_qr_code(key, qr_filename)
    
    print(f"Content stored with key: {key}")
    print(f"QR code generated: {qr_filename}")
    return key

def scan_qr_and_read(key):
    print(f"Simulating QR code scan for key: {key}")
    content = get_content_by_key(key)
    if content:
        print("Retrieved content:", content[:50] + "..." if len(content) > 50 else content)
        text_to_speech(content)
    else:
        print("Content not found")
        text_to_speech("Content not found")

def cleanup():
    global conn
    print("Cleaning up resources...")
    if conn:
        conn.close()
    print("Cleanup complete.")

if __name__ == "__main__":
    try:
        initialize()

        file_path = "/home/arq/Desktop/projects/IA_Kukabook/example.txt"
        print(f"File path entered: {file_path}")
        
        key = process_file(file_path)

        if key:
            print("\nSimulating QR code scan...")
            scan_qr_and_read(key)
        else:
            print("Failed to process the file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        cleanup()

print("Program execution complete.")
