from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
# BASE DIRECTORY
BASE_DIR = Path(__file__).resolve().parent.parent
# APPLICATION SETTINGS
class Settings:

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "ANPR System API",
    )

    APP_VERSION: str = os.getenv(
        "APP_VERSION",
        "1.0.0",
    )

    DEBUG: bool = os.getenv(
        "DEBUG",
        "false",
    ).lower() == "true"
    # Roboflow
    ROBOFLOW_API_KEY: str | None = os.getenv(
        "ROBOFLOW_API_KEY"
    )
    PLATE_MODEL_ID: str = (
        "license-plate-recognition-rxg4e/11"
    )
settings = Settings()
# DIRECTORIES
MODELS_DIR = BASE_DIR / "models"
UPLOADS_DIR = BASE_DIR / "uploads"
RESULTS_DIR = BASE_DIR / "results"
VEHICLE_CROPS_DIR = RESULTS_DIR / "vehicle_crops"
PLATE_CROPS_DIR = RESULTS_DIR / "plate_crops"
PROCESSED_PLATES_DIR = RESULTS_DIR / "processed_plates"
OUTPUT_IMAGES_DIR = RESULTS_DIR / "images"
JSON_RESULTS_DIR = RESULTS_DIR / "json"
# CREATE DIRECTORIES

for directory in [
    MODELS_DIR,
    UPLOADS_DIR,
    RESULTS_DIR,
    VEHICLE_CROPS_DIR,
    PLATE_CROPS_DIR,
    PROCESSED_PLATES_DIR,
    OUTPUT_IMAGES_DIR,
    JSON_RESULTS_DIR,
]:

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )
# MODEL

VEHICLE_MODEL_PATH = (
    MODELS_DIR / "yolov8n.pt"
)
# COCO CLASS IDS

VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}
# DETECTION SETTINGS
VEHICLE_CONFIDENCE = 0.25
VEHICLE_IMAGE_SIZE = 640
# OCR SETTINGS
OCR_LANGUAGE = ["en"]
OCR_MIN_CONFIDENCE = 40