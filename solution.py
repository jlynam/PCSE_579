import heapq

import time

INITIAL_STATE = [0, 3, 4, 3, 0, 5, 6, 5, 0, 1, 2, 1, 0, 7, 8, 7, 0, 9, 10, 9, 0, 1, 2, 1]

def is_goal_state(state, goal_state=None):
    """
    state: Search state

    Returns True if and only if the state is a valid goal state.
    """
    if goal_state is not None:
        return state == goal_state
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

class PriorityQueue:
    """
        Implements a priority queue data structure. Each inserted item
        has a priority associated with it and the client is usually interested
        in quick retrieval of the lowest-priority item in the queue. This
        data structure allows O(1) access to the lowest-priority item.
    """

    def __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild
        # the heap. If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)


def flatten(state):
    string = [str(x) for x in state]
    full_string = ""
    for s in string:
         full_string += s
    return int(full_string)

def breadth_first_search(init_state):
    num_nodes = 0
    reached = set({})
    
    frontier = Queue()
    frontier.push((init_state, [], 1))
    
    while not frontier.is_empty():
        num_nodes += 1

        state, path, _ = frontier.pop()
        if is_goal_state(state):
            print(f"BFS expanded {num_nodes=}")
            return path

        if get_cost_of_actions(path) < 16 and not flatten(state) in reached:
            reached.add(flatten(state))
            for successor_state, action, cost in get_successors(state):
                new_path = path[:]
                new_path.append(action)
                frontier.push((successor_state, new_path, cost))

    print("FAILURE: Goal state not found")


def out_of_place_left(state):
    out_of_place = sum([1 for p, gt in zip(state, INITIAL_STATE) if p != gt])
    return out_of_place


def out_of_place_right(state, target_state):
    out_of_place = sum([1 for p, gt in zip(state, target_state) if p != gt])
    return out_of_place

def a_star_search(initial_state, goal_state=INITIAL_STATE, heuristic=out_of_place_left):
    """Search the node that has the lowest combined cost and heuristic first."""

    num_nodes = 0
    reached = set()

    frontier = PriorityQueue()
    if heuristic is out_of_place_right:
        h_cost = heuristic(initial_state, goal_state)
    else:
        h_cost = heuristic(initial_state)
    frontier.push((initial_state, [], h_cost), h_cost)

    while not frontier.is_empty():
        num_nodes += 1
        state, path, path_cost = frontier.pop()
        if is_goal_state(state, goal_state):
            print(f"A* expanded {num_nodes=}")
            return path

        if not flatten(state) in reached:
            reached.add(flatten(state))
            for successor_state, action, cost in get_successors(state):
                new_path = path[:]
                new_path.append(action)
                if heuristic is out_of_place_right:
                    h_cost = heuristic(successor_state, goal_state)
                else:
                    h_cost = heuristic(successor_state)
                frontier.update((successor_state, new_path, path_cost + cost), path_cost + cost + h_cost)

def bidirectional_a_star_search(initial_state, left_heuristic=out_of_place_left, right_heuristic=out_of_place_right):
    num_nodes = 0

    reached_left = set()
    frontier_left = PriorityQueue()
    h_cost_left = left_heuristic(initial_state)
    frontier_left.push((initial_state, [], h_cost_left), h_cost_left)

    target_state_right = initial_state
    reached_right = set()
    frontier_right = PriorityQueue()
    h_cost_right = right_heuristic(INITIAL_STATE, target_state_right)
    frontier_right.push((initial_state, [], h_cost_right), h_cost_right)

    target = None
    while not frontier_left.is_empty() and not frontier_right.is_empty():
        # Left
        num_nodes += 1
        state, path, path_cost = frontier_left.pop()
        if flatten(state) in reached_right:
            target = state
            break
        
        if not flatten(state) in reached_left:
            reached_left.add(flatten(state))
            for successor_state, action, cost in get_successors(state):
                new_path = path[:]
                new_path.append(action)
                h_cost = left_heuristic(successor_state)
                frontier_left.update((successor_state, new_path, path_cost + cost), path_cost + cost + h_cost)

        # Right
        num_nodes += 1
        state, path, path_cost = frontier_right.pop()
        if flatten(state) in reached_left:
            target = state
            break

        if not flatten(state) in reached_right:
            reached_right.add(flatten(state))
            for successor_state, action, cost in get_successors(state):
                new_path = path[:]
                new_path.append(action)
                h_cost = right_heuristic(successor_state, target_state_right)
                frontier_right.update((successor_state, new_path, path_cost + cost), path_cost + cost + h_cost)

    if target is not None:
        print("initial_state", initial_state)
        print("target", target)
        print("goal_state", INITIAL_STATE)
        left_path = a_star_search(initial_state, target, heuristic=left_heuristic) 
        print(f"{left_path=}")
        right_path = a_star_search(INITIAL_STATE, target, heuristic=right_heuristic)
        print(f"{right_path=}")
        right_path.reverse()
        path = left_path + right_path
        print(f"Bidirectional A* expanded {num_nodes=}")
        return path
    print("Failure: No path was found")


def invert_path(path):
    new_path = []
    for action in path:
        if action == 1:
            new_path.append(3)
        elif action == 2:
            new_path.append(4)
        elif action == 3:
            new_path.append(1)
        else:
            new_path.append(2)

    return new_path

def bidirectional_bfs(initial_state):
    num_nodes = 0
    reached_l = {}
    reached_r = {}

    q_l = Queue()
    q_r = Queue()

    q_l.push((initial_state, [], 1))
    q_r.push((INITIAL_STATE, [], 1))

    
    while not q_l.is_empty() and not q_r.is_empty():
        
        state_l, path_l, cost_l = q_l.pop()
        if flatten(state_l) in reached_r:
            path_r = reached_r[flatten(state_l)]
            path_r = invert_path(path_r)
            path_r.reverse()
            path = path_l + path_r
            print(path)
            print(f"Bi-BFS expanded {num_nodes=}")
            return path
        if not flatten(state_l) in reached_l:
            num_nodes += 1
            reached_l[flatten(state_l)] = path_l
            for successor_state, action, cost in get_successors(state_l):
                new_path_l = path_l[:]
                new_path_l.append(action)
                q_l.push((successor_state, new_path_l, cost))



        state_r, path_r, cost_r = q_r.pop()
        if flatten(state_r) in reached_l:
            
            path_l = reached_l[flatten(state_r)]
            path_r = path_r
            path_r = invert_path(path_r)
            path_r.reverse()
            path = path_l + path_r
            print(path)
            print(f"Bi-BFS expanded {num_nodes=}")
            return path
        if not flatten(state_r) in reached_r:
            num_nodes += 1
            reached_r[flatten(state_r)] = path_r
            for successor_state, action, cost in get_successors(state_r):
                new_path_r = path_r[:]
                new_path_r.append(action)
                q_r.push((successor_state, new_path_r, cost))

    print("no solution found")


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
    

