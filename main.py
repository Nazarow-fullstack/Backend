from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import BytesIO
import os

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from anywhere (change for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File storage path
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store the uploaded file path
excel_file_path = None

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    global excel_file_path
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())  # Save file to disk
        
        excel_file_path = file_path  # Store path for retrieval
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/get-data")
async def get_data():
    global excel_file_path
    if excel_file_path is None:
        raise HTTPException(status_code=400, detail="No Excel file uploaded yet.")
    
    try:
        # Load the Excel file from disk
        excel_data = pd.ExcelFile(excel_file_path)
        
        # Check if the Excel file has any sheets
        if not excel_data.sheet_names:
            raise HTTPException(status_code=400, detail="Excel file contains no sheets.")
        
        df = excel_data.parse(excel_data.sheet_names[0])  # Read the first sheet
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded Excel sheet is empty.")
        
        return df.to_dict(orient="records")  # Convert to JSON and return
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading Excel file: {str(e)}")
