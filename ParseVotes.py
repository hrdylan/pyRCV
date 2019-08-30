from classes import *
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: vote_data_file ")
        quit(1)

    vp = VotesParser(sys.argv[1])
    vp.separate_csv()