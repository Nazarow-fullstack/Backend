from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import json
import os
from fastapi.responses import FileResponse

app = FastAPI()

JSON_FILE = "data.json"
EXCEL_FILE = "data.xlsx"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are allowed")
    
    # Read the Excel file into a Pandas DataFrame
    df = pd.read_excel(file.file)
    
    # Convert DataFrame to JSON
    json_data = df.to_json(orient="records", indent=4)
    
    # Save JSON data to a file
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        f.write(json_data)
    
    return {"message": "File uploaded and converted to JSON successfully"}

@app.get("/download")
def download_file():
    if not os.path.exists(JSON_FILE):
        raise HTTPException(status_code=404, detail="No data available")
    
    # Read JSON data
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Convert JSON back to DataFrame
    df = pd.DataFrame(data)
    
    # Save it as an Excel file
    df.to_excel(EXCEL_FILE, index=False)
    
    return FileResponse(EXCEL_FILE, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="data.xlsx")
