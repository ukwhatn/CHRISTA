import json

import requests

r = requests.post(
    "https://script.google.com/macros/s/AKfycbzfJN5vw8goZdQjHbh9GfVOjM877D1Zc0JG2s31HZCway6SJu5iMpS4WZWLAKbJsXEeJQ/exec",
    json.dumps({
        "url": "http://scp-jp-sandbox3.wikidot.com/test",
        "title": "test",
        "author": {
            "id": "test",
            "name": "test",
        },
        "category": "test",
    }),
    headers={"Content-Type": "application/json"}
)

print(r.text, r.status_code)
