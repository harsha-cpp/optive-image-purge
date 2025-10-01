Let’s do a clean Windows setup and run the server step-by-step (PowerShell).

### 1) Prerequisites
- Install Python 3.10 or 3.11 (64-bit). Add Python to PATH during install.
- Optional but recommended: Microsoft Visual C++ Redistributable (most wheels work without build tools).
- Ensure PowerShell is running as a normal user (Admin not required).

### 2) Get the code
If copying the folder: place `Optive-image` somewhere like `C:\Projects\Optive-image`.
If using git:
```powershell
cd C:\Projects
git clone https://github.com/<your-repo>/Optive-image.git
cd .\Optive-image
```

### 3) Create and activate a virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
python -m pip install --upgrade pip wheel
```

### 4) Install dependencies
- Full (as in `requirements.txt`):
```powershell
pip install -r requirements.txt
```
- Lite (smaller, skips spaCy/Presidio/Gemini; still runs OCR):
```powershell
pip install opencv-python-headless easyocr numpy pillow python-dotenv fastapi "uvicorn[standard]" python-multipart
```

### 5) Optional: spaCy model (only if you installed spaCy/Presidio)
```powershell
python -m spacy download en_core_web_sm
```

### 6) Optional: Gemini API key
If you want Gemini-assisted selection:
```powershell
setx GEMINI_API_KEY "your_api_key_here"
# Close and reopen PowerShell to pick up setx, then:
.\.venv\Scripts\Activate
```

### 7) Run the server
From the project root (where `api.py` is):
```powershell
uvicorn api:app --host 0.0.0.0 --port 8010
```
- Health check: open `http://localhost:8010/health`
- API docs: `http://localhost:8010/docs`

### 8) Upload and test
Using Swagger UI at `/docs`, call `POST /anonymize` with a PNG/JPEG. You can also add instructions text if desired.

### Troubleshooting
- If activation fails: run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` in an elevated PowerShell, then retry activation.
- If `easyocr`/torch wheels fail to install, ensure you’re on 64-bit Python and up-to-date `pip`. CPU install is fine; no CUDA needed.
- If spaCy errors about missing model, run the download step in section 5.

Status: Provided a concise Windows install guide from code checkout to running `uvicorn`.

