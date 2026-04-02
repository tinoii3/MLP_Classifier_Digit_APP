# Digit Writing Recognizer

**Digit Writing Recognizer** is a desktop app for drawing digits with the mouse and classifying them with a pretrained model (`MNIT_model.h5`). The GUI uses **PyQt5**, image preprocessing uses **OpenCV**, and inference runs in **NumPy** with weights loaded from the Keras HDF5 file via **h5py** (no TensorFlow required at runtime).

---

## Features

- **Drawing** — Draw digits on a black canvas with live feedback.
- **Image processing** — Finds the drawn region (bounding box) and resizes it to 28×28, matching the MNIST-style input.
- **Classification** — Uses the trained MLP in `MNIT_model.h5` to predict the digit.
- **On-canvas labels** — Shows the predicted class name in green near the stroke.
- **Clear canvas** — Resets the drawing and predictions.

---

## Project structure

```
digit-drawing-recognizer/
├── main.py                 # Application entry point
├── home_page.py            # Home / menu screen
├── writing_page.py         # Drawing canvas and prediction UI
├── guide_page.py           # Short usage guide
├── mnist_mlp_inference.py  # Loads Keras H5 weights and runs MLP inference in NumPy
├── main.spec               # PyInstaller settings for building a Windows .exe
├── MNIT_model.h5           # Trained Keras model weights
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── TRAIN_MLP_MNIT.ipynb    # Notebook used to train the MLP
└── dist/
    └── main.exe            # Built executable (after PyInstaller)
```

---

## Install dependencies and run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Or install packages manually:

```bash
pip install PyQt5 numpy opencv-python h5py
```

### 2. Run the app

```bash
python main.py
```

---

## Build a Windows executable

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build

```bash
pyinstaller --onefile --add-data "MNIT_model.h5;." main.py
```

Or use the provided spec file if you maintain `main.spec`:

```bash
pyinstaller main.spec
```

The executable is written under the `dist` folder in the project directory.

**Note:** The first launch of the `.exe` may take on the order of ~10 seconds while files unpack.
