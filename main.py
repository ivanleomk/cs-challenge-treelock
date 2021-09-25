# A Bare Bones Slack API
# Illustrates basic usage of FastAPI
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import json
import requests
import os
import sseclient

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


@app.post("/parasite")
async def run_parasite(request: Request):
    from parasites import solve
    body = await request.body()
    body = json.loads(body)
    return solve(body)


@app.post("/tic-tac-toe")
async def run_ttt(request: Request):
    body = await request.body()
    body = json.loads(body)
    battle_id = body["battleId"]
    stream = requests.get("https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + battle_id, stream=True, headers={'Accept': 'text/event-stream'})
    client = sseclient.SSEClient(stream)
    for event in client.events():
        print(json.loads(event.data))
        requests.post("https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" +
                      battle_id, json={"action": "(╯°□°)╯︵ ┻━┻"})
    print("########")






@app.post("/stonks")
async def run_stonks(request: Request):
    body = await request.body()
    body = json.loads(body)
    print(body)
