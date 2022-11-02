import numpy as np
from typing import List, Tuple

# helper function: generate list of preferred genders 
def get_pref_list(gender_pref, person):
    pref = ["Nonbinary"]
    if gender_pref[person] == "Men":
        pref.append("Male")
    elif gender_pref[person] == "Women":
        pref.append("Female")
    elif gender_pref[person] == "Bisexual":
        pref.append("Male")
        pref.append("Female")
    return pref

# helper function: check if two people match each others gender prefs
def matches_prefs(gender_id, gender_pref, a, b):
    a_prefs = get_pref_list(gender_pref, a)
    b_prefs = get_pref_list(gender_pref, b)
    return gender_id[a] in b_prefs and gender_id[b] in a_prefs
    

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    N = len(scores) # total number of people
    unmatched = list(range(N)) # initialize list of unmatched people
    proposals = [[0 for j in range(N)] for i in range(N)] # list of list of people who've they've proposed to
    matches = []

    # every person has already rejected themselves
    for person in range(N):
        proposals[person][person] = 1

    # loop through proposal matrix
    for proposer in range(N):
        for acceptor in range(N):
            # if proposer is acceptor
            if proposer == acceptor:
                continue
                
            # the person we're trying to match has already proposed to this person
            if proposals[proposer][acceptor] == 1:
                continue
            # gender-prefs match
            elif matches_prefs(gender_id, gender_pref, proposer, acceptor):
                # person is unmatched
                if person in unmatched:
                    matches.append((curr, person))

    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
