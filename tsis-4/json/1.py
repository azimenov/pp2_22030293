import json

    
print("""Interface Status\n================================================================================""")
print("DN                                                 Description           Speed    MTU ")
print("-------------------------------------------------- --------------------  ------  ------")
with open('sample-data.json') as f:
    data = json.load(f)

for item in data["imdata"]:
        print(((item["l1PhysIf"])["attributes"])["dn"], end = "                               ")
        print(((item["l1PhysIf"])["attributes"])["speed"], end = "  ")
        print(((item["l1PhysIf"])["attributes"])["mtu"])
        