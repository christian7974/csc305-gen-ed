import json
import requests
from tqdm import tqdm


# URI's 2023 course data API. Found through the course catalog page.
RAW_COURSE_URL = "https://uri.kuali.co/api/v1/catalog/courses/621d2bb525966e0c8c0a643d"
DETAILED_COURSE_URL = "https://uri.kuali.co/api/v1/catalog/course/621d2bb525966e0c8c0a643d"


# General education outcome codes.
OUTCOMES = (
	"A1", "A2", "A3", "A4",
	"B1", "B2", "B3", "B4",
	"C1", "C2", "C3", "D1",
	"GC",
)


def main():
	# Download the course data.
	print("Downloading raw course data...")
	r = requests.get(RAW_COURSE_URL)
	raw_courses = json.loads(r.content)

	# Parse the course data into a better format.
	print("Downloading course descriptions...")
	courses = []
	for raw_course in tqdm(raw_courses):

		# Download the course description.
		detailed_course_url = f"{DETAILED_COURSE_URL}/{raw_course['pid']}"
		r = requests.get(detailed_course_url)

		# Attempt to load the course descri
		try:
			detailed_course = json.loads(r.content)
		except Exception as e:
			detailed_course = {"description": ""}
			print(f"Failed to download:")
			print(f"\t\traw_course = {raw_course}")
			print(f"\t\tdetailed_course_url = {detailed_course_url}")

		# Tag course with outcomes.
		outcomes = [o for o in OUTCOMES if f"({o})" in detailed_course["description"]]

		# Format the course.
		courses.append(
			{
				"code": raw_course["__catalogCourseId"],
				"title": raw_course["title"],
				"desc": detailed_course["description"],
				"outcomes": outcomes,
			}
		)

	# Output course data to disk.
	with open("courses.json", "w") as f:
		json.dump(courses, f)


if __name__ == "__main__":
	main()