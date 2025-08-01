from flask import Flask, request, jsonify, url_for, send_from_directory
import face_recognition
import base64, io, pickle, os, gzip
from PIL import Image
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows cross-origin requests from Netlify

# Load face encodings (compressed)
with gzip.open("encodings/faces.pkl.gz", "rb") as f:
    known_faces = pickle.load(f)

@app.route('/retrieve', methods=['POST'])
def retrieve_json():
    try:
        data = request.get_json()
        selfie_data = data['selfie'].split(',')[1]
        selfie_bytes = base64.b64decode(selfie_data)
        image = Image.open(io.BytesIO(selfie_bytes)).convert("RGB")
        arr = np.array(image)
        encodings = face_recognition.face_encodings(arr)
        if not encodings:
            return jsonify({"photos": []})
        selfie_encoding = encodings[0]
        matches = []
        for face_encoding, photo_path in known_faces:
            match = face_recognition.compare_faces([face_encoding], selfie_encoding, tolerance=0.5)
            if match[0]:
                matches.append(photo_path)
        # Remove duplicates and make URLs absolute
        matches = sorted(list(set(matches)))
        photo_urls = [
            url_for('get_photo', filename=fn, _external=True)
            for fn in matches
        ]
        return jsonify({"photos": photo_urls})
    except Exception as e:
        return jsonify({"photos": [], "error": str(e)}), 500

# Endpoint to serve matched photos (for absolute URL)
@app.route('/static/photos/<path:filename>')
def get_photo(filename):
    return send_from_directory('static/photos', filename)

@app.route('/')
def home():
    return "Backend for Event Photo Face Search — POST a selfie to /retrieve!"

if __name__ == "__main__":
    app.run(debug=True)
