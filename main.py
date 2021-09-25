# A Bare Bones Slack API
# Illustrates basic usage of FastAPI
from fastapi import FastAPI, requests
import json
import requests
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
    me = None
    nxt = "O"
    for event in client.events():
        body = json.loads(event.data)
        print("RECEIVED", body)
        # First initiation
        if "youAre" in body:
            if body["youAre"] == "O":
                requests.post(
                    url, json={"action": "putSymbol", "position": ttt.get_dir(ttt.minimax(board))})
                me = "O"
            else:
                me = "X"
            continue
        # Msgs from server
        if "position" in body and "player" in body:
            # Check for correct player
            if body["player"] != nxt:
                requests.post(url, json={"action": "(╯°□°)╯︵ ┻━┻"})
                return
            nxt = ttt.get_other(nxt)
            # Execute the action received from the server
            b2 = ttt.result(board, ttt.get_action(body["position"]))
            # if not ttt.check_valid(board, b2):
            #     requests.post(url, json={"action": "(╯°□°)╯︵ ┻━┻"})
            #     return
            board = b2
            # Check if we need to send another action
            if body["player"] != me:
                requests.post(
                    url, json={"action": "putSymbol", "position": ttt.get_dir(ttt.minimax(board))})
        elif "action" in body and body["action"] == "(╯°□°)╯︵ ┻━┻":
            return
        elif "winner" in body:
            return
    print("########\n\n")


@app.post("/quoridor")
async def run_ttt(request: Request):
    body = await request.body()
    body = json.loads(body)
    battle_id = body["battleId"]
    stream = requests.get(
        "https://cis2021-arena.herokuapp.com/quoridor/start/" + battle_id, stream=True)
    client = sseclient.SSEClient(stream)
    url = "https://cis2021-arena.herokuapp.com/quoridor/play/" + battle_id
    for event in client.events():
        body = json.loads(event.data)
        print("RECEIVED", body)
        requests.post(url, json={"action": "(╯°□°)╯︵ ┻━┻"})
    print("########\n\n")


@app.post("/stonks")
async def run_stonks(request: Request):
    body = await request.body()
    body = json.loads(body)
    print(body)
