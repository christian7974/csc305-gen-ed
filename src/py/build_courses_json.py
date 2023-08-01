import argparse
import json
import requests
from tqdm import tqdm
from typing import Union
from outcomes import OUTCOMES, outcomes_to_bitset


# URI's 2023 course data API. Found through the course catalog page.
COURSE_URL = "https://uri.kuali.co/api/v1/catalog/courses/621d2bb525966e0c8c0a643d"
DETAILED_COURSE_URL = "https://uri.kuali.co/api/v1/catalog/course/621d2bb525966e0c8c0a643d"


def download_courses() -> list[dict]:
	"""
	Download metadata for all courses from the URI course data API.

	Returns
	-------
		List of dictionaries containing each course's metadata.
	"""
	r = requests.get(COURSE_URL)
	courses = json.loads(r.content)
	return courses


def download_description(course_pid: str) -> str:
	"""
	Download detailed metadata for a specific course from the URI course data API and
	extract the description of the course.

	Parameters
	----------
		course_pid: The PID of the course found in the course metadata.
	
	Returns
	-------
		The course description as a string.

	Raises
	------
		ValueError: The course description does not exist.
	"""
	url = f"{DETAILED_COURSE_URL}/{course_pid}"
	r = requests.get(url)
	try:
		detailed_course = json.loads(r.content)
		description = detailed_course["description"]
		return description
	except json.JSONDecodeError: 
		raise ValueError("Description does not exist.")


def extract_outcomes(desc: str) -> list[str]:
	"""
	Extract a list of all general education outcomes met by a course from the 
	course description.

	Parameters
	----------
		desc: The course description.
	
	Returns
	-------
		All general education outcomes met by the course.
	"""
	return [
		o for o in OUTCOMES
		if f"({o})" in desc
	]


# TODO: These parameters should probably be packed into a data structure.


def add_course(
		db: dict, 
		code: str, 
		title: str, 
		desc: str, 
		outcomes: Union[str, int]
	) -> dict:
	"""
	Add a course to the database dictionary.

	Parameters
	----------
		code: The course code (i.e. CSC212).
		title: The course title (i.e. Data Structures and Abstractions).
		desc: The course description.
		outcomes: The list of outcomes the course meets.
	
	Returns
	-------
		The modified database dictionary.
	"""
	program = code[:3]
	if program not in db: db[program] = {}
	db[program][code] = {
		"title": title,
		"desc": desc,
		"outcomes": outcomes,
	}
	return db


def get_parser() -> argparse.ArgumentParser:
	"""
	Get the argument parser.

	Returns
	-------
		The argument parser.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument("file_path", type=str)
	parser.add_argument("--as_bitset", type=int, default=True, required=False)
	return parser


def main():
	"""
	Builds the course JSON file.
	"""

	# Parse the arguments.
	parser = get_parser()
	args = parser.parse_args()

	# Download the course metadata.
	print("*** Downloading course metadata ***")
	courses = download_courses()

	# Download the course descriptions and construct the database.
	print("*** Downloading course descriptions ***")
	db = {}
	for course in tqdm(courses):

		# Download the course description.
		try:
			desc = download_description(course_pid=course["pid"])
		except ValueError:
			desc = ""
			print(f"Failed to download description:")
			print(f"\t\tcourse = {course}")

		# Extract the outcomes from the course description.
		outcomes = extract_outcomes(desc=desc)
		if args.as_bitset:
			outcomes = outcomes_to_bitset(outcomes=outcomes)

		# Add the course to the database.
		db = add_course(
			db=db, 
			code=course["__catalogCourseId"],
			title=course["title"],
			desc=desc,
			outcomes=outcomes,
		)

	# Output the database to disk.
	with open(args.file_path, "w") as f:
		json.dump({"courses": {"2023": db}}, f)


if __name__ == "__main__":
	main()