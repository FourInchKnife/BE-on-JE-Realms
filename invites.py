from mojangpy import Account
email = input("email:")
password = input("password:")
user = Account(email,password)

user.clientToken = input("client token (leave blank if you've never used this before):")

if user.clientToken == "":
    user.clientToken = user.gen_uuid()
    print("Your user token is \"{0}\"\nMake sure you save this somewhere you'll remember it. This is not sensitive data.".format(user.clientToken))
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

