import _thread
import threading
import os
import json
import time
from chess import TUI
from chess import board
from network import network


print("connecting to server")
client = network.Network()
print("connected")
ping = 0
queuePos = 0
in_Queue = False
Color = ""


def network(conn,n):
    global queuePos,Color

    while True:
        if in_Queue:
            con = client.send("{\"header\": \"queue\"}")
            if not con == None:
                #print("test: ",con)
                if not con == "":
                    data = json.loads(con)
                    if "pos" in data["data"]:
                        queuePos = json.loads(con)["data"]["pos"]


        global ping
        t0 = time.time()
        req = conn.send("{\"header\":\"ping\"}")
        t1 = time.time()
        if not req == None:
             data = json.loads(req)
             if data["header"] == "pong":
                 ping = (t1 - t0)*1000

        time.sleep(0.1)





#check_connection(client,1)




threading.Thread(target=network, args=(client,1)).start()

nickName = input("Enter your nickname: ")

connection = client.send("{\"header\":\"connect\",\"data\":{\"nickname\":\"" + nickName + "\"}}")
data = json.loads(connection)

if data["header"] == "connected":
    print("logged in as " + data["data"]["nickname"])


con = client.send("{\"header\": \"request_queue\"}")

data = json.loads(con)

if data["header"] == "queued_in":
    in_Queue = True
    time.sleep(0.5)
    print("waiting for players (" + str(queuePos) + " in queue)")


while in_Queue:
    print("waiting for players (" + str(queuePos) + " in queue)")
    Pos = int(queuePos)
    if Pos < 0:
        if Pos == -1:
            Color = "white"
        else:
            Color = "black"
        in_Queue = False
        GameStarted = True

    time.sleep(2)


b = TUI.BoardGuiConsole(board.Board(),Color)

b.load("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")



while GameStarted:
    os.system("cls")
    turn = b.board.player_turn

    b.unicode_representation()



    while not turn == Color:
        con = client.send(json.dumps({"header":"get_fen"}))

        if not con == "":
            data = json.loads(con)
            if "header" in data:
                if data["header"] == "fen":
                    b.load(json.loads(con)["data"]["fen"])
                    turn = b.board.player_turn
        time.sleep(0.5)


    b.move()

    con = client.send(json.dumps({"header":"set_fen", "data":{"fen":b.board.export()}}))


#b = board.Board()

#TUI.display(b)
