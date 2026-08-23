from pathlib import Path
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.config import UPLOADS_DIR
from app.anpr.pipeline import ANPRPipeline

router = APIRouter(
    prefix="/api/image",
    tags=["ANPR Image"],
)


# LOAD ANPR PIPELINE ONCE
pipeline = ANPRPipeline()


# ALLOWED IMAGE TYPES
ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
}


# PROCESS IMAGE
@router.post("/process")
async def process_image(
    file: UploadFile = File(...),
):

    # Validate file
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected.",
        )

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Allowed: JPG, JPEG, PNG, WEBP, BMP."
            ),
        )

    # Generate unique filename
    unique_name = (
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    input_path = (
        UPLOADS_DIR
        / unique_name
    )

    # Save uploaded image
    try:

        contents = await file.read()

        with open(
            input_path,
            "wb",
        ) as output_file:

            output_file.write(contents)

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Failed to save image: "
                f"{error}"
            ),
        )

    # Run ANPR
    try:

        result = pipeline.process_image(
            input_path
        )

    except Exception as error:

        # Remove uploaded file if processing fails
        if input_path.exists():
            input_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=(
                f"ANPR processing failed: "
                f"{error}"
            ),
        )

    # Return result
    output_path = Path(
        result["output_image"]
    )

    if not output_path.exists():

        raise HTTPException(
            status_code=500,
            detail="Processed image was not created.",
        )

    return {
        "success": True,

        "message": (
            "Image processed successfully."
        ),

        "filename": file.filename,

        "result": result,

        "processed_image": (
            f"/api/image/result/"
            f"{output_path.name}"
        ),
    }


# SERVE PROCESSED IMAGE
@router.get("/result/{filename}")
async def get_processed_image(
    filename: str,
):

    # Security: only use the filename
    safe_filename = Path(
        filename
    ).name

    file_path = (
        Path(
            "results/images"
        )
        / safe_filename
    )

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="Processed image not found.",
        )

    return FileResponse(
        path=file_path,
        media_type="image/jpeg",
    )