from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from model import analyze_train, route_search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Railway Analytics Backend Running 🚆"}

@app.get("/predict/{train_no}")
def predict(train_no: int):
    return analyze_train(train_no)

@app.get("/route-search")
def search(source: str, destination: str):
    return route_search(source, destination)