#!/usr/bin/python3

import sys
import random
import math
import time
import numpy as matrix

#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 30
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
#####################################################
#####################################################



# Outputs a random integer, according to a multinomial
# distribution specified by probs.
# Multinomial distribution is a generalization of the 
# binomial distribution. For example, it models the 
# probability of counts for rolling a k-sided die n times.
def rand_multinomial(probs):
    # Make sure probs sum to 1
    # print("THIS IS PROBS: ", probs)
    assert(abs(sum(probs) - 1.0) < 1e-5)
    rand = random.random()                  # Return the next random floating point number in the range [0.0, 1.0)
    for index, prob in enumerate(probs):
        if rand < prob:
            return index
        else:
            rand -= prob
    return 0

# Outputs a random key, according to a (key,prob)
# iterator. For a probability dictionary
# d = {"A": 0.9, "C": 0.1}
# call using rand_multinomial_iter(d.items())
def rand_multinomial_iter(iterator):
    rand = random.random()
    for key, prob in iterator:
        if rand < prob:
            return key
        else:
            rand -= prob
    return 0

class HMM():

    def __init__(self):
        self.num_states = 2
        self.prior = [0.5, 0.5]
        self.transition = [[0.999, 0.001], [0.01, 0.99]]
        self.emission = [{"A": 0.291, "T": 0.291, "C": 0.209, "G": 0.209},
                         {"A": 0.169, "T": 0.169, "C": 0.331, "G": 0.331}]

    # Generates a sequence of states and characters from
    # the HMM model.
    # - length: Length of output sequence
    def sample(self, length):
        sequence = []
        states = []
        rand = random.random()
        cur_state = rand_multinomial(self.prior)
        for i in range(length):
            states.append(cur_state)
            char = rand_multinomial_iter(self.emission[cur_state].items())
            sequence.append(char)
            cur_state = rand_multinomial(self.transition[cur_state])
        return sequence, states

    # Generates a emission sequence given a sequence of states
    def generate_sequence(self, states):
        sequence = []
        for state in states:
            char = rand_multinomial_iter(self.emission[state].items())
            sequence.append(char)
        return sequence

    # Computes the (natural) log probability of sequence given a sequence of states.
    def logprob(self, sequence, states):
        ###########################################
        # Start your code
        # print("My code here")
        # print(self.emission)

        logProbability = math.log(self.prior[0])

        # i = index and nt = nucleotide 
        for i,nt in enumerate(sequence):
            if i > 0:
                logProbability += math.log(self.transition[states[i-1]][states[i]])
            logProbability += math.log(self.emission[states[i]][nt])
        return logProbability
        # logProbability = []

        # # Obtain the first state and value from the sequence of emission
        # initial_emission = self.emission[states[0]][sequence[0]]
        # logProbability.append(math.log(self.prior[0]) + math.log(initial_emission))
        # # print("initial_emission", initial_emission)
        # # print("log(self.prior[0])", math.log(self.prior[0]))
        # # print("log(initial_emission)", math.log(initial_emission))
        # # print("logProbability:", logProbability)

        # for i in range(1, len(sequence)):
        #     emission = self.emission[states[i]][sequence[i]]
        #     # Obtain chance of staying in A/T or C/G rich region if A/T or C/G respectively
        #     transition = self.transition[states[i-1]][states[i]]
        #     # print ("transition: ", self.transition[states[i-1]][states[i]])
        #     previous = logProbability[i-1]
            
        #     logProbability.append(math.log(transition) + math.log(emission) + previous)
        
        # return logProbability[len(logProbability)-1]

        # End your code
        ###########################################


    # Outputs the most likely sequence of states given an emission sequence
    # - sequence: String with characters [A,C,T,G]
    # return: list of state indices, e.g. [0,0,0,1,1,0,0,...]
    def viterbi(self, sequence):
        ###########################################
        # Start your code
        # print("My code here")
        # print("sequence[0]", sequence[0])
        # print("sequence", sequence)

        start_time = time.time()

        lenSequence = len(sequence)

        # initialize variables to grab probability of first letters of sequence 
        # for A/T and C/G rich areas
        emission0 = self.emission[0][sequence[0]]
        emission1 = self.emission[1][sequence[0]]

        # create two empty matrices with random values using numpy | #rows = num_states
        matrix0 = matrix.empty([self.num_states, lenSequence])
        matrix1 = matrix.empty([self.num_states, lenSequence])
        matrix0[0,0] = math.log(self.prior[0]) + math.log(emission0)
        matrix0[1,0] = math.log(self.prior[1]) + math.log(emission1)
        matrix1[0,0] = 0
        matrix1[1,0] = 0

        for i in range(1,lenSequence):
            for j in range(0, self.num_states):
                previousValue0 = matrix0[0][i-1]
                previousValue1 = matrix0[1][i-1]

                currEmission = self.emission[j][sequence[i]]

                currTransition0 = self.transition[0][j]
                currTransition1 = self.transition[1][j]

                probability0 = math.log(currTransition0) + previousValue0
                probability1 = math.log(currTransition1) + previousValue1
                matrix0[j,i] = max(probability0, probability1) + math.log(currEmission)
                matrix1[j,i] = matrix.argmax([probability0, probability1])

        #check to see which state has higher probabilty
        states = matrix.empty(lenSequence, int)
        states[lenSequence-1] = matrix0[:, lenSequence-1].argmax()

        for k in range(lenSequence-1, 0, -1):
            states[k-1] = matrix1[states[k],k]
        
        end_time = time.time()
        print(end_time - start_time)
        
        return states.tolist()

        # End your code
        ###########################################

def read_sequence(filename):
    with open(filename, "r") as f:
        return f.read().strip()

def write_sequence(filename, sequence):
    with open(filename, "w") as f:
        f.write("".join(sequence))

def write_output(filename, logprob, states):
    with open(filename, "w") as f:
        f.write(str(logprob))
        f.write("\n")
        for state in range(2):
            f.write(str(states.count(state)))
            f.write("\n")
        f.write("".join(map(str, states)))
        f.write("\n")

hmm = HMM()

file = sys.argv[1]
sequence = read_sequence(file)
viterbi = hmm.viterbi(sequence)
logprob = hmm.logprob(sequence, viterbi)
name = "my_"+file[:-4]+'_output.txt'
write_output(name, logprob, viterbi)


