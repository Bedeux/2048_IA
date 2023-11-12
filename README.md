# 2048 AI Project

Welcome to my 2048 AI project! This project is dedicated to creating the most powerful artificial intelligence for the popular game 2048. The primary objective is to develop an AI algorithm (with Reinforcement Learning) capable of achieving high scores.

### How to Play

Before delving into the details of the AI project, an understanding of the rules of the 2048 game is essential. The following section offers an overview of the gameplay and objectives.

In 2048, a tile-matching puzzle game, the objective is to reach the coveted 2048 tile. The game unfolds on a 4x4 grid, where players combine tiles with identical numbers by moving them in four directions: up, down, left, and right. When two tiles bearing the same number collide, they merge into a single tile with a value equal to the sum of the originals.

New tiles, valued at either 2 or 4, materialize on the board after each move. The challenge lies in strategically merging tiles to construct larger numbers and clear space on the board. The game concludes when the grid is full, and no further moves are possible.

While the primary aim is to achieve the 2048 tile, players can continue to pursue higher-numbered tiles, striving for the highest possible score (the score is determined by the sum of all tile values on the board).

Here's a visual representation of the game:

<img src="https://github.com/Bedeux/2048_IA/assets/77120351/cfde807d-30bb-4115-962a-74654301d8ef" width="400">

## Results Overview

Throughout the development of this project, I explored various strategies and techniques to enhance the performance of my AI. Below, you will find a comprehensive summary of my results, each of which has been rigorously tested across 100 games:

| Strategy                                     | Max Tile Value | Max Score | Average Score |
| ------------------------------------------ | :-------------: | :-------: | :-----------: |
| [**Random Choices**](#random-choices)      |      256   |   2 704   |     869       |
| [**Prioritization**](#prioritization)      |      512    |   7 532   |     1 908     |
| [**Reinforcement Learning**](#reinforcement-learning) | 1024 | 13 792  | 5 839 |
| [**Reinforcement Learning with Optimizations**](#reinforcement-learning-with-optimizations) | 2048 | 32 440 | 12 011 |

For your information, achieving a 2048 tile in the game usually requires approximately 20 000 points.

## Random Choices

After setting up the game in Python, the first thing I tested was random actions. At this stage, the AI would randomly select one of the available moves. As a reminder, there are 4: Up, Down, Left and Right. I discovered with this method that it was possible to lose without having a tile of at least 128 ^^

Here are my top 3 scores out of 100 games: 

![Random Backgound OK](https://github.com/Bedeux/2048_IA/assets/77120351/0d166e4f-1d06-4419-9e76-8a48bbf2d100)

## Prioritization

The first significant strategy I implemented was a prioritization strategy. In other words, my AI gave preference to specific moves following this order:

- Down
- Left
- Right
- Up
  
As long as it could move downwards, the AI would prioritize the downward direction. If that option was no longer available, it would then prioritize moving to the left, and so on. The goal was to minimize upward movements (a move only considered when no other moves were possible). 

With this AI, I attempted to replicate a strategy commonly used by humans: guiding the largest tile into a corner and keeping it there. However, it's worth noting that my AI's performance with this strategy is well below that of human players.

![Prioritization Background OK](https://github.com/Bedeux/2048_IA/assets/77120351/42bf070e-df81-4f15-99b5-ac39c2615ee1)

## Reinforcement Learning

I initiated this project with the goal of delving into reinforcement learning, and the game 2048 presented itself as an ideal testing ground. Initially, I attempted to construct a Q-Table, only to realize the immense number of possible positions in this game—amounting to billions. Consequently, I pivoted towards a simpler strategy focusing on immediate rewards.

In each position within the 2048 game, I analyze up to four potential moves, comparing the rewards associated with each to determine and select the optimal move.

Here an example :

![2048 Rewards](https://github.com/Bedeux/2048_IA/assets/77120351/76ccdd30-e17a-4ec5-9c81-6d0f3b354bd5)

#TODO

![RL V1 Background OK](https://github.com/Bedeux/2048_IA/assets/77120351/f34070cf-f8af-4d4c-beb8-901536aec196)

## Reinforcement Learning with Optimizations

This strategy uses Reinforcement Learning with new rewards and specific hyperparameter optimizations.

Weights: {'border': 0.96, 'biggest_adjacents': 0.806, 'future_merges': 0.388, 'empty_cells': 0.445, 'full_line': 0.509, 'weighted_sum': 0.139}

![RL V2 Background OK](https://github.com/Bedeux/2048_IA/assets/77120351/7b8b9331-c38d-4838-befe-2b05bf6a7cfe)
