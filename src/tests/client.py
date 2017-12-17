
import requests
import json
import os

SERVER = "http://127.0.0.1:5000"
BASE_URL = SERVER + "/api/v1"
EXAMPLES_PATH = os.path.join(os.path.pardir, "examples")


access_token = None
session = requests.session()
#session.headers["Content-Type"] = "application/json"

# authenticate
resp = session.post(BASE_URL + "/auth/login", data={"login": "root", "password": "password"})
content = json.loads(resp.content.decode())
session.headers["Authorization"] = "JWT " + content["access_token"]


resp = session.get(BASE_URL + "/users/1")
print(resp.content.decode("utf-8"))


resp = session.get(BASE_URL + "/users/self")
print(resp.content.decode("utf-8"))