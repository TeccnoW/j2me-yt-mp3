from fastapi import FastAPI

app = FastAPI(
    root_path="/APP",
    version="0.0.1",
    redoc_url="/redocs",  # None
    docs_url="/docs"  # None
)

@app.get("/online")
async def read_root():
    return {"status": "online"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)