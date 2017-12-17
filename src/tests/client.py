import requests
import os
import time

SERVER = "http://127.0.0.1:5000"
BASE_URL = SERVER + "/api/v1"
EXAMPLES_PATH = os.path.join(os.path.pardir, "examples")

access_token = None
session = requests.session()
# session.headers["Content-Type"] = "application/json"

# authenticate
resp = session.post(BASE_URL + "/auth/login", data={"login": "root", "password": "password"})
content = resp.json()
session.headers["Authorization"] = "JWT " + content["access_token"]

resp = session.get(BASE_URL + "/users/1")
print(resp.content.decode("utf-8"))

resp = session.get(BASE_URL + "/users/self")
print(resp.content.decode("utf-8"))

resp = session.post(BASE_URL + "/tasks/", json={
    "title": "Some Title",
    "description": "Some Desc",
    "prority": "high",
    "deadline": "2017-12-17T11:01:55",
    "subscribers_visibility": "title_only",
    "public_visibility": "presence_only",
})
json = resp.json()
task_id = json["data"]["id"]
print(json)

time.sleep(2)
resp = session.put(BASE_URL + "/tasks/%s" % task_id, json={
    "title": "Some Title 2 ",
    "description": "Some Desc 2",
    "prority": "medium",
    "deadline": "2018-12-17T11:01:55",
    "subscribers_visibility": "presence_only",
    "public_visibility": "invisible",
})
print(resp.json())

resp = session.put(BASE_URL + "/tasks/%s/start" % task_id)
print(resp.json())
resp = session.put(BASE_URL + "/tasks/%s/pause" % task_id)
print(resp.json())
resp = session.put(BASE_URL + "/tasks/%s/finish" % task_id)
print(resp.json())

resp = session.get(BASE_URL + "/users/self/tasks")
print(resp.content.decode("utf-8"))

resp = session.delete(BASE_URL + "/tasks/%s" % task_id)
print(resp.content.decode("utf-8"))

resp = session.delete(BASE_URL + "/tasks/%s" % task_id)
print(resp.content.decode("utf-8"))

resp = session.get(BASE_URL + "/users/self/tasks")
print(resp.content.decode("utf-8"))
