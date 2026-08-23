import cv2

from inference_sdk import InferenceHTTPClient

from app.config import (
    settings,
    RESULTS_DIR,
)

class PlateDetector:
    """
    Detects license plates using Roboflow.
    """

    def __init__(self):

        print(
            "Initializing Roboflow plate detector..."
        )

        if not settings.ROBOFLOW_API_KEY:

            raise RuntimeError(
                "ROBOFLOW_API_KEY is missing "
                "from .env"
            )

        self.client = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key=settings.ROBOFLOW_API_KEY,
        )

        print(
            "Roboflow plate detector ready."
        )

    def detect(self, vehicle_crop):

        # Temporary image
        temp_path = (
            RESULTS_DIR / "_temp_vehicle.jpg"
        )

        success = cv2.imwrite(
            str(temp_path),
            vehicle_crop,
        )

        if not success:

            print(
                "Failed to create temporary "
                "vehicle image."
            )

            return None

        try:

            result = self.client.infer(
                str(temp_path),
                model_id=settings.PLATE_MODEL_ID,
            )

        except Exception as error:

            print(
                "Roboflow plate detection error:",
                error,
            )

            return None

        finally:

            if temp_path.exists():
                temp_path.unlink()

        predictions = result.get(
            "predictions",
            [],
        )

        if not predictions:
            return None

        # Select highest-confidence plate
        best_prediction = max(
            predictions,
            key=lambda prediction:
                prediction.get(
                    "confidence",
                    0,
                ),
        )

        return best_prediction


def crop_plate(
    vehicle_crop,
    prediction,
):
    """
    Crop detected plate from vehicle crop.
    """

    if prediction is None:
        return None, None

    x = prediction["x"]
    y = prediction["y"]

    w = prediction["width"]
    h = prediction["height"]

    # Convert center coordinates
    # to corner coordinates

    x1 = int(x - w / 2)
    y1 = int(y - h / 2)

    x2 = int(x + w / 2)
    y2 = int(y + h / 2)
    height, width = vehicle_crop.shape[:2]
    # Keep coordinates inside image
    x1 = max(0, x1)
    y1 = max(0, y1)

    x2 = min(width, x2)
    y2 = min(height, y2)

    if x2 <= x1 or y2 <= y1:

        return None, None

    plate_crop = vehicle_crop[
        y1:y2,
        x1:x2
    ]

    return (
        plate_crop,
        [
            x1,
            y1,
            x2,
            y2,
        ],
    )