# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


#####################################################
#####################################################
# Please enter the number of hours you spent on this
# assignment here
num_hours_i_spent_on_this_assignment = 20
#####################################################
#####################################################

#####################################################
#####################################################
# Give one short piece of feedback about the course so far. What
# have you found most interesting? Is there a topic that you had trouble
# understanding? Are there any changes that could improve the value of the
# course to you? (We will anonymize these before reading them.)
"""
<Your feedback goes here>
This course has been refreshing. I enjoy having a different focus for each of the lectures
(where on Monday, high level concepts are explained, Wednesday, examples are done, and on Friday
we get to apply and share our knowledge). 

The most interesting topic that I've found so far has been the games and adversarial search topics 
covered in class. 

I'm still having some trouble with understanding the concepts behind state spaces. 

As for improvements made to the class, I often re-watch
lectures online and find that when participants write on the board, I can't see what they're writing
as the camera does not focus on the white board, but rather on the projector. It would be nice to 
have students write on the projector so what they're writing is more visible.

"""
#####################################################
#####################################################



"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Question 1.1
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print ( problem.getStartState() )
    print ( problem.isGoalState(problem.getStartState()) )
    print ( problem.getSuccessors(problem.getStartState()) )

    """
    "*** YOUR CODE HERE ***"


    startPos = problem.getStartState()      # stores the initial position
    currPos = problem.getStartState()       # stores the current position while going through maze
    exploredPos = []
    exploredPos.append(startPos)

    # Defining the fringe using Stack to enable elements to be pushed on
    pushVariable = (startPos, [])       # where the list contains directions for pacman to move
    fringe = util.Stack()
    fringe.push(pushVariable)

    while not fringe.isEmpty() and not problem.isGoalState(currPos):
        currNode, actions = fringe.pop()
        successors = problem.getSuccessors(currNode)
        exploredPos.append(currPos)

        for item in successors:
            location = item[0]
            if location not in exploredPos:
                currPos = item[0]          # stores value of currPos for use in pushVariable below
                direction = item[1]

                returnList = actions + [direction]
                fringe.push((currPos, returnList))

    return returnList




def breadthFirstSearch(problem):
    """Question 1.2
     Search the shallowest nodes in the search tree first.
     """
    "*** YOUR CODE HERE ***"

    startPos = problem.getStartState()
    exploredPos = []
    exploredPos.append(startPos)

    pushVariable = (startPos, [])
    fringe = util.Queue()
    fringe.push(pushVariable)

    while not fringe.isEmpty():
        currNode, actions = fringe.pop()

        if problem.isGoalState(currNode):
            return actions

        successors = problem.getSuccessors(currNode)

        for item in successors: 
            currPos = item[0]
            if not currPos in exploredPos:
                # startPos = item[0]
                direction = item[1]
                exploredPos.append(currPos)
                returnList = actions + [direction]

                fringe.push((currPos, returnList))
    return actions



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Question 1.3
    Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    startPos = problem.getStartState()
    exploredPos = []
    
    fringe = util.PriorityQueue()
    fringe.push((startPos, []), heuristic(startPos, problem))

    while not fringe.isEmpty():
        currNode, actions = fringe.pop()
    
        if problem.isGoalState(currNode):
            return actions
        
        if currNode not in exploredPos:
            successors = problem.getSuccessors(currNode)

            for item in successors:
                location = item[0]
                if location not in exploredPos:
                    directions = item[1]
                    totalActions = actions + [directions]
                    fn = problem.getCostOfActions(totalActions) + heuristic(location, problem)
                    fringe.push((location, actions + [directions]), fn)
        exploredPos.append(currNode)
    return actions



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
