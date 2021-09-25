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

import json

@app.post("/parasite")
async def run_parasite(request: Request):
    from parasites import solve
    body = await request.body()
    body = json.loads(body)
    return solve(body)
    