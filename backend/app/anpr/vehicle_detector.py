from ultralytics import YOLO

from app.config import (
    VEHICLE_MODEL_PATH,
    VEHICLE_CLASSES,
    VEHICLE_CONFIDENCE,
    VEHICLE_IMAGE_SIZE,
)


class VehicleDetector:
    """
    Detects vehicles using YOLO.
    """

    def __init__(self):

        print(
            "Loading vehicle detection model..."
        )

        self.model = YOLO(
            str(VEHICLE_MODEL_PATH)
        )

        print(
            "Vehicle detection model loaded."
        )

    def detect(self, image):

        results = self.model.predict(
            source=image,
            conf=VEHICLE_CONFIDENCE,
            imgsz=VEHICLE_IMAGE_SIZE,
            classes=list(
                VEHICLE_CLASSES.keys()
            ),
            verbose=False,
        )

        result = results[0]

        vehicles = []

        height, width = image.shape[:2]

        for vehicle_id, box in enumerate(
            result.boxes,
            start=1,
        ):

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0],
            )

            confidence = float(
                box.conf[0]
            )

            class_id = int(
                box.cls[0]
            )

            class_name = VEHICLE_CLASSES.get(
                class_id,
                "unknown",
            )

            # Keep coordinates valid
            x1 = max(0, x1)
            y1 = max(0, y1)

            x2 = min(width, x2)
            y2 = min(height, y2)

            if x2 <= x1 or y2 <= y1:
                continue

            vehicle_crop = image[
                y1:y2,
                x1:x2
            ]

            vehicles.append(
                {
                    "vehicle_id": vehicle_id,

                    "vehicle_class": class_name,

                    "vehicle_confidence": confidence,

                    "bbox": [
                        x1,
                        y1,
                        x2,
                        y2,
                    ],

                    "crop": vehicle_crop,
                }
            )

        return vehicles