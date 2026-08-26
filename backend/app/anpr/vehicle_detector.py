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

    Includes:
    1. YOLO class-agnostic NMS
    2. Additional IoU-based duplicate filtering
    3. Containment-based duplicate filtering

    Goal:
        One physical vehicle should produce
        only one vehicle detection.
    """

    # ----------------------------------------------------------
    # Duplicate detection thresholds
    # ----------------------------------------------------------

    DUPLICATE_IOU_THRESHOLD = 0.60

    DUPLICATE_OVERLAP_THRESHOLD = 0.80

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

    # ==========================================================
    # CALCULATE IOU
    # ==========================================================

    @staticmethod
    def calculate_iou(
        box_a,
        box_b,
    ):
        """
        Calculate Intersection over Union.

        Box format:
            [x1, y1, x2, y2]
        """

        ax1, ay1, ax2, ay2 = box_a
        bx1, by1, bx2, by2 = box_b

        # ------------------------------------------------------
        # Intersection coordinates
        # ------------------------------------------------------

        intersection_x1 = max(
            ax1,
            bx1,
        )

        intersection_y1 = max(
            ay1,
            by1,
        )

        intersection_x2 = min(
            ax2,
            bx2,
        )

        intersection_y2 = min(
            ay2,
            by2,
        )

        # ------------------------------------------------------
        # Intersection dimensions
        # ------------------------------------------------------

        intersection_width = max(
            0,
            intersection_x2
            - intersection_x1,
        )

        intersection_height = max(
            0,
            intersection_y2
            - intersection_y1,
        )

        intersection_area = (
            intersection_width
            * intersection_height
        )

        # ------------------------------------------------------
        # Individual areas
        # ------------------------------------------------------

        area_a = (
            max(
                0,
                ax2 - ax1,
            )
            *
            max(
                0,
                ay2 - ay1,
            )
        )

        area_b = (
            max(
                0,
                bx2 - bx1,
            )
            *
            max(
                0,
                by2 - by1,
            )
        )

        # ------------------------------------------------------
        # Union
        # ------------------------------------------------------

        union_area = (
            area_a
            + area_b
            - intersection_area
        )

        if union_area <= 0:
            return 0.0

        return (
            intersection_area
            / union_area
        )

    # ==========================================================
    # CALCULATE OVERLAP / CONTAINMENT
    # ==========================================================

    @staticmethod
    def calculate_overlap_ratio(
        box_a,
        box_b,
    ):
        """
        Calculates how much of the smaller bounding box
        is covered by the intersection.

        This catches cases where one duplicate box is
        mostly inside another box.

        Example:

            Large box:
            ┌───────────────────┐
            │                   │
            │   ┌───────────┐   │
            │   │ duplicate │   │
            │   │   box     │   │
            │   └───────────┘   │
            │                   │
            └───────────────────┘

        IoU may not always be high enough,
        but containment/overlap will be high.
        """

        ax1, ay1, ax2, ay2 = box_a
        bx1, by1, bx2, by2 = box_b

        # ------------------------------------------------------
        # Intersection
        # ------------------------------------------------------

        intersection_x1 = max(
            ax1,
            bx1,
        )

        intersection_y1 = max(
            ay1,
            by1,
        )

        intersection_x2 = min(
            ax2,
            bx2,
        )

        intersection_y2 = min(
            ay2,
            by2,
        )

        intersection_width = max(
            0,
            intersection_x2
            - intersection_x1,
        )

        intersection_height = max(
            0,
            intersection_y2
            - intersection_y1,
        )

        intersection_area = (
            intersection_width
            * intersection_height
        )

        # ------------------------------------------------------
        # Box areas
        # ------------------------------------------------------

        area_a = (
            max(
                0,
                ax2 - ax1,
            )
            *
            max(
                0,
                ay2 - ay1,
            )
        )

        area_b = (
            max(
                0,
                bx2 - bx1,
            )
            *
            max(
                0,
                by2 - by1,
            )
        )

        smaller_area = min(
            area_a,
            area_b,
        )

        if smaller_area <= 0:
            return 0.0

        return (
            intersection_area
            / smaller_area
        )

    # ==========================================================
    # REMOVE DUPLICATE VEHICLES
    # ==========================================================

    def _remove_duplicate_vehicles(
        self,
        vehicles,
    ):
        """
        Removes multiple detections that correspond
        to the same physical vehicle.

        IMPORTANT:
        Vehicle classes are NOT required to match.

        Therefore:

            car + car     -> compare
            car + truck   -> compare
            truck + truck -> compare

        This is important because YOLO can sometimes
        classify the same physical vehicle differently.
        """

        if not vehicles:
            return []

        # ------------------------------------------------------
        # Highest-confidence detections first
        # ------------------------------------------------------

        vehicles = sorted(
            vehicles,
            key=lambda vehicle:
                vehicle[
                    "vehicle_confidence"
                ],
            reverse=True,
        )

        kept = []

        for vehicle in vehicles:

            current_box = vehicle[
                "bbox"
            ]

            current_class = vehicle[
                "vehicle_class"
            ]

            current_confidence = vehicle[
                "vehicle_confidence"
            ]

            duplicate = False

            # --------------------------------------------------
            # Compare with already accepted vehicles
            # --------------------------------------------------

            for existing in kept:

                existing_box = existing[
                    "bbox"
                ]

                existing_class = existing[
                    "vehicle_class"
                ]

                # --------------------------------------------------
                # IoU
                # --------------------------------------------------

                iou = self.calculate_iou(
                    current_box,
                    existing_box,
                )

                # --------------------------------------------------
                # Containment / overlap
                # --------------------------------------------------

                overlap = (
                    self.calculate_overlap_ratio(
                        current_box,
                        existing_box,
                    )
                )

                # --------------------------------------------------
                # Duplicate condition
                # --------------------------------------------------

                if (
                    iou
                    >= self.DUPLICATE_IOU_THRESHOLD
                    or
                    overlap
                    >= self.DUPLICATE_OVERLAP_THRESHOLD
                ):

                    duplicate = True

                    print(
                        "Duplicate vehicle "
                        "detection removed:"
                    )

                    print(
                        f"  Current: "
                        f"{current_class} "
                        f"({current_confidence:.2f})"
                    )

                    print(
                        f"  Existing: "
                        f"{existing_class} "
                        f"("
                        f"{existing['vehicle_confidence']:.2f}"
                        f")"
                    )

                    print(
                        f"  IoU: "
                        f"{iou:.2f}"
                    )

                    print(
                        f"  Overlap: "
                        f"{overlap:.2f}"
                    )

                    break

            # --------------------------------------------------
            # Keep unique detection
            # --------------------------------------------------

            if not duplicate:
                kept.append(
                    vehicle
                )

        # ------------------------------------------------------
        # Reassign vehicle IDs
        # ------------------------------------------------------

        for vehicle_id, vehicle in enumerate(
            kept,
            start=1,
        ):

            vehicle[
                "vehicle_id"
            ] = vehicle_id

        return kept

    # ==========================================================
    # DETECT VEHICLES
    # ==========================================================

    def detect(
        self,
        image,
    ):
        """
        Detect vehicles in an image.

        Returns:
            List of unique vehicle detections.
        """

        # ------------------------------------------------------
        # YOLO detection
        # ------------------------------------------------------

        results = self.model.predict(
            source=image,

            conf=VEHICLE_CONFIDENCE,

            imgsz=VEHICLE_IMAGE_SIZE,

            classes=list(
                VEHICLE_CLASSES.keys()
            ),

            # Explicit NMS IoU threshold
            iou=0.60,

            # IMPORTANT:
            # Treat overlapping detections as duplicates
            # even when their predicted classes differ.
            agnostic_nms=True,

            verbose=False,
        )

        result = results[0]

        vehicles = []

        height, width = (
            image.shape[:2]
        )

        # ------------------------------------------------------
        # Extract detections
        # ------------------------------------------------------

        for box in result.boxes:

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

            class_name = (
                VEHICLE_CLASSES.get(
                    class_id,
                    "unknown",
                )
            )

            # --------------------------------------------------
            # Keep coordinates inside image
            # --------------------------------------------------

            x1 = max(
                0,
                x1,
            )

            y1 = max(
                0,
                y1,
            )

            x2 = min(
                width,
                x2,
            )

            y2 = min(
                height,
                y2,
            )

            # --------------------------------------------------
            # Invalid box
            # --------------------------------------------------

            if (
                x2 <= x1
                or y2 <= y1
            ):
                continue

            # --------------------------------------------------
            # Crop vehicle
            # --------------------------------------------------

            vehicle_crop = image[
                y1:y2,
                x1:x2
            ]

            # --------------------------------------------------
            # Store detection
            # --------------------------------------------------

            vehicles.append(
                {
                    "vehicle_id": 0,

                    "vehicle_class":
                        class_name,

                    "vehicle_confidence":
                        confidence,

                    "bbox": [
                        x1,
                        y1,
                        x2,
                        y2,
                    ],

                    "crop":
                        vehicle_crop,
                }
            )

        # ------------------------------------------------------
        # Remove duplicates
        # ------------------------------------------------------

        vehicles = (
            self._remove_duplicate_vehicles(
                vehicles
            )
        )

        return vehicles