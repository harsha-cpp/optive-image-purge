# Image Anonymizer

This project anonymizes images locally by detecting sensitive text (numbers, prices, IDs, etc.) via EasyOCR and blurring those regions with OpenCV.

## Installation

1.  Clone the repository.
2.  Create and activate a virtual environment, then install the required packages:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
    python -m pip install -r requirements.txt
    ```

## Usage

1.  Place your images (PNG, JPG, JPEG) in the `input_images` directory.
2.  Run the main script:
    ```bash
    python main.py
    ```
3.  The anonymized images will be saved in the `output_images` directory.

## Configuration

No API keys or native dependencies are required. Everything is installed via pip.
