# 🚘 ANPR — Automatic Number Plate Recognition System

An AI-powered **Automatic Number Plate Recognition (ANPR)** system that detects vehicles, identifies license plates, preprocesses plate images, and extracts license plate numbers using OCR.

The project currently supports **image-based ANPR through a FastAPI backend and React + TypeScript frontend**.

Video processing and live webcam detection are planned as the next development stages.

---

## ✨ Features

### Backend
- **Vehicle detection using YOLO:** Supports Car, Motorcycle, Bus, Truck
- **License plate detection:** High-accuracy detection via Roboflow
- **Plate processing pipeline:** Plate cropping, CLAHE enhancement, and multi-step OCR preprocessing
- **Text extraction:** EasyOCR with confidence score calculation
- **Classification:** Readable / Unreadable classification thresholding
- **Visualization:** Processed image annotation with bounding boxes and labels
- **API:** Asynchronous REST API powered by FastAPI

### Frontend
- **Modern Stack:** React + TypeScript + Vite + Tailwind CSS
- **Interactive UI:** Responsive dashboard with drag-and-drop file upload
- **Real-time Previews:** Original and processed image comparisons
- **Analytics & Breakdown:** Vehicle confidence, OCR confidence, and detection statistics
- **Extensible Layout:** Video and Live Webcam options prepared for future implementation

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │     React + TS       │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │
                               │ HTTP Request
                               │ Image Upload
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │        Backend       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    ANPR Pipeline     │
                    └──────────┬───────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
       YOLO Vehicle       Roboflow Plate      EasyOCR
        Detection          Detection           OCR
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │   Processed Image    │
                    │   + Detection Data   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     FastAPI JSON      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React Result UI     │
                    │                      │
                    │ • Processed Image    │
                    │ • Plate Number       │
                    │ • Confidence         │
                    │ • Statistics         │
                    └──────────────────────┘
                    

```
     

 ## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| **Backend** | Python, FastAPI, OpenCV, Ultralytics YOLO, Roboflow, EasyOCR, NumPy, python-dotenv |
| **Frontend** | React, TypeScript, Vite, Tailwind CSS, Axios, Lucide React |

---

## ⚙️ Installation & Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/macOS
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt     
```
## Frontend Run Setup (React + TypeScript)

Follow these steps to set up and run the frontend:

```bash
cd frontend
```
```bash
npm install
```
```bash
npm install axios lucide-react
```

```bash
npm run dev
```

---

#### 🌐 Access URL
- **Local Application:** `http://localhost:5173`

> **Note:** Ensure the backend (`FastAPI`) server is running at `http://127.0.0.1:8000` to handle API requests properly.

## Future Development
###  STEP 1: Image ANPR
      │
      ▼
COMPLETED ✅
```
STEP 2: Video Upload 🔄
      │
      ├── Video Frame Extraction
      ├── Frame-by-Frame ANPR
      └── Processed Video Generation

STEP 3: Live Webcam 🔄
      │
      ├── Real-Time Vehicle Detection
      ├── Real-Time Plate Detection
      └── Low-Latency Streaming OCR
```

🎥 Demonstration Video
A video demonstration of the Image ANPR functionality is available:

https://drive.google.com/file/d/1qbEMIJgddry-AA73vzLCvgNeo0n6p2Sg/view?usp=sharing

## 📜 Conclusion

This project delivers a robust, end-to-end image-based **Automatic Number Plate Recognition (ANPR)** system. By combining a **FastAPI** backend with a modern **React + TypeScript** frontend, it provides an intuitive interface for uploading images, visualizing detection boundaries, and analyzing confidence metrics in real time.

The modular architecture cleanly separates detection (YOLO), localization (Roboflow), and text extraction (EasyOCR), establishing a reliable foundation for the next development milestones: multi-frame **video processing** and low-latency **live webcam streams**.