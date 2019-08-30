from classes import *
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("USAGE: vote_data_file results_data_file_prefix")
        quit(1)

    em = ElectionManager(sys.argv[1], sys.argv[2])

    em.run_election()


