from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

# Your existing routes here, e.g.:
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Vercel!"}

# Adapter for Vercel serverless
handler = Mangum(app)
