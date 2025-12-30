# SketchHelper
# Sketch Generation & Layered Edge Detection Web App

This project is a Flask-based web application that converts uploaded images into **step-by-step sketch guides** using computer vision techniques. It is designed for artists, learners, and hobbyists who want to create pencil sketches or grid-based drawings from reference images.

The application generates:

* Multiple **edge-detection layers**
* A **shaded pencil sketch**
* A **grid overlay reference system** for accurate drawing

---

## Features

* Image upload via a simple web interface
* Automatic image resizing and padding (A4 resolution support)
* Layered edge detection using multiple Canny thresholds
* Pencil-style shaded sketch generation
* Grid-based drawing assistance (custom rows & columns)
* Clean and minimal Flask UI
* Supports JPG, PNG, and JPEG formats

---

## How It Works

1. User uploads an image through the browser.
2. The image is resized and padded to a fixed A4 resolution.
3. The system enhances contrast using CLAHE and applies bilateral filtering.
4. Multiple edge-detection layers are generated.
5. A shaded pencil sketch is created using dodge blending.
6. All outputs are displayed step-by-step on the web page.

---

## Technologies Used

* Python
* Flask
* OpenCV
* NumPy
* HTML (Jinja templates)

---

## Directory Structure

```
project-root/
│
├── app.py
├── static/
│   ├── uploads/
│   │   └── uploaded_images.jpg
│   │
│   ├── steps/
│   │   ├── layer1.jpg
│   │   ├── layer2.jpg
│   │   └── shaded.jpg
│
├── templates/
│   └── index.html
│
└── README.md
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sketch-generator.git
cd sketch-generator
```

### 2. Install Dependencies

```bash
pip install flask opencv-python numpy
```

### 3. Run the Application

```bash
python app.py
```

### 4. Open in Browser

```
http://127.0.0.1:5000/
```

---

## Usage Steps

1. Start the Flask application.
2. Upload an image (PNG/JPG/JPEG).
3. Enter grid rows and columns (optional).
4. Submit the image.
5. View generated outputs:

   * Edge Layer 1
   * Edge Layer 2
   * Shaded Sketch
6. Use the images as drawing or sketching references.

---

## Output Description

| Output File | Description                |
| ----------- | -------------------------- |
| layer1.jpg  | Strong edge outline        |
| layer2.jpg  | Medium-detail edge layer   |
| shaded.jpg  | Pencil-style shaded sketch |

---

## Use Cases

* Pencil sketch practice
* Grid drawing for beginners
* Art tutorials and teaching aids
* Portrait sketch preparation
* Educational drawing tools

---

## Limitations

* Works best with clear and well-lit images
* Complex backgrounds may introduce noise
* Not designed for real-time processing

---

## Future Enhancements

* Download all steps as a ZIP file
* Adjustable edge sensitivity controls
* Real-time grid overlay on output images
* Color sketch mode
* Mobile-responsive UI
* User authentication and history tracking

---

## Author

**Parth Lathiya**

---

