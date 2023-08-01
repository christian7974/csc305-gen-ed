import argparse
import json
import functools
from outcomes import COMPLETE


def make_dp(bitsets: list[int]):
	"""
	Create a dynamic program to compute the minimum number of course to complete 
	the general education outcomes.

	Parameters
	----------
		bitsets: List of outcome sets that can be completed in a single course.

	Returns
	-------	
		A function that takes in a bitset of completed outcomes and returns the minimum
		number of courses to complete the remaining outcomes.
	"""

	@functools.cache
	def dp(s: int) -> int:
		"""
		Minimum number of courses to complete general education outcomes not contained 
		within the bitset of outcomes s. Note that this solves the set cover problem. 

		Parameters
		----------
			s: The bitset of completed general education outcomes.
		
		Returns
		-------
			The minimum number of course to complete the remaining general education
			outcomes.
		"""

		# If all outcomes are complete, it takes zero courses to complete all outcomes.
		if s == COMPLETE:
			return 0

		# Otherwise, we need to take more courses. Try taking each possible course and 
		# choose the one that leads to completion of all outcomes in the fewest number 
		# of courses possible.
		return 1 + min(
			dp(s | b)
			for b in bitsets
			if (s | b) != s # Ignore courses that do not meet new outcomes.
		)

	return dp


def get_parser() -> argparse.ArgumentParser:
	"""
	Get the argument parser.

	Returns
	-------
		The argument parser.
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument("courses_file_path", type=str)
	parser.add_argument("search_file_path", type=str)
	return parser


def main():
	"""
	Builds the search JSON file.
	"""

	# Parse the args.
	parser = get_parser()
	args = parser.parse_args()
	print(args)

	# Load the course data.
	with open(args.courses_file_path, "r") as f:
		db = json.load(f)["courses"]["2023"]

	# Compute the set of outcome sets that can be completed in a single course.
	bitsets = set(
		db[program][course]["outcomes"]
		for program in db
		for course in db[program]
	)

	# Build the dynamic program.
	dp = make_dp(bitsets=bitsets)

	# Build a dictionary mapping bitsets of completed outcomes to a list of course
	# outcome bitsets that will minimize the total number of required courses.
	db = {
		s: {
			"outcomes": [
				b for b in bitsets
				if dp(s | b) == dp(s) - 1
			],
			"min_courses": dp(s),
		}
		for s in range(0, COMPLETE + 1)
	}
	
	# Write the results to a file.
	with open(args.search_file_path, "w") as f:
		json.dump(db, f)


if __name__ == "__main__":
	main()
