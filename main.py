# A Bare Bones Slack API
# Illustrates basic usage of FastAPI
from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
from fastapi import FastAPI, Request
import json
import requests
import sseclient
import tictactoe as ttt
import datetime

# Instantiate the FastAPI
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/asteroid")
async def run_asteroid(request: Request):
    from asteroids import solve
    body = await request.body()
    body = json.loads(body)
    print(body)
    return solve(body["test_cases"])


@app.post("/parasite")
async def run_parasite(request: Request):
    from parasites import solve
    body = await request.body()
    body = json.loads(body)
    return solve(body)


@app.post("/optopt")
async def run_optopt(request: Request):
    body = await request.body()
    body = json.loads(body)
    print(body)


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
            try:
                b2 = ttt.result(board, ttt.get_action(body["position"]))
            except:
                requests.post(url, json={"action": "(╯°□°)╯︵ ┻━┻"})
                return
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


@app.post("/stock-hunter")
async def run_stonks(request: Request):
    from stockhunter import solve
    body = await request.body()
    body = json.loads(body)
    return solve(body)


cred = credentials.Certificate('firebase-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.post("/fixedrace")
async def run_race(request: Request):
    body = await request.body()
    races = db.collection("race_strs")

    docs = races.stream()

    key = str(datetime.datetime.now().hour)
    results = None
    for doc in docs:
        if doc.id == key:
            results = doc.to_dict()
    print(results)

    races.document(key).set(
        {str(datetime.datetime.now()): str(body)}, merge=True)
    return body
