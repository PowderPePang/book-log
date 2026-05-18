from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, book log"}

@app.get("/health")
def health():
    return {"status": "ok"}