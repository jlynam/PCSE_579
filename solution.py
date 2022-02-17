INITIAL_STATE = [0, 3, 4, 3, 0, 5, 6, 5, 0, 1, 2, 1, 0, 7, 8, 7, 0, 9, 10, 9, 0, 1, 2, 1]

def is_goal_state(state):
    """
    state: Search state

    Returns True if and only if the state is a valid goal state.
    """
    return state == INITIAL_STATE


def get_successors(state):
    """
      state: Search state

    For a given state, this should return a list of triples, (successor,
    action, stepCost), where 'successor' is a successor to the current
    state, 'action' is the action required to get there, and 'stepCost' is
    the incremental cost of expanding to that successor.
    """
    # left CW
    state_1 = state[10:12] + state[0:10] + state[12:21] + state[7:10]
    # print(state_1)
    # right CW
    state_2 = state[0:9] + state[11:23] + state[11:14]
    # print(state_2)
    # left CCW
    state_3 = state[2:12] + state [0:2] + state[12:21] + state[11:12] + state[0:2]
    # print(state_3)
    # right CCW
    state_4 = state[0:9] + state[19:21] + state[9:22]
    # print(state_4)

    return [(state_1, 1, 1), (state_2, 2, 1), (state_3, 3, 1), (state_4, 4, 1)]

def get_cost_of_actions(actions):
    """
     actions: A list of actions to take

    This method returns the total cost of a particular sequence of actions.
    The sequence must be composed of legal moves.
    """
    return len(actions)


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


def flatten(state):
    string = [str(x) for x in state]
    full_string = ""
    for s in string:
         full_string += s
    return int(full_string)

def breadth_first_search(init_state):
    reached = set({})
    
    frontier = Queue()
    frontier.push((init_state, [], 1))

    while not frontier.is_empty():
        state, path, _ = frontier.pop()
        if is_goal_state(state):
            return path

        if get_cost_of_actions(path) < 16 and not flatten(state) in reached:
            reached.add(flatten(state))
            for successor_state, action, cost in get_successors(state):
                new_path = path[:]
                new_path.append(action)
                frontier.push((successor_state, new_path, cost))

    print("FAILURE: Goal state not found")



if __name__ == "__main__":
    start_config = input("Input starting configuration.\n")
    start_config = [int(x) for x in start_config.split(" ")]
    solution = breadth_first_search(start_config)
    if solution is None:
        print("Cannot solve with given arrangement")
    else:
        print("Solution path:")
        print(solution)
        print("Length of solution path =", get_cost_of_actions(solution))
    

