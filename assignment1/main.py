#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses

# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    # if the one person's gender is not the other person's preference, 
    # then they are not compatible at all, so the score should be 0.
    if ((user1.gender not in user2.preferences) or 
        (user2.gender not in user1.preferences)):
        return 0
    
    # calculate the number of questions they answered the same
    num_qs = len(user1.responses)
    same_ans = 0
    for q in range(num_qs):
        if user1.responses[q] == user2.responses[q]:
            same_ans += 1
    
    # the score is the percentage of questions they answered the same
    score = same_ans / num_qs

    return score
    


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
