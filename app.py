import os
import base64
import cv2
import numpy as np
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_and_pad(img, target_size):
    h, w = img.shape[:2]
    target_w, target_h = target_size
    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(img, (new_w, new_h))
    top = (target_h - new_h) // 2
    bottom = target_h - new_h - top
    left = (target_w - new_w) // 2
    right = target_w - new_w - left
    padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return padded

def get_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    return base64.b64encode(buffer).decode('utf-8')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        if file and allowed_file(file.filename):
            # Read image directly from memory
            filestr = file.read()
            npimg = np.frombuffer(filestr, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

            target_size = (2480, 3508)
            padded_img = resize_and_pad(img, target_size)
            gray = cv2.cvtColor(padded_img, cv2.COLOR_BGR2GRAY)

            # Processing
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            contrast = clahe.apply(gray)
            blur = cv2.bilateralFilter(contrast, 9, 75, 75)

            # Layers
            layer1 = cv2.bitwise_not(cv2.Canny(blur, 30, 100))
            layer2 = cv2.bitwise_not(cv2.Canny(blur, 10, 70))

            # Shaded Sketch
            inverted = cv2.bitwise_not(gray)
            blurred = cv2.GaussianBlur(inverted, (25, 25), 0)
            shaded = cv2.divide(gray, 255 - blurred, scale=256)
            shaded = cv2.equalizeHist(shaded)

            # Convert all to Base64 strings
            data = {
                "layer1": get_base64(layer1),
                "layer2": get_base64(layer2),
                "shaded": get_base64(shaded),
                "original": get_base64(padded_img)
            }

            grid_rows = int(request.form.get('grid_rows', 29))
            grid_cols = int(request.form.get('grid_cols', 21))

            return render_template("index.html", data=data, rows=grid_rows, cols=grid_cols)

    return render_template("index.html", data=None)

if __name__ == "__main__":
    app.run(debug=True)
