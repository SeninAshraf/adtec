import face_recognition
import os
import pickle
import gzip
import numpy as np

PHOTO_DIR = "static/photos/"
ENCODING_FILE = "encodings/faces.pkl.gz"

os.makedirs("encodings", exist_ok=True)
all_encodings = []

for filename in os.listdir(PHOTO_DIR):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        img_path = os.path.join(PHOTO_DIR, filename)
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        for encoding in encodings:
            all_encodings.append((encoding.astype(np.float32), filename))

with gzip.open(ENCODING_FILE, "wb") as f:
    pickle.dump(all_encodings, f)

print(f"Processed {len(all_encodings)} face encodings (compressed)")
