from pathlib import Path
import json

from app.anpr.pipeline import ANPRPipeline
from app.config import (
    OUTPUT_IMAGES_DIR,
    JSON_RESULTS_DIR,
)

# INPUT DIRECTORY
INPUT_DIR = Path(
    "test_images"
)

# SUPPORTED IMAGE TYPES
SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
}
# FIND IMAGES
def get_images():
    if not INPUT_DIR.exists():
        raise FileNotFoundError(
            f"Input directory does not exist: "
            f"{INPUT_DIR}"
        )
    images = [
        path
        for path in INPUT_DIR.iterdir()
        if (
            path.is_file()
            and path.suffix.lower()
            in SUPPORTED_EXTENSIONS
        )
    ]
    return sorted(images)
# PRINT RESULT
def print_result(result):
    print("\n")
    print("=" * 80)
    print(
        f"IMAGE: {result['image']}"
    )
    print("=" * 80)
    vehicles = result.get(
        "vehicles",
        [],
    )
    if not vehicles:
        print(
            "No vehicles with detected plates."
        )
        return
    for vehicle in vehicles:
        print(
            f"\nVehicle ID: "
            f"{vehicle['vehicle_id']}"
        )
        print(
            f"Vehicle: "
            f"{vehicle['vehicle_class']}"
        )
        print(
            f"Vehicle confidence: "
            f"{vehicle['vehicle_confidence']:.2f}"
        )
        print(
            f"Plate detected: "
            f"{vehicle['plate_detected']}"
        )
        print(
            f"Plate confidence: "
            f"{vehicle['plate_confidence']:.2f}"
        )
        print(
            f"Plate: "
            f"{vehicle['plate_text']}"
        )
        print(
            f"OCR confidence: "
            f"{vehicle['ocr_confidence']:.2f}"
        )
        print(
            f"Status: "
            f"{vehicle['status']}"
        )
# MAIN
def main():
    images = get_images()
    if not images:
        print(
            f"No images found in: "
            f"{INPUT_DIR}"
        )
        return
    print(
        "ANPR BATCH TEST"
    )
    print(
        f"Input directory: "
        f"{INPUT_DIR}"
    )
    print(
        f"Images found: "
        f"{len(images)}"
    )
    # Initialize pipeline ONCE
    pipeline = ANPRPipeline()
    all_results = []
    # Process every image
    for index, image_path in enumerate(
        images,
        start=1,
    ):
        print("\n")
        print(
            "#" * 80
        )
        print(
            f"PROCESSING "
            f"{index}/{len(images)}"
        )
        print(
            f"Image: {image_path.name}"
        )
        try:
            result = (
                pipeline.process_image(
                    image_path
                )
            )
            all_results.append(
                result
            )
            print_result(
                result
            )
        except Exception as error:
            print(
                f"\nERROR processing "
                f"{image_path.name}:"
            )
            print(error)
            all_results.append(
                {
                    "image": image_path.name,
                    "status": "Error",
                    "error": str(error),
                    "vehicles": [],
                }
            )
    # Save combined JSON
    combined_json_path = (
        JSON_RESULTS_DIR
        / "batch_results.json"
    )
    with open(
        combined_json_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            all_results,
            file,
            indent=4,
            ensure_ascii=False,
        )
    # Summary
    total_images = len(
        all_results
    )
    successful_images = sum(
        1
        for result in all_results
        if result.get("status")
        == "Processed"
    )
    total_plates = sum(
        len(
            result.get(
                "vehicles",
                [],
            )
        )
        for result in all_results
    )
    readable_plates = sum(
        1
        for result in all_results
        for vehicle in result.get(
            "vehicles",
            [],
        )
        if vehicle.get("status")
        == "Readable"
    )
    unreadable_plates = sum(
        1
        for result in all_results
        for vehicle in result.get(
            "vehicles",
            [],
        )
        if vehicle.get("status")
        == "Unreadable"
    )
    print("\n")
    print("BATCH SUMMARY")
    print(
        f"Images processed: "
        f"{successful_images}/{total_images}"
    )
    print(
        f"Vehicles with detected plates: "
        f"{total_plates}"
    )
    print(
        f"Readable plates: "
        f"{readable_plates}"
    )
    print(
        f"Unreadable plates: "
        f"{unreadable_plates}"
    )
    print(
        f"\nCombined JSON:"
    )
    print(
        combined_json_path
    )
    print(
        f"\nOutput images:"
    )
    print(
        OUTPUT_IMAGES_DIR
    )

if __name__ == "__main__":
    main()