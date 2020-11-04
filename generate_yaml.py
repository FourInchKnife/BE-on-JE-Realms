import pyyaml
from mojangpy import Account
email = input("email:")
password = input("password:")
BEName = input("bedrock edition username (caps matter):")
user.clientToken = input("client token (leave blank if you've never used this before):")

user = Account(email,password)
if user.clientToken = "":
    user.clientToken = user.gen_uuid()

print("Your user token is \"{0}\"\nMake sure you save this somewhere you'll remember it. This is not sensitive data.".format(user.clientToken))
user.authenticate()
if user.validate():
   print("logged in")
else:
    print("vaidation failed...")
user.realm_worlds()
for i in user.realms:
    print("[{0}] {1}".format(user.realms.index(i),i.name))
realm = user.realms[int(input("which one?"))]
ip = realm.join().split(":")
user.invalidate()
print("logged out")
print("generating config.yml for geyser")
with open("sample.yml","r") as file:
    sample = file.read()
sample = sample.format(realm.motd,realm.owner,realm.name,ip[0],ip[1],BEName,email,password)
print(sample)
with open("config.yml","w") as file:
    file.write(sample)
