# 2048_AI

I initiated this project with the primary goal of achieving the highest possible score using an AI in the game 2048.

Throughout the development of this project, I explored various strategies and techniques to enhance the performance of my AI. Below, you will find a comprehensive summary of my results, each of which has been rigorously tested across 100 games:

| Strategy                                     | Execution Time | Max Score | Average Score |
| ------------------------------------------ | :-------------: | :-------: | :-----------: |
| [**Random Choices**](#random-choices)      |      7.3 sec    |   2 728   |     937       |
| [**Prioritization**](#prioritization)      |      8.0 sec    |   6 316   |     1 795     |
| [**Reinforcement Learning**](#reinforcement-learning) | 25.9 sec | 21 452  | 5 857 |
| [**Reinforcement Learning with Optimizations**](#reinforcement-learning-with-optimizations) | 53.8 sec | 32 024 | 12 226 |

For your information, achieving a 2048 tile in the game usually requires approximately 20,000 points.

## Random Choices

The first thing I tested was random actions. At this stage, the AI would randomly select one of the available moves. As a reminder, there are 4: Up, Down, Left and Right. I discovered with this method that it was possible to lose without having a tile of at least 128 ^^

## Prioritization

The first significant strategy I implemented was a prioritization strategy. In other words, my AI gave preference to specific moves following this order:

- Down
- Left
- Right
- Up
  
As long as it could move downwards, the AI would prioritize the downward direction. If that option was no longer available, it would then prioritize moving to the left, and so on. The goal was to minimize upward movements (a move only considered when no other moves were possible). 

With this AI, I attempted to replicate a strategy commonly used by humans: guiding the largest tile into a corner and keeping it there. However, it's worth noting that my AI's performance with this strategy is well below that of human players.

## Reinforcement Learning

#TODO

(First version of RL)

## Reinforcement Learning with Optimizations

This strategy uses Reinforcement Learning with new rewards and specific hyperparameter optimizations.

Weights: {'border': 0.96, 'biggest_adjacents': 0.806, 'future_merges': 0.388, 'empty_cells': 0.445, 'full_line': 0.509, 'weighted_sum': 0.139}