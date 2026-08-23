import cv2


def overlay_vehicle_result(
    output_image,
    vehicle,
    plate_text,
):
    # Vehicle bounding box
    x1, y1, x2, y2 = vehicle["bbox"]
    box_width = x2 - x1
    box_height = y2 - y1
    # Dynamic font size based on bounding box
    font_scale = max(
        0.35,
        min(
            0.65,
            box_width / 500,
        ),
    )

    font_thickness = max(
        1,
        int(font_scale * 4),
    )
    cv2.rectangle(
        output_image,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2,
    )
    # Vehicle label
    vehicle_label = (
        f"{vehicle['vehicle_class']} "
        f"{vehicle['vehicle_confidence']:.2f}"
    )
    cv2.putText(
        output_image,
        vehicle_label,
        (
            x1,
            max(
                20,
                y1 - int(35 * font_scale / 0.6),
            ),
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (0, 255, 0),
        font_thickness,
    )

    # Plate label
    plate_label = (
        f"Plate: {plate_text}"
    )

    cv2.putText(
        output_image,
        plate_label,
        (
            x1,
            max(
                20,
                y1 - int(10 * font_scale / 0.65),
            ),
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (0, 255, 255),
        font_thickness,
    )