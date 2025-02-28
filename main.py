from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# CORS configuration (allowing requests from the frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Only allow localhost:3000 (your frontend)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

UPLOAD_FOLDER = "uploads"
EXCEL_FILE_NAME = "data.xlsx"

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    # Print the received file name to debug
    print(f"Received file: {file.filename}")

    file_path = os.path.join(UPLOAD_FOLDER, EXCEL_FILE_NAME)

    # Remove old file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)

    # Save the new file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"File saved to {file_path}")

    return {"message": "File uploaded successfully", "filename": EXCEL_FILE_NAME}
