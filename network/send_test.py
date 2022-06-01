from network import Network
import json

f = open("data_test.json", "r")




data = json.load(f)

client = Network()

print(json.dumps(data))

con = client.send(json.dumps(data))



print(json.loads(con))

con = client.send("{\"header\": \"request_queue\"}")

data = json.loads(con)

if data["header"] == "queued_in":
    while True:
        con = client.send("{\"header\": \"queue\"}")

        queuePos = json.loads(con)["data"]["pos"]

        print("queue position :" + queuePos)
