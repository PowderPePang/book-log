from fastapi import FastAPI
from app.routes import books

app = FastAPI(title="Booklog API")

# Plug the router into the application
app.include_router(books.router)

@app.get("/")
def read_root():
    return {"status": "ok, API is running"}