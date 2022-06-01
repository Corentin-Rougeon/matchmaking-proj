from network import Network
import json

f = open("data_test.json", "r")




data = json.load(f)

client = Network()

print(json.dumps(data))

con = client.send(json.dumps(data))



print(json.loads(con))


while True:
    con = client.send("{\"header\": \"queue\"}")

    queuePos = json.loads(con)["data"]["pos"]

    print("queue position :" + queuePos)
