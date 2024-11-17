import json
import os


with open("response.json", "r", encoding="utf-8") as f:

    obj = json.load(f)

with open("response.json", "w", encoding="utf-8") as wf:
    json.dump(obj,wf, indent=4)