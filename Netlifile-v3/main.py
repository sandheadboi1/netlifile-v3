from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from filestack import Client
import os
import shutil
import requests

#to run: python -m uvicorn main:app --reload
# to view: http://localhost:8000
# key: AneJf7xi8Rx2i1FR9pvRcz

key2 = Client("AneJf7xi8Rx2i1FR9pvRcz")
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

STORAGE_DIR = "storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/data")
async def get_data():
    return {"message": "Hello from Python!"}

#@app.get("/storage")
#async def get_files():
#    folder_path = "storage"  # relative to where you run main.py
#    try:
#        fileslist = os.listdir(folder_path)
#        return {"files": fileslist}
#    except FileNotFoundError:
#        return {"error": "storage folder not found"}
    
from fastapi.responses import FileResponse

STORAGE_DIR = "storage"

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(STORAGE_DIR, filename)
    if os.path.isfile(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
    return {"error": "File not found"}

    
uploaded_files = {}  # map filename -> filestack url

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(STORAGE_DIR, file.filename)

    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    new_filelink = key2.upload(filepath=file_location)
    uploaded_files[file.filename] = new_filelink.url

    return {
        "message": f"Saved at {new_filelink.url}",
        "link": new_filelink.url
    }

@app.get("/storage")
async def get_files():
    # return list of {name, url}
    return {"files": [{"name": k, "url": v} for k, v in uploaded_files.items()]}

