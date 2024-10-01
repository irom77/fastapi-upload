import os
from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.responses import JSONResponse
import shutil

app = FastAPI()

API_KEY = "abc"  # Replace with your actual API key
UPLOAD_DIR = "downloaded"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...), x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    
    if not file.filename.endswith('.csv'):
        return JSONResponse(status_code=400, content={"message": "File must be a CSV"})
    
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    return {"message": f"CSV file '{file.filename}' uploaded successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
