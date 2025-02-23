from fastapi import FastAPI

from app.search.search import search
from app.vectorize.vectorize import vectorize
from pydantic import BaseModel

app = FastAPI()

class SearchRequestBody(BaseModel):
    query: str

@app.get("/")
def health():
    return {"message": "Server is running"}

# vectorize
@app.get("/vectorize")
def vectorize_data():
    return vectorize()

# search
@app.post("/search")
def search_data(body: SearchRequestBody):
    return search(body.query)