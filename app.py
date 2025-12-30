import os
import uuid
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
STEP_FOLDER = os.path.join(BASE_DIR, 'static', 'steps')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STEP_FOLDER, exist_ok=True)

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

    # Use a white background for padding
    padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    return padded

def layered_edge_detection(image_path, output_dir, target_size):
    img = cv2.imread(image_path)
    padded_img = resize_and_pad(img, target_size)
    gray = cv2.cvtColor(padded_img, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    contrast = clahe.apply(gray)
    blur = cv2.bilateralFilter(contrast, 9, 75, 75)

    edges_low = cv2.Canny(blur, 30, 100)
    edges_med = cv2.Canny(blur, 10, 70)

    cv2.imwrite(os.path.join(output_dir, "layer1.jpg"), cv2.bitwise_not(edges_low))
    cv2.imwrite(os.path.join(output_dir, "layer2.jpg"), cv2.bitwise_not(edges_med))

def create_shaded_sketch(input_path, output_path, target_size):
    image = cv2.imread(input_path)
    padded_image = resize_and_pad(image, target_size)
    gray = cv2.cvtColor(padded_image, cv2.COLOR_BGR2GRAY)
    
    # Invert and blur
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (25, 25), sigmaX=0, sigmaY=0)

    # Perform dodge blend
    def dodge(front, back):
        result = cv2.divide(front, 255 - back, scale=256)
        return result

    sketch = dodge(gray, blurred)

    # Optional: increase contrast
    sketch = cv2.equalizeHist(sketch)

    cv2.imwrite(output_path, sketch)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        if file and allowed_file(file.filename):
            original_name = secure_filename(file.filename)
            unique_id = uuid.uuid4().hex
            base_filename = f"{unique_id}_{original_name}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], base_filename)
            file.save(filepath)

            # Get grid dimensions from form, with defaults
            grid_rows = int(request.form.get('grid_rows', 29))
            grid_cols = int(request.form.get('grid_cols', 21))

            # Set a fixed target size (e.g., A4 at 300 DPI)
            target_size = (2480, 3508)

            layered_edge_detection(filepath, STEP_FOLDER, target_size)

            shaded_path = os.path.join(STEP_FOLDER, "shaded.jpg")
            create_shaded_sketch(filepath, shaded_path, target_size)

            image_bases = ["layer1", "layer2", "shaded"]
            return render_template("index.html", images=image_bases, original_image=base_filename, rows=grid_rows, cols=grid_cols)

    return render_template("index.html", images=None, original_image=None)

if __name__ == "__main__":
    app.run(debug=True)