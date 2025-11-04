# Gamified packing of geometric objects

This repository contains code that was developed for the engineering thesis by the same title by Piotr Kosakowski and Michał Matejczuk, written under the supervision of prof. dr hab. Jarosław Grytczuk at the Technical University of Warsaw.

The project introduces PackIt! games played on a triangular and hexagonal grid. It utilises AlphaZero algorithm for training game models that acquire good results at finding winning strategies for several variant/board size configurations.

## PackIt! games

The developed games are insipired by the original idea presented by T. Garrison et al. in [this paper](https://arxiv.org/pdf/2403.12195).

Originally, PackIt! is a two-player game where players alternately place tiles on a quadratic grid of some given size, under the following constraints:
1. On the _i_-th turn, the active player has to place a tile covering _i_ or _i+1_ squares.
2. The tiles have to be rectangular.
3. The tiles placed  by players can't overlap with tiles placed in previous turns.
If a player can't make a legal move, they lose the game - in other words, last player to place a tile wins.

We introduce two new variants of the game by changing the geometry of the boards.
### Triangular variant
The game is played on a triangular grid, costricted into the shape of a triangle. Same rules apply as in the original game, however we slightly modify constraints 1 and 2:
1. On the _i_-th turn, the active player has to place a tile covering _i_ or _i+1_ **triangles**.
2. The tiles have to be **convex shapes**.

### Hexagonal variant
The game is played on a hexagonal grid, costricted into the shape of a quasi-hexagon (if the edges of the board were smoothed, it would be a hexagon). Same rules apply as in the original game, however we slightly modify constraints 1 and 2:
1. On the _i_-th turn, the active player has to place a tile covering _i_ or _i+1_ **hexes**.
2. The tiles have to be **approximately convex shapes** (a line segment between any two centers of the covered hexes lies entirely in the interior of the tile).

## Implementation
The games are designed mainly to work with [this general AlphaZero implementation](https://github.com/suragnair/alpha-zero-general), but a UI has also been added. The games and a model training framework are also available as a pip package:
```pip install polygonal-packit```
A hosted web application that allowed playing 1v1 or against AI agents is currently unavailable.

### AI agents
We used Google Deepmind's AlphaZero algorithm for training our game models. We are extremely thankful to the authors of [this general implementation of the algorithm](https://github.com/suragnair/alpha-zero-general) that made it possible.
As there is no expert knowledge or expert players available for our games, we decided to set the goals of model training utilising the conclusions of Zermelo's theorem. According to the theorem, under a number of constraints that our games satisfy, one of the players (starting or non-starting) has a perfect winning strategy. This meant that for our models to be considered "good" at the game, they would have to win close to 100% of games in one starting configuration, and as much as possible in the other configuration.
We tested the models against random agents, minimax algorithm (with depth constraints due to complexity) and human players. The results for selected variants and board sizes are presented below:

1. Against a random agents:

| Board Type | Win rate when starting | Win rate when not starting | Total win rate |
| :--- | :---: | :---: | :---: |
| Triangular 4 | 46% | 100% | 73% |
| Triangular 5 | 100% | 68% | 84% |
| Triangular 6 | 84% | 96% | 90% |
| Hexagonal 4 | 72% | 98% | 85% |
| Hexagonal 5 | 66% | 96% | 81% |
| Hexagonal 6 | 82% | 88% | 85% |

2. Against minimax (depth in parentheses):

| Board Type | Win rate when starting | Win rate when not starting | Total win rate |
| :--- | :---: | :---: | :---: |
| Triangular 4 (3) | 0% | 100% | 50% |
| Triangular 5 (2) | 100% | 80% | 90% |
| Triangular 6 (2) | 78% | 82% | 80% |
| Hexagonal 4 (2) | 84% | 100% | 92% |
| Hexagonal 5 (2) | 76% | 92% | 84% |
| Hexagonal 6 (1) | 50% | 74% | 62% |

3. Against human players:

| Board Type | Win rate when starting | Win rate when not starting | Total win rate |
| :--- | :---: | :---: | :---: |
| Triangular 4 | 17/38 | 15/15 | 60% |
| Triangular 5 | 14/15 | 9/17 | 72% |
| Triangular 6 | 15/24 | 14/16 | 73% |
| Hexagonal 4 | 12/19 | 13/16 | 71% |
| Hexagonal 5 | 8/10 | 6/6 | 88% |
| Hexagonal 6 | 3/7 | 7/8 | 67% |
