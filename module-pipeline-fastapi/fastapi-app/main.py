from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for POST request data


class GreetingRequest(BaseModel):
    name: str
    age: int


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/greet/{name}")
def greet_name(name: str):
    return {"message": f"Hello, {name}!"}


@app.post("/greet")
def create_greeting(request: GreetingRequest):
    if request.age < 0:
        raise HTTPException(status_code=400, detail="Age cannot be negative")
    return {"message": f"Hello, {request.name}! You are {request.age} years old."}
