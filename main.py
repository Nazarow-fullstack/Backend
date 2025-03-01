from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# CORS configuration (allows frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from anywhere (update for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder to store uploaded files
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store uploaded file path
excel_file_path = None

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    global excel_file_path
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())  # Save file
        
        excel_file_path = file_path  # Store path
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/get-data")
async def get_data():
    global excel_file_path
    if excel_file_path is None:
        raise HTTPException(status_code=400, detail="No Excel file uploaded yet.")
    
    try:
        df = pd.read_excel(excel_file_path)  # Read Excel file
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded Excel sheet is empty.")
        
        return df.to_dict(orient="records")  # Convert to JSON for Telegram bot
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading Excel file: {str(e)}")
