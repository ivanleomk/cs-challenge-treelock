# A Bare Bones Slack API
# Illustrates basic usage of FastAPI
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List


# Instantiate the FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}