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

user.authenticate()
if user.validate():
   print("logged in")
else:
    print("vaidation failed...")
user.realm_invites()
for i in user.invites:
    print("[{0}] {1}".format(user.invites.index(i),i.name))
realm = user.invites[int(input("which one?"))]
realm.accept()
user.invalidate()
print("logged out")
