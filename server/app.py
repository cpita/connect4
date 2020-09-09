import json
import numpy as np
from flask import Flask, jsonify
from flask.globals import request
from flask_cors import CORS

from core import mcts, alpha_beta, get_action_space, flatten, simulate_move

AB_DIFFICULTIES = {
    '1': 4,
    '2': 5,
    '3': 6,
    '4': 7,
    '5': 8
}

MCTS_DIFFICULTIES = {
    '1': 100,
    '2': 200,
    '3': 500,
    '4': 1000,
    '5': 2000
}

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    board = np.reshape(np.array(list(map(lambda x: int(x), request.args.get('board').split(',')[:-1]))), (6, 7))
    algorithm = request.args.get('algorithm')
    difficulty = request.args.get('difficulty')

    turn = 1 if len(np.where(np.reshape(board, (42,)) != 0)[0]) % 2 == 0 else -1
    response = {}
    if len(np.where(np.reshape(board, (42,)) != 0)[0]) < 3:
        response['action'] = 3
        return response
    if algorithm == 'mcts':
        tree = mcts(board, turn, MCTS_DIFFICULTIES[difficulty])
        actions = get_action_space(board)
        np.random.shuffle(actions)
        next_idxs = [np.where(np.all(tree[:, :-2]==flatten(simulate_move(board.copy(), action, turn)),axis=1))[0][0] for action in actions]
        values = [tree[i, -2] for i in next_idxs]
        if turn == 1:
            best_action = actions[np.argmax(values)]
        else:
            best_action = actions[np.argmin(values)]
        response['action'] = int(best_action)
    elif algorithm == 'ab':
        _, action = alpha_beta(turn, board, 1, turn * np.inf, AB_DIFFICULTIES[difficulty])
        response['action'] = int(action)

    return jsonify(response)





if __name__ == '__main__':
    tmp = np.zeros([6, 7])
    print('Starting numba compilation...')
    alpha_beta(1, tmp, 1, np.inf, 5)
    mcts(tmp, 1, 1000)
    print('Finished numba compilation')
    app.run()