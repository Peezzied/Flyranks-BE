from fastapi import FastAPI

app = FastAPI(title="A4 - Auth Practice")

@app.get("/")
def home():
    pass