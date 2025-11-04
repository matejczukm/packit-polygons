# Gamified packing of geometric objects

This repository contains code that was developed for the engineering thesis by the same title by Piotr Kosakowski and Michał Matejczuk, written under the supervision of prof. dr hab. Jarosław Grytczuk at the Technical University of Warsaw.

The project introduces PackIt! games played on a triangular and hexagonal grid. It utilises AlphaZero algorithm for training game models that acquire good results at finding winning strategies for several variant/board size configurations.

## PackIt! games

The developed games are insipired by the original idea presented by T. Garrison et. al. in [this paper](https://arxiv.org/pdf/2403.12195).

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


