import os
import tempfile
import shutil
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from starlette.background import BackgroundTask

from utils.image_utils import anonymize_image


app = FastAPI(title="Optive Image Anonymizer", version="1.0.0")


@app.get("/health")
def health() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.post("/anonymize")
async def anonymize(
    image: UploadFile = File(...),
    instructions: Optional[str] = Form(None),
) -> FileResponse:
    if image.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        raise HTTPException(status_code=400, detail="Only PNG and JPEG images are supported")

    # Read instructions from file if not provided
    if not instructions:
        instructions_path = os.path.join(os.getcwd(), "instructions.txt")
        if os.path.exists(instructions_path):
            with open(instructions_path, "r") as f:
                instructions = f.read()
        else:
            instructions = ""

    # Create a persistent temp dir; clean it after response is sent
    tmpdir = tempfile.mkdtemp(prefix="optive_")
    input_suffix = ".png" if (image.filename or "").lower().endswith(".png") else ".jpg"
    input_path = os.path.join(tmpdir, f"input{input_suffix}")
    output_path = os.path.join(tmpdir, f"output{input_suffix}")

    # Save upload to disk
    content = await image.read()
    with open(input_path, "wb") as f:
        f.write(content)

    # Run anonymization
    anonymize_image(input_path, output_path, instructions or "")

    if not os.path.exists(output_path):
        # Cleanup on failure
        shutil.rmtree(tmpdir, ignore_errors=True)
        raise HTTPException(status_code=500, detail="Failed to generate anonymized image")

    # Return the processed image and delete temp dir after response is sent
    filename_base = os.path.splitext(os.path.basename(image.filename or "image"))[0]
    return FileResponse(
        output_path,
        media_type=image.content_type,
        filename=f"{filename_base}_anonymized{input_suffix}",
        background=BackgroundTask(lambda: shutil.rmtree(tmpdir, ignore_errors=True)),
    )


# To run locally: `uvicorn api:app --reload`

