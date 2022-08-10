# pythonSnake
OOP Doubly Linked Snake, drawn using CMU 112 Graphics Module

run 'python -m pip install -r requirements.txt' to install the required packages

run snakeGame.py to play the game

Misc Notes:

First project using python to practice OOP and doubly linked list.

A snake is stored as a linked list of segments which contains a head, a tail, and corners where the snake has turned. Each segment contains coordinate and direction attribute.

When moving, head and tail segment coordinates are modified. If the tail passes the second last segment, pop the tail.

When changing directions or eating an apple, add a new head to the beginning of the list.

Create and update a set of all snake coordinates and check after each movement is head is in the set to determine when the snake eats itself.

Snakes are drawn as connecting lines, extrapolating all segments from the segments stored in the linked list.
