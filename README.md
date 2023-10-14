# Pong Game with Q-learning

This project implements the classic Pong game using Python and applies the Q-learning algorithm to train two AI agents to play against each other.

## Description

The Pong game is a two-player sports game that simulates table tennis. Both of them have most one bullet in screen.
When your bullet hit the racket or enemy lost a ball, you get 1 score.
In this implementation, the game is designed using the Python turtle module, and two AI agents are trained to play against each other using the Q-learning algorithm.

## Requirements

- Python 3.9
- NumPy
- turtle

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone <repository_url>
cd Pong-Game-with-Q-Learning
```

### Install the required dependencies:

```bash
pip install numpy
pip install turtle
```

### Usage

Run the `game.py` script to start the pong game process

Then Run the `game_call2.py` script to start the training process for the Pong game with Q-learning:

During the training process, the trained models will be saved in the `modelAb` and `modelBb` directories.

Q-Learning table for round 10000 and 1050 are provided

else, you can just use

```bash
PongZone()
```

after Run the `game.py` script to run the game without Q-learning



### File Descriptions

* `game.py`: Implements the Pong game environment.
* `game_call2.py`: Contains the main script to train the Pong game using Q-learning.
* `README.md`: Provides information about the project.

### License

This project is licensed under the MIT License - see the [LICENSE](https://chat.openai.com/c/LICENSE) file for details.

## Acknowledgements

This project was created as part of a learning exercise and was inspired by the following resources:

- The Q-learning algorithm explanation and examples from the [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html) book by Richard S. Sutton and Andrew G. Barto.

Special thanks to the authors and contributors of the above resources for providing valuable insights and guidance.
And Sincere thanks for my friend __Houdeyfa__ coopration with me to finish this project.

