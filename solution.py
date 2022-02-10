
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in this_ojb-oriented terminology: an abstract class).

    You do not need to change anything in this class, EVER.
    """
    #TODO
    def __init__(self, config):
        pass


    # TODO
    def get_start_state(self):
        """
        Returns the start state for the search problem.
        """
        util.raise_not_defined()

    # TODO
    def is_goal_state(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raise_not_defined()

    # TODO
    def get_successors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raise_not_defined()

    def get_cost_of_actions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raise_not_defined()


class Queue:
    """A container with a first-in-first-out (FIFO) queuing policy."""

    def __init__(self):
        self.list = []

    def push(self, item):
        """Enqueue the 'item' into the queue"""
        self.list.insert(0, item)

    def pop(self):
        """
            Dequeue the earliest enqueued item still in the queue. This
            operation removes the item from the queue.
        """
        return self.list.pop()

    def is_empty(self):
        """Returns true if the queue is empty"""
        return len(self.list) == 0



def breadth_first_search(problem):
    """Search the shallowest nodes in the search tree first."""


    reached = set({})
    
    frontier = Queue()
    frontier.push((problem.get_start_state(), [], 1))

    while not frontier.is_empty():
        state, path, _ = frontier.pop()
        if problem.is_goal_state(state):
            return path

        if not state in reached:
            reached.add(state)
            for successor_state, action, cost in problem.get_successors(state):
                new_path = path[:]
                new_path.append(action)
                frontier.push((successor_state, new_path, cost))

    print("FAILURE: Goal state not found")
