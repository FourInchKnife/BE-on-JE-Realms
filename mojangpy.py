import requests

class InputError(Exception):
    def __init__(self,message=" ",response=" "):
        super().__init__("Invalid user input: "+message+"\n"+response)
class ResponseError(Exception):
    def __init__(self,message=" ",response= " "):
        super().__init__("Mojang's server gave an unexpected response: "+response+"\n"+message)

class Player():
    def __init__(self,username,uuid):
        self.username = username
        self.uuid = uuid

class Account():
    def __init__(self,username,password,clientToken = None):
        self.username = username
        self.password = password
        self.clientToken = clientToken
        self.session = requests.Session()
    def gen_uuid(self):
        return requests.get("https://www.uuidgenerator.net/api/version4").text
    def authenticate(self):
        payload = { \
            "agent":{ \
                "name":"Minecraft", \
                "version":1 \
            }, \
            "username":self.username, \
            "password":self.password, \
            "clientToken":self.clientToken, \
            "requestUser":True \
        }
        auth_response = self.session.post("https://authserver.mojang.com/authenticate",json=payload)
        if not "accessToken" in list(auth_response.json()):
            raise InputError("either the username or the password was incorrect.",auth_response.text)
        self.auth_data = auth_response.json()
        self.cookie = { \
            "sid":"token:{0}:{1}".format(self.auth_data["accessToken"],self.auth_data["selectedProfile"]["id"]), \
            "user":self.auth_data["selectedProfile"]["name"], \
            "version":"1.16.4"\
        }
    def signout(self):
        payload = { \
            "username":self.username, \
            "password":self.password \
        }
        self.session.post("https://authserver.mojang.com/signout",json=payload)
    def invalidate(self):
        payload = { \
            "accessToken": self.auth_data["accessToken"], \
            "clientToken": self.auth_data["clientToken"] \
        }
        self.session.post("https://authserver.mojang.com/invalidate",json=payload)
    def validate(self):
        payload = { \
            "accessToken": self.auth_data["accessToken"], \
            "clientToken": self.auth_data["clientToken"] \
        }
        response = self.session.post("https://authserver.mojang.com/validate",json=payload).status_code
        if response == 204:
            return True
        elif response == 403:
            return False
        else:
            print("something very much broke... ono")
    def refresh(self):
        payload = { \
            "accessToken": self.auth_data["accessToken"], \
            "clientToken": self.auth_data["clientToken"], \
            "requestUser": True \
        }
        self.auth_response = self.session.post("https://authserver.mojang.com/refresh",json=payload)
        self.auth_data = self.auth_response.json()
        self.cookie = { \
            "sid":"token:{0}:{1}".format(self.auth_data["accessToken"],self.auth_data["selectedProfile"]["id"]), \
            "user":self.auth_data["selectedProfile"]["name"], \
            "version":"1.16.4"\
        }
    def realm_worlds(self):
        response = self.session.get("https://pc.realms.minecraft.net/worlds",cookies=self.cookie)
        print(response,response.text)
        self.realms = []
        for i in response.json()["servers"]:
            self.realms.append(Realm(self,i))
    def realm_invites(self):
        response = self.session.get("https://pc.realms.minecraft.net/invites/pending",cookies=self.cookie)
        print(response,response.text)
        self.invites = []
        for i in response.json()["invites"]:
            self.invites.append(RealmInvite(self,i))

class Realm():
    def __init__(self,account,data):
        self.id = data["id"]
        self.remoteSubscriptionId = data["remoteSubscriptionId"]
        self.owner = Player(data["owner"],data["ownerUUID"])
        self.name = data["name"]
        self.motd = data["motd"]
        self.state = data["state"]
        self.account = account
    def join(self):
        return self.account.session.get("https://pc.realms.minecraft.net/worlds/v1/{0}/join/pc".format(self.id),cookies=self.account.cookie).json()["address"]

class RealmInvite():
    def __init__(self,account,data):
        self.id = data["invitationId"]
        self.name = data["worldName"]
        self.description = data["worldDescription"]
        self.owner = Player(data["worldOwnerName"],data["worldOwnerUuid"])
        self.date = data["date"]
        self.account = account
    def accept(self):
        self.account.session.put("https://pc.realms.minecraft.net/invites/accept/"+self.id,cookies = self.account.cookie)
    def reject(self):
        self.account.session.put("https://pc.realms.minecraft.net/invites/reject/"+self.id,cookies = self.account.cookie)
