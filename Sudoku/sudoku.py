#!/usr/bin/python3

import sys, getopt
#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
# num_hours_i_spent_on_this_assignment = 0
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
# <Your feedback goes here>
"""

I appreciate that Professor Libbrecht actually listens to our feedback and immediately
puts that feedback into action as opposed to waiting until next semester.

"""
#####################################################
#####################################################

def main(argv):
   inputfile = ''
   N=0
   try:
      opts, args = getopt.getopt(argv,"hn:i:",["N=","ifile="])
    #   print ("OPTS: ", opts)
    #   print ("ARGS: ", args)
   except getopt.GetoptError:
      print ('sudoku.py -n <size of Sodoku> -i <inputputfile>')
      sys.exit(2)
   for opt, arg in opts:
    #    print ("OPT: ", opt)
    #    print ("ARG: ", arg)
       if opt == '-h':
           print ('sudoku.py  -n <size of Sodoku> -i <inputputfile>')
           sys.exit()
       elif opt in ("-n", "--N"):
           N = int(arg)
       elif opt in ("-i", "--ifile"):
           inputfile = arg
#    print ("INPUTFILE: ", inputfile)
   instance = readInstance(N, inputfile)
#    print ("INSTANCE: ", instance)
   toCNF(N,instance,inputfile+str(N)+".cnf")
#    print ("TOCNF: ",  toCNF(N,instance,inputfile+str(N)+".cnf")) 



def readInstance (N, inputfile):
    if inputfile == '':
        return [[0 for j in range(N)] for i in range(N)]
    with open(inputfile, "r") as input_file:
        instance =[]
        for line in input_file:
            number_strings = line.split() # Split the line on runs of whitespace
            numbers = [int(n) for n in number_strings] # Convert to integers
            if len(numbers) == N:
                instance.append(numbers) # Add the "row" to your list.
                # print ("NUMBER_STRINGS_BEFORE_ELSE: ", number_strings)
            else:
                print("Invalid Sudoku instance!")
                sys.exit(3)
            # print ("NUMBER_STRINGS_AFTER_ELSE: ", number_strings)
        # print ("NUMBER_STRINGS_OUTER: ", number_strings)
        return instance # a 2d list: [[1, 3, 4], [5, 5, 6]]


# The definition of a clause may extend beyond a single line of text.

# The definition of a clause is terminated by a final value of 0.

# The file terminates after the last clause is defined.

""" Question 1 """
def toCNF (N, instance, outputfile):
    """ Constructs the CNF formula C in Dimacs format from a sudoku grid."""
    """ OUTPUT: Write Dimacs CNF to output_file """
    output_file = open(outputfile, "w")
    "*** YOUR CODE HERE ***"

    total_variables = N*N*N
    total_clauses = 0
    
    final_clauses = []

    # i = x coordinate
    # j = y coordinate
    # k = value at x,y coordinate
    # N = size of puzzle    

    # Constraint 1
    # Each cell contains at least one copy of any number

    for i in range(1, N+1):
        for j in range(1, N+1):
            clause = ""
            for k in range (1, N+1):
                clause += str(assignNumber(i,j,k,N)) + " "
            
            clause += "0\n"
            final_clauses.append(clause)
            total_clauses += 1

    # Constraint 2
    # Each cell contains at most one copy of any number

    for i in range(1, N+1):
        for j in range(1, N+1):
            for k in range(1, N+1):
                for l in range(k+1, N+1):
                    clause = ""
                    clause += str(-assignNumber(i,j,k,N)) + " "
                    clause += str(-assignNumber(i,j,l,N)) + " "
                    clause += "0\n"
                    final_clauses.append(clause)
                    total_clauses += 1

    # Constraint 3
    # No two fields in any column contain the same value

    for i in range(1, N+1):
        for k in range(1, N+1):
            for j1 in range(1, N+1):
                for j2 in range(j1+1, N+1):
                    clause = ""
                    clause += str(-assignNumber(i,j1,k,N)) + " "
                    clause += str(-assignNumber(i,j2,k,N)) + " "
                    clause += "0\n"
                    final_clauses.append(clause)
                    total_clauses += 1

    # Constraint 4
    # No two fields in any row contain the same value

    for j in range(1, N+1):
        for k in range(1, N+1):
            for i1 in range(1, N+1):
                for i2 in range(i1+1, N+1):
                    clause = ""
                    clause += str(-assignNumber(i1,j,k,N)) + " "
                    clause += str(-assignNumber(i2,j,k,N)) + " "
                    clause += "0\n"
                    final_clauses.append(clause)
                    total_clauses += 1 

    # Constraint 5
    # Ensure that solution matches original puzzle
    
    for y in range(0, len(instance)):
        for x in range(0, len(instance[y])):
            currentInstance = instance[y][x]
            if (currentInstance != 0):
                final_clauses.append(str(assignNumber(x+1,y+1,currentInstance,N)) + " 0\n")
                total_clauses += 1
    
    # Formatting CNF document
    output_file.write("c " + str(outputfile) + "\n")
    output_file.write("p cnf " + str(total_variables) + " " + str(total_clauses) + "\n")

    for i in range(0, len(final_clauses)-1):
        output_file.write(final_clauses[i])
    
    last_line = final_clauses[len(final_clauses)-1].strip('\n')
    output_file.write(last_line)


    "*** YOUR CODE ENDS HERE ***"
    output_file.close()


# Converts coordinates and value to index
def assignNumber (i, j, k, N):
    input_num = (i - 1)*(N*N) + (j - 1)*(N) + (k-1) + 1
    return input_num

if __name__ == "__main__":
   main(sys.argv[1:])
