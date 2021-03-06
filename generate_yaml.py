from mojangpy import Account
import json

if input("Have you used this before (y/N)?").lower() in ["y","yes"]:
    store = False
    with open("creds.json","r") as file:
        fileJson = json.loads(file.read())
        try:
            email = fileJson["email"]
            password = fileJson["password"]
        except:
            email = input("email:")
            password = input("password:")
            store = True
        if store:
            if input("Do you want to store your login (y/N)?").lower() in ["y","yes"]:
                with open("creds.json","w") as file:
                    file.write(json.dumps({"email":email,"password":password,"clientToken":user.clientToken}))
        user = Account(email,password)
        user.clientToken = fileJson["clientToken"]
else:
    email = input("email:")
    password = input("password:")
    user = Account(email,password)
    user.clientToken = user.gen_uuid()
    if input("Do you want to store your login (y/N)?").lower() in ["y","yes"]:
        with open("creds.json","w") as file:
            file.write(json.dumps({"email":email,"password":password,"clientToken":user.clientToken}))
    else:
        with open("creds.json","w") as file:
            file.write(json.dumps({"clientToken":user.clientToken}))

BEName = input("bedrock edition username (caps matter):")


user.authenticate()
if user.validate():
   print("logged in")
else:
    print("vaidation failed...")
user.realm_worlds()
for i in user.realms:
    print("[{0}] {1}".format(user.realms.index(i),i.name))
realm = user.realms[int(input("which one?"))]
joinResponse = realm.join()
print(joinResponse.text)
ip = joinResponse.json()["address"].split(":")
user.invalidate()
print("logged out")
print("generating config.yml for geyser")
with open("sample.yml","r") as file:
    sample = file.read()
sample = sample.format(realm.motd,realm.owner.username,realm.name,ip[0],ip[1],BEName,email,password)
print(sample)
with open("config.yml","w") as file:
    file.write(sample)
