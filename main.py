import os
from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.responses import JSONResponse
import shutil

app = FastAPI()

API_KEY = "abc"  # Replace with your actual API key
UPLOAD_DIR = "downloaded"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to the File Upload API"}

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...), x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    
    if not (file.filename.endswith('.csv') or file.filename.endswith('.json')):
        return JSONResponse(status_code=400, content={"message": "File must be a CSV or JSON"})
    
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    file_type = "CSV" if file.filename.endswith('.csv') else "JSON"
    return {"message": f"{file_type} file '{file.filename}' uploaded successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

print("FastAPI application is running. Access it at http://localhost:8000")
print("Available endpoints:")
print("  GET  /")
print("  POST /upload-file/")
