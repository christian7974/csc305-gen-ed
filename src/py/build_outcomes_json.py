import argparse
import json
from outcomes import bitset_to_outcomes, OUTCOME_TO_BIT, COMPLETE


def get_parser() -> argparse.ArgumentParser:
    """
	Get the argument parser.

	Returns
	-------
		The argument parser.
	"""
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str)
    return parser


def main() -> None:
    """
	Builds the search JSON file.
	"""

    # Parse the arguments.
    parser = get_parser()
    args = parser.parse_args()

    # Compute the lookup tables.
    db = {
        "outcome_to_bit": OUTCOME_TO_BIT,
        "bitset_to_outcomes": {
            b: bitset_to_outcomes(b)
            for b in range(COMPLETE + 1)
        }
    }

    # Write the tables to a file.
    with open(args.file_path, "w") as f:
        json.dump({"outcomes": {"2023": db}}, f)
    


if __name__ == "__main__":
    main()