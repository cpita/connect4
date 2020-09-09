import numpy as np
from numba import jit


@jit(nopython=True)
def simulate_move(board, action, turn):
    """Returns the new board position with the desired move
    :param board: array representing the board
    :type board: np.array -> shape = (6, 7)
    :param action: integer (0 to 6) that corresponds to the column the player wants to play in
    :type action: int
    :param turn: 1 corresponds to the first player (X) and -1 to the second.
    :type turn: int
    :returns: array representing the board after the move
    :rtype: np.array -> shape = (6, 7)
    """
    i = len(np.where(board[:, action] == 0)[0]) - 1
    board[i, action] = turn
    return board


@jit(nopython=True)
def get_reward(board):
    """Returns the winner of a given board, 0 if there's a tie or None if the game has not ended
    :param board: array representing the board
    :type board: np.array -> shape = (6, 7)
    :returns: 1 if Player 1 has won, -1 if Player 2 has won, 0 if there's a tie, None otherwise
    :rtype: int or None
    """
    # Check Horizontal
    for i in range(6):
        for j in range(4):
            if abs(board[i, j] + board[i, j + 1] + board[i, j + 2] + board[i, j + 3]) == 4:
                return board[i, j]

    # Check Vertical
    for i in range(3):
        for j in range(7):
            if abs(board[i, j] + board[i + 1, j] + board[i + 2, j] + board[i + 3, j]) == 4:
                return board[i, j]

    # Check Diag
    for i in range(3):
        for j in range(4):
            if abs(board[i, j] + board[i + 1, j + 1] + board[i + 2, j + 2] + board[
                i + 3, j + 3]) == 4:
                return board[i, j]

    for i in range(3):
        for j in range(3, 7):
            if abs(board[i, j] + board[i + 1, j - 1] + board[i + 2, j - 2] + board[
                i + 3, j - 3]) == 4:
                return board[i, j]

    # Return 0 if the game is finished and it's a tie
    if len(get_action_space(board)) == 0:
        return 0


@jit(nopython=True)
def get_action_space(board):
    """Returns a list of integers corresponding to the columns that are playable i.e. not full"""
    return np.where(np.array([len(np.where(board[:, i] == 0)[0]) for i in range(7)]) != 0)[0]


@jit(nopython=True)
def rollout(board, turn):
    """Simulates a the outcome of a game by playing random actions from a given state
    :param board: array representing the board
    :type board: np.array -> shape = (6, 7)
    :param turn: 1 if it's Player 1's turn, else -1
    :type turn: int
    :returns: 1 if Player 1 wins, -1 if Player 2 wins, 0 if there's a tie.
    :rtype: int
    """
    action = np.random.choice(get_action_space(board))
    board = simulate_move(board, action, turn)
    reward = get_reward(board)
    if reward is None:
        return rollout(board, turn * (-1))
    return reward


@jit(nopython=True)
def ucb(turn, exp_value, n_parent, n):
    """Computes Upper Confidence Bound of a given state/node
    :param turn: 1 if it's Player 1's turn, else -1
    :type turn: int
    :param exp_value: the expected value obtained from the current node
    :type exp_value: float
    :param n_parent: number of times the parent node has been visited
    :type n_parent: int
    :param n: number of times the current node has been visited
    :type n: float
    :returns: UCB value of given input
    :rtype: float
    """
    if n == 0:
        return np.inf * turn
    return exp_value + 0.7 * np.sqrt((2*np.log(n_parent))/n) * turn


@jit(nopython=True)
def flatten(board):
    """Flattens a (6,7) board into a (42,) array"""
    return np.reshape(board, (42,))


@jit(nopython=True)
def find_index(tree, row):
    """Finds the row number of a given row on the tree, or returns -1 if the row is not found
    :param tree: arrray representing the tree where each row consists of one state with 44 numbers: 1-42 correspond to the board, 43 is expected value and 44 is number of visits
    :type tree: np.array -> shape = (None, 44)
    :param row: arrray representing one state with 44 numbers
    :type row: np.array -> shape = (44,)
    """
    z = np.where(np.sum(tree[:, :-2] == row, axis=1) == 42)[0]
    if len(z) > 0:
        return z[0]
    return -1


@jit(nopython=True)
def alpha_beta(minmax, board, depth, cut_off, max_depth):
    """ Applies the Minimax algorithm with Alpha-Beta prunnnig
    :param minmax: 1 if the current board corresponds to Player 1's turn (maximizes), -1 otherwise(minimizes)
    :type minmax: int
    :param board: array representing the board
    :type board: np.array -> shape = (6, 7)
    :param depth: depth of the current state in the tree
    :type depth: int
    :param cut_off: used as the cut off value for which part of the tree is prunned
    :type cut_off: value
    :param max_depth: maximum depth level that can be explored
    :type max_depth: int
    :returns: best value that can be obtained from the given board and the corresponding action
    :rtype: tuple[int]
    """
    best_value = np.inf * minmax * (-1)
    best_action = None

    actions = get_action_space(board)
    np.random.shuffle(actions)

    for action in actions:
        next_board = simulate_move(board.copy(), action, minmax)
        value = get_reward(next_board)
        if value is None:
            if depth == max_depth:
                value = 0
            else:
                value, _ = alpha_beta(minmax * (-1), next_board.copy(), depth + 1, best_value, max_depth)

        if (value > cut_off and minmax == 1) or (value < cut_off and minmax == -1):
            return np.inf * minmax, None

        if (value > best_value and minmax == 1) or (value < best_value and minmax == -1):
            best_value = value
            best_action = action
            if (best_value == 1 and minmax == 1) or (best_value == -1 and minmax == -1):
                return best_value, int(best_action)

    return best_value, int(best_action)


@jit(nopython=True)
def mcts_episode(board, turn, tree):
    """Applies one eipsode / simulation of the MCTS algorithm
    :param board: array representing the board
    :type board: np.array -> shape = (6, 7)
    :param turn: 1 if it's Player 1's turn, else -1
    :type turn: int
    :param tree: arrray representing the tree where each row consists of one state with 44 numbers: 1-42 correspond to the board, 43 is expected value and 44 is number of visits
    :type tree: np.array -> shape = (None, 44)
    :returns: reward obtained from recursively applying UCB action selection and a random rollout on the given board, and the updated MCTS tree from that episode
    :rtype: tuple
    """
    tree_idx = find_index(tree, flatten(board))

    value = get_reward(board)

    if value is None:

        if tree_idx == -1:

            value = rollout(board.copy(), turn)

        else:

            actions = get_action_space(board)
            np.random.shuffle(actions)

            prev_n_visits = tree[tree_idx, -1]
            best_value = np.inf * turn * (-1)

            for action in actions:

                child_state = simulate_move(board.copy(), action, turn)
                child_tree_index = find_index(tree, flatten(child_state))
                if child_tree_index == -1:
                    exp_value, n = 0, 0
                else:
                    exp_value, n = tree[child_tree_index, -2], tree[child_tree_index, -1]
                ucb_value = ucb(turn, exp_value, prev_n_visits, n)


                if (ucb_value > best_value and turn == 1) or (ucb_value < best_value and turn == -1):
                    best_action = action
                    best_value = ucb_value
                    if ucb_value == np.inf * turn:
                        break

            value, tree = mcts_episode(simulate_move(board.copy(), best_action, turn), turn * (-1), tree)

    if tree_idx == -1:
        prev_value, prev_n_visits = 0, 0
        n_visits = prev_n_visits + 1
        exp_value = prev_value + (1 / n_visits) * (value - prev_value)

        new_row = np.empty(shape=(1, 44))
        new_row[0, :-2] = flatten(board)
        new_row[0, -2] = exp_value
        new_row[0, -1] = n_visits
        tree = np.vstack((tree, new_row))
    else:
        prev_value = tree[tree_idx, -2]
        prev_n_visits = tree[tree_idx, -1]
        n_visits = prev_n_visits + 1
        exp_value = prev_value + (1 / n_visits) * (value - prev_value)

        tree[tree_idx, -2] = exp_value
        tree[tree_idx, -1] = n_visits

    return value, tree


def mcts(board, turn, iters):
    """Applies MCTS on a given board for a given number of iterations
    :param board: array representing the board
    :type board: np.array -> shape = (6, 7)
    :param turn: 1 if it's Player 1's turn, else -1
    :type turn: int
    :param iters: numer of MCTS iterations to perform
    :type iters: int
    :returns: tree derived from the current board, which will then be consumed using greedy action selection
    :rtype: np.array -> shape = (None, 44)
    """
    tree = np.empty(shape=(0, 44))

    for i in range(iters):
        _, tree = mcts_episode(board, turn, tree)

    return tree