import cv2


def expand_plate_crop(
    plate_crop,
    horizontal_ratio=0.08,
    vertical_ratio=0.15,
):
    if plate_crop is None or plate_crop.size == 0:
        return None
    height, width = plate_crop.shape[:2]
    x_margin = int(width * horizontal_ratio)
    y_margin = int(height * vertical_ratio)
    return plate_crop


def preprocess_plate_variants(plate_crop):
    if plate_crop is None or plate_crop.size == 0:
        return {}

    # Resize

    height, width = plate_crop.shape[:2]

    # Target height for OCR.
    target_height = 160

    scale = target_height / max(height, 1)

    target_width = max(
        int(width * scale),
        100,
    )

    resized = cv2.resize(
        plate_crop,
        (target_width, target_height),
        interpolation=cv2.INTER_CUBIC,
    )

    # Slight denoising

    denoised = cv2.bilateralFilter(
        resized,
        5,
        50,
        50,
    )

    # Grayscale

    gray = cv2.cvtColor(
        denoised,
        cv2.COLOR_BGR2GRAY,
    )

    # Contrast enhancement

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )

    clahe_image = clahe.apply(gray)

    # Sharpen

    sharpen_kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (3, 3),
    )

    sharpened = cv2.addWeighted(
        clahe_image,
        1.5,
        cv2.GaussianBlur(
            clahe_image,
            (0, 0),
            2,
        ),
        -0.5,
        0,
    )

    # OTSU

    _, otsu = cv2.threshold(
        clahe_image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    # Adaptive threshold
    adaptive = cv2.adaptiveThreshold(
        clahe_image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )

    return {
        "original": resized,
        "gray": gray,
        "clahe": clahe_image,
        "sharpened": sharpened,
        "otsu": otsu,
        "adaptive": adaptive,
    }


def preprocess_plate(plate_crop):
    variants = preprocess_plate_variants(
        plate_crop
    )

    return variants.get(
        "sharpened"
    )