import secrets
import socket
import json
import string
from _thread import *
import sys
import random

server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


Queue = []
Online_players = {}
Playing = {}
Games = []
Fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
White = ""
Black = ""
GameStarted = False
GameID = 0


try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")



def send_data(conn, data):
    conn.send(str.encode(data))


def recieve(conn,player):
    print(conn,player)
    data = conn.recv(1024).decode()

    if(data == "handshake"):
        send_data(conn, "handshake")


    return conn.recv(1024).decode()





def threaded_client(conn, datain):
    global GameStarted, White, Black,Fen
    conn.send(str.encode(datain))
    print(conn)
    print(datain)
    QueuePos = 0
    reply = ""
    while True:
        try:

            data = conn.recv(1024).decode()
            jsonData = json.loads(data)
            header = ""

            if "header" in jsonData:
                header = jsonData["header"]

            if not data:
                print("Disconnected")

                break
            else:
                reply = data

                #print("Received: ", data)
                #print("header: ", header)

                if header == "connect":
                    Online_players[datain] = jsonData["data"]["nickname"]
                    print(Online_players)
                    reply = "{\"header\": \"connected\", \"data\": {\"nickname\": \"" + jsonData["data"]["nickname"] + "\"}}"


                if header == "request_queue":
                    Queue.append(datain)
                    print("queue :",Queue)
                    QueuePos = len(Queue)
                    reply = "{\"header\": \"queued_in\"}"

                if header == "queue":
                    QueuePos = Queue.index(datain) + 1
                    if QueuePos > 2 or not GameStarted:
                        reply = "{\"header\": \"queue\",\"data\":{\"pos\":\"" + str(QueuePos) + "\"}}"
                    else:
                        reply = "{\"header\": \"queue\",\"data\":{\"pos\":\"" + str(-QueuePos) + "\"}}"
                    #reply = "{\"header\": \"queue\",\"data\":{\"pos\":\"" + str(QueuePos) + "\"}}"




                if header == "ping":
                    reply = "{\"header\": \"pong\"}"


                if header == "set_fen":
                    Fen = jsonData["data"]["fen"]

                if header == "get_fen":
                    reply = "{\"header\": \"fen\",\"data\":{\"fen\":\"" + Fen + "\"}}"


                if len(Queue) > 1 and not GameStarted:
                    print(Queue)
                    White = Queue[0]
                    Black = Queue[1]
                    GameStarted = True


                #print("Sending: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break
    if datain in Queue:
        Queue.remove(datain)


    Online_players.pop(datain,None)
    print("Lost connection")
    print(Queue)

    if len(Queue) <= 1:
        GameStarted = False
        Fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        White = ""
        Black = ""

    conn.close()

currentPlayer = 0



while True:
    conn, addr = s.accept()
    token = ''.join(random.choices(string.ascii_lowercase, k=10))

    print("Connected to:", addr)



    start_new_thread(threaded_client, (conn, token))
    print(currentPlayer)
    currentPlayer += 1