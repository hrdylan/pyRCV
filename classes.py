#classes for pyRCV
# classes for pyRCV
import warnings
import csv
import copy
import json
HEADER_KEY = "SubmissionId"
HEADER_SEPARATOR = "-"

class Voter:

    def __init__(self, votes, id):
        """
        :param votes: a list of the full set of the voter's candidate preferences (list<int>).
        :param id: the voter's numeric identifier (int)
        """
        self.votes = votes
        self.id = id
        if len(self.votes) > 0:
            self.curr_vote = 0
        else:
            warnings.warn("Voter created with no votes (votes = [])", UserWarning)

    def __str__(self):
        return str(self.id) + ":" + str(self.votes)

    def get_vote(self):
        """
        Description: Returns the votes current candidate preference.
        :return: candidate_id (int)
        """
        return self.votes[self.curr_vote]

    def incr_curr_vote(self):
        """
        Description: increments the voter's curr_vote to the next candidate 
        :return: void
        """

        if self.curr_vote + 1 >= len(self.votes):
            warnings.warn("Attempted to increment curr_vote out of bounds of self.votes, function call had no effect ",
                          UserWarning)
            return "failure"
        else:
            self.curr_vote += 1
            return "success"


class Candidate:

    def __init__(self, name, candidate_id):
        """
        :param name: the candidate's name (str)
        :param candidate_id: the candidate's numeric identifier (int)
        """
        self.name = name
        self.candidate_id = candidate_id


class RoundResults:

    def __init__(self, round, election_title):
        self.election_title = election_title
        self.round = round
        self.candidates = None
        self.vote_counts = {}
        self.vote_counts_ids = {}
        self.winner = None
        self.m_set = None

    def to_dict(self):
        results = {}
        results["election"] = self.election_title
        results["round"] = self.round
        results['winner'] = self.winner
        results['counts'] = self.vote_counts
        if self.m_set:
            results['eliminated'] = list(self.m_set)
        return results

    def to_json(self): 
        with open(self.election_title + "_" + str(self.round) +".json", "w+") as json_file:
            json_results = {}
            json_results["election"] = self.election_title
            json_results["round"] = self.round
            json_results['winner'] = self.winner
            json_results['counts'] = self.vote_counts
            if self.m_set:
                json_results['eliminated'] = list(self.m_set)
            return json.dump(json_results, json_file)

    def to_csv(self):
        with open(self.election_title + "_" + str(self.round) +".csv", "w+") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Election Title", self.election_title])
            writer.writerow(["Winner", self.winner])
            writer.writerow(["Round", self.round])
            writer.writerow(["Candidates", self.candidates])
            for cand in self.vote_counts:
                writer.writerow([cand, str(self.vote_counts[cand])])
            for cand in self.vote_counts_ids:
                writer.writerow([cand])
                for voter in self.vote_counts_ids[cand]:
                    writer.writerow([voter])
            writer.writerow(["Eliminated Candidates", self.m_set])

    def __str__(self):
        ids = {key: [voter.id for voter in self.vote_counts_ids[key]] for key in self.vote_counts_ids.keys()}
        return "Round %s\nVote Counts: %s\nVote Counts by Id: %s\nWinner: %s\nMinimum Candidates: %s" % (str(self.round), str(self.vote_counts), str(ids), str(self.winner), str(self.m_set))


class VotesParser:

    def __init__(self, vote_file):
        self.vote_file = vote_file
        self.file_lines = []
        self.get_lines()
        self.elections = self.get_elections()

    def print_csv(self, csv_file_path):
        with open(csv_file_path) as csv_file:
            reader = csv.reader(csv_file)
            for line in reader:
                print(line)

    def get_lines(self):
        with open(self.vote_file) as csv_file:
            reader = csv.reader(csv_file)
            self.file_lines = []

            if len(self.file_lines) > 0:
                warnings.warn("VoteParser tried to write over its data (action prevented).", RuntimeWarning)
                return

            for line in reader:
                self.file_lines.append(line)

    def get_elections(self):
        header = []

        # grab header from the lines of the file
        for line in self.file_lines:
            if line[0] == HEADER_KEY:
                header = line
        elections = {}
        for i in range(len(header)):
            column = header[i]
            if column == HEADER_KEY:
                continue
            else:
                election_title = column.split(HEADER_SEPARATOR)[0]  # this line is tailored to specific csv format
                if election_title not in elections:
                    elections[election_title] = [i]
                else:
                    elections[election_title].append(i)

        # check election columns are consecutive
        for election_title in elections.keys():
            columns = elections[election_title]
            for i in range(len(columns) - 1):
                if int(columns[i]) + 1 != int(columns[i + 1]):
                    warnings.warn("Voting results from individual election are not consecutive in csv file", RuntimeWarning)

        return elections

    def separate_csv(self):
        for election in self.elections.keys():
            csv_file = open(str(election) + "-data.csv", "w+")
            columns = self.elections[election]
            writer = csv.writer(csv_file)

            # iterate through all lines in file
            for line in self.file_lines:

                # get voter data for this election and write it to file
                if line[0].isdigit():
                    new_line = [line[0]]
                    for column in columns:
                        new_line.append(line[column].strip())
                    writer.writerow(new_line)


class ElectionManager:

    def __init__(self, vote_file, output_prefix, v=True):
        """
        :param vote_file: path to the file containing votes for the election
        """
        self.vote_file = vote_file
        self.f_candidates = self.get_candidates()  # list, remains unmodified

        if v:
            print("Candidates Found", self.f_candidates)
        self.candidates = self.get_candidates()  # list of names of all candidates in election currently, is modified

        self.voters = self.get_voters()  # list

        if v:
            print("Number of Voters:", len(self.voters))

        self.round_results = [] # results of each election round
        self.output_prefix = output_prefix
    

    def get_candidates(self):
        candidates = []
        with open(self.vote_file) as csv_file:
            reader = csv.reader(csv_file)
            for line in reader:
                if len(line) <= 1:
                    warnings.warn("vote file:" + self.vote_file + " does not contain data", RuntimeWarning)
                    print(line)
                    exit(1)

                if not line[0].isdigit():
                    warnings.warn("ID column does not contain numeric data", RuntimeWarning)
                    print(line)
                    exit(1)

                for column in line[1:]:

                    if column not in candidates and column != '':
                        candidates.append(column)

        return candidates

    def get_voters(self, v=False):
        voters = []
        count_empty = 0
        with open(self.vote_file) as csv_file:
            reader = csv.reader(csv_file)
            for line in reader:
                if len(line) <= 1:
                    warnings.warn("vote file:" + self.vote_file + " does not contain data", RuntimeWarning)
                    exit(1)
                while '' in line:
                    line.remove('')

                if len(line) > 1:
                    voters.append(Voter(line[1:], int(line[0])))
                if len(line) <= 1:
                    count_empty += 1
        if v:
            print("empty votes", count_empty)
        return voters

    def run_election(self):
        round_count = 1
        while self.run_round(round_count) is None:
            round_count += 1

        results = {'rounds': []}
        for round in self.round_results:
            results['rounds'].append(round.to_dict())
        print(json.dumps(results))


    def run_round(self, number, v=False):

        """
        Description: runs a single round of RCV
        :return: None or name of winning candidate
        """
        if v:
            print("Round", number)
        # dictionaries mapping candidate strings to counts or lists of voter objects
        vote_counts = {candidate: 0 for candidate in self.candidates}
        vote_counts_ids = {candidate: [] for candidate in self.candidates}

        # results object for the round
        results = RoundResults(number, self.output_prefix)
        results.candidates = copy.deepcopy(self.candidates)

        # count votes for each candidate
        for voter in self.voters:

            # make sure candidate str is in vote_counts
            if voter.get_vote() not in vote_counts.keys():
                if voter.get_vote() not in self.f_candidates:
                    warnings.warn("voter has a vote that does not match any candidate", RuntimeWarning)
                    print(voter.get_vote())
                    exit(1)

            else:

                # add one to the candidate's tally and add the voter to the list of voters for that candidate
                vote_counts[voter.get_vote()] += 1
                vote_counts_ids[voter.get_vote()].append(voter)

        # add counts and lists to results object
        results.vote_counts = vote_counts
        results.vote_counts_ids = vote_counts_ids

        # check if a candidate won
        for candidate in vote_counts.keys():
            if vote_counts[candidate] > len(self.voters)/2:
                results.winner = candidate
                self.round_results.append(results)
                return candidate

        # no candidate achieved a majority, find candidates with least votes
        m_set = get_min_set(vote_counts)
        results.m_set = m_set

        # check edge cases
        if len(m_set) == len(self.candidates):
            print("All candidates have same vote counts")
            print(vote_counts)
            self.round_results.append(results)
            return "All candidates tied"

        if len(m_set) > 1:
            print("Tie for last place")
            self.round_results.append(results)
            return "All candidates tied"

        # eliminate those candidates
        for candidate in m_set:
            self.candidates.remove(candidate)

        # increment voter preferences to next valid candidate
        for candidate in m_set:
            for voter in vote_counts_ids[candidate]:
                while voter.get_vote() not in self.candidates:

                    # voter has run out of votes, stop incrementation
                    # occurs when a voter has not entered the full number of preferences
                    status = voter.incr_curr_vote()
                    if status == "failure":
                        break

        self.round_results.append(results)
        return None


def get_min_set(dict):
    """
    :param dict: dictionary with integers as values
    :return: the set of keys that have the minimum value in the dict
    """
    m = min(dict, key=dict.get)
    m_set = set()
    for key in dict.keys():
        if dict[key] == dict[m]:
            m_set.add(key)
        if dict[key] < dict[m]:
            warnings.warn("builtin min() failed to find minimum value in dictionary", RuntimeWarning)
    return m_set