import json


FILE_PATHS = [
    "firebase_courses.json",
    "firebase_outcomes.json",
    "firebase_search.json",
]


db = {}
for file_path in FILE_PATHS:
    with open(file_path, "r") as f:
        db |= json.load(f)


with open("firebase.json", "w") as f:
    json.dump(db, f)
