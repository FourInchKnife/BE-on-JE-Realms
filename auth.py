import requests

class MinecraftUser():
    def __init__(self,username,password,uuid = None):
        self.username = username
        self.password = password
        self.clientToken = uuid
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
        self.auth_response = self.session.post("https://authserver.mojang.com/authenticate",json=payload)
        self.auth_data = self.auth_response.json()
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
        self.realms = response.json()["servers"]
    def realm_getIP(self,id):
        return self.session.get("https://pc.realms.minecraft.net/worlds/v1/{0}/join/pc".format(id),cookies=self.cookie).json()["address"]
