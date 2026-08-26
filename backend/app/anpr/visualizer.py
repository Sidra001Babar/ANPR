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
    vehicle_text_size = cv2.getTextSize( 
        vehicle_label, 
        cv2.FONT_HERSHEY_SIMPLEX, 
        font_scale, 
        font_thickness, 
    )[0] 
    vehicle_text_x = ( 
        x1 + (box_width - vehicle_text_size[0]) // 2 
    ) 
    cv2.putText(
        output_image,
        vehicle_label,
        ( 
            vehicle_text_x, 
            y1 + int(25 * font_scale / 0.65), 
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
    plate_text_size = cv2.getTextSize( 
        plate_label, 
        cv2.FONT_HERSHEY_SIMPLEX, 
        font_scale, 
        font_thickness, 
    )[0] 
 
    plate_text_x = ( 
        x1 + (box_width - plate_text_size[0]) // 2 
    ) 

    cv2.putText(
        output_image,
        plate_label,
        ( 
            plate_text_x, 
            y1 + int(50 * font_scale / 0.65), 
        ), 
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        (0, 255, 255),
        font_thickness,
    )