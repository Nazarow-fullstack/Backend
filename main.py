from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import BytesIO

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from anywhere (change for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store the uploaded Excel file in memory
excel_data = None

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    global excel_data
    contents = await file.read()  # Read the file into memory
    excel_data = pd.ExcelFile(BytesIO(contents))  # Store it as a Pandas ExcelFile object

    return {"message": "File uploaded successfully", "filename": file.filename}

@app.get("/get-data")
async def get_data():
    global excel_data
    if excel_data is None:
        return {"error": "No Excel file uploaded yet."}
    
    df = excel_data.parse(excel_data.sheet_names[0])  # Read the first sheet
    return df.to_dict(orient="records")  # Convert to JSON and return

