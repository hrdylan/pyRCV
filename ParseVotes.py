from classes import *
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("USAGE: vote_data_file parsed_elections_folder")
        quit(1)

    vp = VotesParser(sys.argv[1])
    vp.separate_csv(sys.argv[2])