import secrets
import socket
import json
from _thread import *
import sys

server = "0.0.0.0"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Queue = []
Games = []

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
    data = conn.recv(2048).decode()

    if(data == "handshake"):
        send_data(conn, "handshake")


    return conn.recv(2048).decode()

def threaded_client(conn, datain):
    conn.send(str.encode(datain))
    print(conn)
    print(datain)
    QueuePos = 0
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()
            jsonData = json.loads(data)
            header = ""

            if "header" in jsonData:
                header = jsonData["header"]

            if not data:
                print("Disconnected")

                break
            else:
                reply = data

                print("Received: ", data)
                print("header: ", header)

                if header == "connect":
                    Queue.append(datain)
                    print(Queue)
                    QueuePos = len(Queue)
                    reply = "{\"header\": \"connected\"}"


                if header == "queue":
                    QueuePos = Queue.index(datain) + 1
                    reply = "{\"header\": \"queue\",\"data\":{\"pos\":\"" + str(QueuePos) + "\"}}"

                print("Sending: ", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    Queue.remove(datain)

    print("Lost connection")
    print(Queue)
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    token = secrets.token_urlsafe(16)
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, token))
    print(currentPlayer)
    currentPlayer += 1