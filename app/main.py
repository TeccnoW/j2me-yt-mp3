from dotenv import load_dotenv
load_dotenv(".env")

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import modules.xPyTube as xPyTube
import jinja2
import urllib.parse

app = FastAPI(
    version="0.0.1",
    redoc_url="/redocs",  # None
    docs_url="/docs"  # None
)

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = jinja2.Environment(loader=jinja2.FileSystemLoader("static"))

@app.get("/online")
async def online():
    return {"status": "online"}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    template = templates.get_template("index.html")
    return HTMLResponse(template.render())

@app.post("/download")
async def download_file(url: str = Form(...)):
    result = xPyTube.convert_to_mp3(url)
    if result:
        mp3_path, name = result
        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{urllib.parse.quote(name)}"
        }
        return FileResponse(mp3_path, media_type='audio/mpeg', headers=headers)
    return {"error": "Error occurred"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)