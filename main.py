# A Bare Bones Slack API
# Illustrates basic usage of FastAPI
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List


# Instantiate the FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/asteroid")
async def run_asteroid(request: Request):
    from asteroids import calc_asteroids
    body = await request.body()
    return calc_asteroids(body)
