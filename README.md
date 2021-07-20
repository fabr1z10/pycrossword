# pycrossword

Crossword Generation Library

This is a Python library that can create crossword puzzles, starting from a grid and a dictionary of words and clues. Once built and installed, 
you can import the library by using

	import pycrossword

You can create an empty grid by instatiating one grid class as in the following snippet:

	grid = cw.Grid(6, 6, [1, 4, 2, 3, 3, 2, 4, 1])

The Grid class takes in 3 arguments:

- the width of the grid;
- the height of the grid;
- the list of black cells, each one identified by a pair of integers indicating its row and column.



