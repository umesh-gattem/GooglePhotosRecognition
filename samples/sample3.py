import json

with open("GooglePhotos.json", "r") as file:
    print(json.load(file))