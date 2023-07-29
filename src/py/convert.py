import json

with open("courses.json", "r") as f:
	d = json.load(f)
out = {
	"courses": {
		"2023": {

		}
	}
}
o = out["courses"]["2023"]

for c in d:
	major = c["code"][:3]
	if major not in o:
		o[major] = {}
	o[major][c["code"]] = c
	del c["code"]

with open("firebase_courses.json", "w") as f:
	json.dump(out, f)