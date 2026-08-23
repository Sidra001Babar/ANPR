from pathlib import Path

import cv2

from app.anpr.vehicle_detector import (
    VehicleDetector,
)

from app.anpr.plate_detector import (
    PlateDetector,
    crop_plate,
)

from app.anpr.preprocessing import (
    preprocess_plate,
)

from app.anpr.ocr import (
    PlateOCR,
)

from app.anpr.visualizer import (
    overlay_vehicle_result,
)
from app.anpr.preprocessing import (
    preprocess_plate_variants,
)
from app.config import (
    VEHICLE_CROPS_DIR,
    PLATE_CROPS_DIR,
    PROCESSED_PLATES_DIR,
    OUTPUT_IMAGES_DIR,
)
from app.config import OCR_MIN_CONFIDENCE

class ANPRPipeline:
    def __init__(self):

        print("\nInitializing ANPR Pipeline...")

        # Load models once
        self.vehicle_detector = (
            VehicleDetector()
        )

        self.plate_detector = (
            PlateDetector()
        )

        self.ocr = PlateOCR()

        print(
            "ANPR Pipeline initialized."
        )
    # SAVE VEHICLE CROP
    def _save_vehicle_crop(
        self,
        crop,
        image_name,
        vehicle_id,
    ):
        base_name = Path(
            image_name
        ).stem

        filename = (
            f"{base_name}_"
            f"vehicle_{vehicle_id}.jpg"
        )
        path = (
            VEHICLE_CROPS_DIR
            / filename
        )
        cv2.imwrite(
            str(path),
            crop,
        )
        return str(path)

    # SAVE PLATE CROP
    def _save_plate_crop(
        self,
        crop,
        image_name,
        vehicle_id,
    ):
        base_name = Path(
            image_name
        ).stem
        filename = (
            f"{base_name}_"
            f"vehicle_{vehicle_id}_"
            f"plate.jpg"
        )
        path = (
            PLATE_CROPS_DIR
            / filename
        )
        cv2.imwrite(
            str(path),
            crop,
        )
        return str(path)

    # SAVE PROCESSED PLATE
    def _save_processed_plate(
        self,
        processed,
        image_name,
        vehicle_id,
    ):
        base_name = Path(
            image_name
        ).stem

        filename = (
            f"{base_name}_"
            f"vehicle_{vehicle_id}_"
            f"processed.jpg"
        )
        path = (
            PROCESSED_PLATES_DIR
            / filename
        )
        cv2.imwrite(
            str(path),
            processed,
        )
        return str(path)
    # PROCESS IMAGE
    def process_image(
        self,
        image_path,
    ):

        image_path = Path(
            image_path
        )

        image_name = (
            image_path.name
        )
        print(
            f"Processing: {image_name}"
        )

        # LOAD IMAGE
        image = cv2.imread(
            str(image_path)
        )

        if image is None:
            raise ValueError(
                f"Could not read image: "
                f"{image_path}"
            )
        output_image = image.copy()
        # STEP 1: VEHICLES
        print(
            "[1/6] Detecting vehicles..."
        )
        vehicles = (
            self.vehicle_detector.detect(
                image
            )
        )
        print(
            "Vehicles detected:",
            len(vehicles),
        )
        image_results = []
        # PROCESS EVERY VEHICLE
        for vehicle in vehicles:

            vehicle_id = (
                vehicle["vehicle_id"]
            )

            print(
                f"\nVehicle {vehicle_id}: "
                f"{vehicle['vehicle_class']}"
            )
            # SAVE VEHICLE CROP
            vehicle_path = (
                self._save_vehicle_crop(
                    vehicle["crop"],
                    image_name,
                    vehicle_id,
                )
            )
            # STEP 2: PLATE DETECTION
            print(
                "[2/6] Detecting plate..."
            )
            prediction = (
                self.plate_detector.detect(
                    vehicle["crop"]
                )
            )
            # NO PLATE
            if prediction is None:

                print(
                    "Plate not detected. "
                    "Ignoring vehicle."
                )

                continue
            # STEP 3: PLATE CROP
            print(
                "[3/6] Cropping plate..."
            )

            plate_crop, plate_bbox = (
                crop_plate(
                    vehicle["crop"],
                    prediction,
                )
            )

            if plate_crop is None:

                print(
                    "Invalid plate bounding box."
                )

                continue
            plate_path = (
                self._save_plate_crop(
                    plate_crop,
                    image_name,
                    vehicle_id,
                )
            )
            # STEP 4: PREPROCESSING
            print(
                "[4/6] Preprocessing plate..."
            )

            processed_variants = (
                preprocess_plate_variants(
                    plate_crop
                )
            )

            processed_plate = processed_variants[
                "sharpened"
            ]

            processed_path = (
                self._save_processed_plate(
                    processed_plate,
                    image_name,
                    vehicle_id,
                )
            )
            # STEP 5: OCR
            print(
                "[5/6] Extracting text..."
            )

            plate_text, ocr_confidence = (
                self.ocr.extract_text(
                    processed_variants
                )
            )

            if (
                not plate_text
                or ocr_confidence < 40
            ):

                plate_text = "Unreadable"

                status = "Unreadable"

                reason = (
                    "OCR confidence was too low."
                )

            else:

                status = "Readable"

                reason = None
            print(
                "Plate:",
                plate_text,
            )
            print(
                "OCR confidence:",
                round(
                    ocr_confidence,
                    2,
                ),
            )
            # STEP 6: VISUALIZATION
            overlay_vehicle_result(
                output_image,
                vehicle,
                plate_text,
            )
            # RECORD
            record = {
                "vehicle_id": vehicle_id,

                "vehicle_class": vehicle[
                    "vehicle_class"
                ],

                "vehicle_confidence": vehicle[
                    "vehicle_confidence"
                ],

                "vehicle_bbox": vehicle[
                    "bbox"
                ],

                "plate_detected": True,

                "plate_confidence": prediction.get(
                    "confidence",
                    0,
                ),

                "plate_bbox": plate_bbox,

                "vehicle_crop": vehicle_path,

                "plate_crop": plate_path,

                "processed_plate": processed_path,

                "plate_text": plate_text,

                "ocr_confidence": ocr_confidence,

                "status": status,

                "reason": reason,
            }

            image_results.append(
                record
            )

        # SAVE OUTPUT IMAGE
        output_filename = (
            image_path.stem
            + "_anpr.jpg"
        )
        output_path = (
            OUTPUT_IMAGES_DIR
            / output_filename
        )
        cv2.imwrite(
            str(output_path),
            output_image,
        )
        print(
            "\nOutput saved:",
            output_path,
        )
        # RETURN RESULT
        return {
            "image": image_name,
            "status": "Processed",
            "vehicles": image_results,
            "output_image": str(
                output_path
            ),
        }