# ANPR System Backend

## Description

The **Automatic Number Plate Recognition (ANPR) System** is a Python-based backend designed to automatically detect vehicles, locate their license plates, and recognize license plate numbers from images.

The system combines multiple computer vision and AI technologies. **YOLOv8** is used for vehicle detection, **Roboflow** is used for license plate detection, **OpenCV** is used for image processing and preprocessing, and **EasyOCR** is used to extract the characters from detected license plates.

The system is designed as a modular backend so that each stage of the ANPR process can be independently improved or replaced. Currently, the system processes images locally and generates annotated images, vehicle crops, plate crops, processed plate images, and JSON results. The backend is also structured to be integrated with **FastAPI**, allowing a frontend application to upload images and receive ANPR results through APIs.

### Main Capabilities

- Detect cars, motorcycles, buses, and trucks.
- Detect license plates inside detected vehicles.
- Crop and save detected vehicles and license plates.
- Apply multiple preprocessing techniques to improve OCR.
- Extract license plate characters using EasyOCR.
- Generate and compare multiple OCR candidates.
- Select the best OCR result using candidate scoring.
- Identify plates as readable or unreadable.
- Generate annotated output images.
- Process multiple images in a single batch.
- Save structured results in JSON format.
- Dynamically adjust visualization text size according to the vehicle bounding-box size.
- Ignore vehicles where no license plate is detected during visualization.

---

## Workflow

```text
                                                      Input Image
                                   │
                                   ▼
                       ┌─────────────────────┐
                       │  Vehicle Detection   │
                       │       YOLOv8         │
                       └──────────┬───────────┘
                                  │
                                  ▼
                            Vehicle Crop
                                  │
                                  ▼
                       ┌─────────────────────┐
                       │  Plate Detection     │
                       │      Roboflow        │
                       └──────────┬───────────┘
                                  │
                         Plate Detected?
                            ┌─────┴─────┐
                            │           │
                           NO          YES
                            │           │
                            ▼           ▼
                        Ignore       Plate Crop
                        Vehicle          │
                                         ▼
                              Image Preprocessing
                                         │
                       ┌─────────────────┼─────────────────┐
                       │                 │                 │
                    Resize          Grayscale           CLAHE
                       │                 │                 │
                       └─────────────────┼─────────────────┘
                                         │
                              Sharpening / OTSU /
                              Adaptive Threshold
                                         │
                                         ▼
                        Convert grayscale variants
                             back to 3-channel BGR
                        (required only for PaddleOCR)
                                         │
                                         ▼
                ╔════════════════════════════════════════╗
                ║           OCR ENGINE IN USE              ║
                ║                                          ║
                ║   ❌ EasyOCR   →  REPLACED, NOT USED     ║
                ║      (used in your OLD ocr.py — kept     ║
                ║       in the project as a fallback file  ║
                ║       only, not called by the pipeline)  ║
                ║                                          ║
                ║   ✅ PaddleOCR →  ACTIVE ENGINE           ║
                ║      (ocr_paddle.py — this is what       ║
                ║       pipeline.py now imports and runs)  ║
                ║      use_textline_orientation=False       ║
                ║      enable_mkldnn=False                 ║
                ╚════════════════════════════════════════╝
                                         │
                                         ▼
                          Run PaddleOCR on every variant
                        (resized, gray, clahe, sharpened,
                              otsu, adaptive)
                                         │
                                         ▼
                          Multiple OCR Candidates
                        (text + confidence per variant)
                                         │
                                         ▼
                              Candidate Scoring
                        (confidence + consistency +
                          frequency + length score)
                                         │
                                         ▼
                             Final Plate Number
                                         │
                          Confidence ≥ OCR_MIN_CONFIDENCE?
                            ┌────────────┴────────────┐
                            │                         │
                           YES                        NO
                            │                         │
                            ▼                         ▼
                        Readable                 Unreadable
                            │                         │
                            └────────────┬────────────┘
                                         ▼
                                  Visualization
                            (bounding box + plate label
                                  on output image)
                                         │
                                         ▼
                             JSON + Output Image
                        (vehicle_crop, plate_crop,
                          processed_plate, plate_text,
                             ocr_confidence, status)

```
## Reasons Why a Plate Can Be Marked as "Unreadable"

### Unreadable Plate Reason

A license plate is marked as **Unreadable** when the OCR system cannot reliably recognize the plate text. This occurs in either of the following cases:

- **No text detected:** OCR fails to extract any characters from the detected license plate.
- **Low OCR confidence:** OCR detects text, but the confidence score is **below 40%**, meaning the recognized text is not considered reliable.

Low OCR confidence can occur due to:
- Blurry or low-resolution plate images
- Small or distant license plates
- Poor lighting or excessive brightness
- Obstructed or partially visible plates
- Distorted or incorrectly cropped plates
- Unclear, damaged, or difficult-to-read characters


## Conclusion
 This ANPR backend provides a complete modular pipeline for detecting vehicles, detecting their license plates, preprocessing plate images, recognizing plate characters, and generating structured results.

The system is currently focused on image-based ANPR processing and backend development. Its modular architecture allows individual components such as the vehicle detector, plate detector, preprocessing methods, or OCR engine to be improved independently.                        