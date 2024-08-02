import cv2
from pyzbar import pyzbar
import pygame
import os
import webbrowser
import gdown

def decode_qr_code(frame):
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        return obj.data.decode('utf-8')
    return None

def download_audio_from_drive(url):
    audio_file = 'temp_audio.mp3'
    
    # Extract file ID from URL
    try:
        file_id = url.split('/d/')[1].split('/')[0]
        gdown_url = f'https://drive.google.com/uc?id={file_id}'
    except IndexError:
        print("Error: URL does not contain a valid Google Drive file ID.")
        return None
    
    gdown.download(gdown_url, audio_file, quiet=False)
    
    return audio_file

def play_audio(audio_file):
    if audio_file is None:
        print("Error: No audio file to play.")
        return
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()
    os.remove(audio_file)

def enhance_image(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    enhanced = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return enhanced

def main():
    cap = cv2.VideoCapture(1)  # Use 0 for the default camera
    print("Scanning for QR code. Please show the QR code to the camera.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        enhanced_frame = enhance_image(frame)
        
        qr_code_url = decode_qr_code(enhanced_frame)
        if qr_code_url:
            print(f"QR Code detected: {qr_code_url}")
            webbrowser.open(qr_code_url)
            
            
            break
        
        cv2.imshow("QR Code Scanner", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
