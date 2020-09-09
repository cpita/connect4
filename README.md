# Connec4 AI

### Play the game of connect4 against a human-level agent

There are two algorithms implemented, Minimax with Alpha Beta prunning and Monte Carlo Tree Search (the latter plays better).

The level of difficulty corresponds to the depth examined in Minimax and to the number of simulations performed in MCTS.

Try it out [here](https://cpita.github.io/connect4)

Note that all computation is performed on the server side and the client just makes API calls, so the response time will depend on your network speed and the number of connections with the server.
