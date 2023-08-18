"""
A collection of functions and constants to convert between outcome representations.
"""


OUTCOMES = (
	"A1", "A2", "A3", "A4",
	"B1", "B2", "B3", "B4",
	"C1", "C2", "C3", "D1",
	"GC",
)


OUTCOME_TO_BIT = {o: 1 << i for i, o in enumerate(OUTCOMES)}


COMPLETE = (1 << len(OUTCOMES)) - 1


def outcomes_to_bitset(outcomes: list[str]) -> int:
	"""
	Convert a list of unique outcomes to a bitset.
	
	Parameters
	----------
        outcomes: A list of unique outcomes.

	Returns
	-------
        A bitset representing the list of unique outcomes.
	"""
	return sum(
		OUTCOME_TO_BIT[outcome]
		for outcome in outcomes
	)


def bitset_to_outcomes(bitset: int) -> list[str]:
	"""
    Convert a bitset to a list of unique outcomes.

    Parameters
    ----------
        bitset: A bitset of outcomes.
	
	Returns
	-------
        A list of all outcomes in the bitset.
    """
	return [
		o for i, o in enumerate(OUTCOMES)
		if bitset & (1 << i) != 0
    ]
