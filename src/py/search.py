import json
import functools


# Load the course data.
with open("courses.json", "r") as f:
	courses = json.load(f)


# Map each outcome to a bit in a bitset.
outcome_to_bit = {
	"A1": 1 << 0, "A2": 1 << 1, "A3": 1 << 2, "A4": 1 << 3,
	"B1": 1 << 4, "B2": 1 << 5, "B3": 1 << 6, "B4": 1 << 7,
	"C1": 1 << 8, "C2": 1 << 9, "C3": 1 << 10, "D1": 1 << 11,
	"GC": 1 << 12,
}


def outcomes_to_bitset(outcomes):
	"""
	Given a list of unique outcomes, convert them to a bitset.
	"""
	return sum(
		outcome_to_bit[outcome]
		for outcome in outcomes
	)


# Build mapping of bitsets to outcomes for all courses.
bitset_to_outcomes = {}
for course in courses:
	bitset = outcomes_to_bitset(course["outcomes"])
	bitset_to_outcomes[bitset] = course["outcomes"]


# The full bitset.
FULL = (1 << 13) - 1


@functools.cache
def dp(s):
	"""
	Minimum number of courses to complete general education 
	outcomes not contained within the bitset s.
	"""

	# If all outcomes are completed, it takes zero 
	# courses to complete the remaining outcomes.
	if s == FULL:
		return 0

	# Otherwise, we need to take more courses. Try
	# taking each possible course and choose 
	# the one that leads to completion of all outcomes
	# in the fewest number of courses possible.
	return 1 + min(
		dp(s | b)
		for b in bitset_to_outcomes
		if (s | b) != s # Ignore courses that do not meet new outcomes.
	)


def search(completed_bitset):
	"""
	Given a set of completed outcomes, returns a list
	of course outcomes such that taking a course matching 
	any of them keep the student on track for completing
	the minimum number of general education courses.
	"""
	s = completed_bitset
	return [
		bitset_to_outcomes[b]
		for b in bitset_to_outcomes
		if dp(s | b) == dp(s) - 1 # Check if taking the course leads to minimum total courses.
	]



# Map each possible set of completed outcomes to the outcome sets that lead to an optimal path.
s_to_outcomes = {}
for completed_bitset in range(0, 1 << 13):
	s_to_outcomes[completed_bitset] = {
		"outcomes": search(completed_bitset),
		"min_courses": dp(completed_bitset),
	}


# Write the results to a file.
with open("firebase_search.json", "w") as f:
	json.dump(s_to_outcomes, f)