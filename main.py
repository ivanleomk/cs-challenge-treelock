# A Bare Bones Slack API
# Illustrates basic usage of FastAPI
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
import json
import requests
import os
import sseclient
import tictactoe as ttt

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
    stream = requests.get(
        "https://cis2021-arena.herokuapp.com/tic-tac-toe/start/" + battle_id, stream=True)
    client = sseclient.SSEClient(stream)
    url = "https://cis2021-arena.herokuapp.com/tic-tac-toe/play/" + battle_id
    board = ttt.initial_state()
    for event in client.events():
        body = json.loads(event.data)
        print("RECEIVED", body)
        # First initiation
        if "youAre" in body:
            if body["youAre"] == "O":
                action = ttt.minimax(board)
                board = ttt.result(board, action)
                print("SENT", {"action": "putSymbol", "position": ttt.get_dir(action)})
                requests.post(
                    url, json={"action": "putSymbol", "position": ttt.get_dir(action)})
            continue
        # Other msgs from server
        if "position" in body:
            # Execute the server's action
            action = ttt.get_action(body["position"])
            board = ttt.result(board, action)
            # Execute and send back our own action
            action = ttt.minimax(board)
            board = ttt.result(board, action)
            print("SENT", {"action": "putSymbol", "position": ttt.get_dir(action)})
            requests.post(
                url, json={"action": "putSymbol", "position": ttt.get_dir(action)})
        else:
            requests.post(url, json={"action": "(╯°□°)╯︵ ┻━┻"})
    print("########\n\n")

@app.post("/stonks")
async def run_stonks(request: Request):
    body = await request.body()
    body = json.loads(body)
    print(body)
