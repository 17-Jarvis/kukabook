import qrcode
#audio_url = "https://drive.google.com/file/d/1FF2oj2b84_U2PmvCrmRG7RnfoU-Xyc77/view?usp=sharing"

# Step 2: Generate QR Code for the Audio URL
def generate_qr_code(url, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

qr_filename = "audio_qr.png"
#generate_qr_code(audio_url, qr_filename)

links = ["https://drive.google.com/file/d/1ZgyBMgAltSeLUzvWCrs3xc0RDF5BNfVA/view?usp=sharing"]
for i in range(len(links)):
    qr_filename = f"audio_file{[i]}.png"
    generate_qr_code(links[i], qr_filename)