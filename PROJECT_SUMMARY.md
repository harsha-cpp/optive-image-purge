Project summary (as implemented during this session)

Overview
- Purpose: Anonymize images by detecting and blurring sensitive content while preserving layout.
- Inputs: Images in `input_images/`.
- Outputs: Redacted images in `output_images/`.

Pipeline (final architecture)
1) OCR extraction
   - Library: EasyOCR
   - Output: tokens with bounding boxes per line

2) Token grouping
   - Cluster OCR results into lines (y-center proximity), left-to-right sort.

3) Gemini-assisted selection (required when GEMINI_API_KEY is set)
   - Library: `google-generativeai` (Gemini 1.5 Flash)
   - We send line-wise token text as JSON and the contents of `instructions.txt`.
   - Model returns JSON array of `{ line_idx, token_idx }` to blur.

4) Rule-based redaction (precision-focused)
   - Regex patterns:
     - Emails, phone numbers, long numbers, ID-like tokens.
     - Address indicators (Street/Lane/Road/etc.).
     - Bank-related keywords (bank/iban/ifsc/swift/routing/account/micr).
   - Label → value logic:
     - Labels (e.g., `Employee ID`, `Issue Date`, `Phone`, `Email`) cause tokens to the right on the same line to be blurred.
   - Cross-token detection:
     - Reconstructs a line string to catch emails/phones split across multiple tokens and maps matches back to token indices.

5) NER-based redaction (complementary)
   - Library: Presidio Analyzer with spaCy `en_core_web_sm`.
   - Entities targeted: PERSON, EMAIL_ADDRESS, PHONE_NUMBER, LOCATION, CREDIT_CARD, US_SSN, DATE_TIME, etc.
   - Hits are mapped back to the OCR tokens and blurred.

6) Blurring
   - OpenCV Gaussian blur applied per token bounding box.
   - Kernel scales with region size.

Files changed
- `utils/image_utils.py`
  - Replaced cloud call with local OCR flow.
  - Added regex heuristics, label→value logic, name/address/bank rules.
  - Added Presidio+spaCy NER integration.
  - Added Gemini-assisted token selection (mandatory when key present).
  - Added cross-token stitching for emails/phones/long numbers/addresses.
- `requirements.txt`
  - `opencv-python-headless`, `easyocr`, `numpy`, `pillow`, `python-dotenv`
  - `presidio-analyzer`, `spacy`, `google-generativeai`
- `readme.md`
  - Updated to reflect local processing and setup steps.

Environment/setup
- Create venv: `python3 -m venv .venv && source .venv/bin/activate`
- Install deps: `python -m pip install -r requirements.txt`
- spaCy model: `python -m spacy download en_core_web_sm` (first run only)
- Gemini (optional/required by current code path): set `GEMINI_API_KEY` in shell or `.env`.

How to run
- `source .venv/bin/activate && python main.py`
- Output will be written to `output_images/` with the same filenames.

Notes/limitations observed
- OCR may split single items (e.g., emails) into multiple tokens; the cross-token pass addresses this but can still depend on OCR accuracy.
- Presidio with the small spaCy model favors speed over recall; upgrading to a larger model can improve name/address recall at the cost of size.
- Gemini selection depends on accurate OCR text; very noisy scans can reduce effectiveness.

Recommended next improvements
- Add page/region-level de-duplication and union merging of overlapping boxes to avoid repeated blurs.
- Persist debug overlays (boxes + labels) to a sidecar image for easier QA.
- Add CLI switches to toggle: Gemini on/off, aggressiveness levels, languages for EasyOCR.
- Consider Cloud Vision OCR for higher-quality bounding boxes if acceptable.


