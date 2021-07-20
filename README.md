# pycrossword

Crossword Generation Library

This is a Python library that can create crossword puzzles, starting from a grid and a dictionary of words and clues. Once built and installed, 
you can import the library by using

	import pycrossword

You can create an empty grid by instatiating one grid class as in the following snippet:

	grid = cw.Grid(13, 13, [4, 0, 5, 1, 11, 1, 2, 2, 10, 2, 9, 3, 0, 4, 8, 4, 1, 5, 7, 5, 6, 6, 5, 7, 11, 7, 4, 8, 12, 8, 3, 9, 2, 10, 10, 10, 1, 11, 7, 11, 8, 12])

The Grid class takes in 3 arguments:

- the width of the grid;
- the height of the grid;
- the list of black cells, each one identified by a pair of integers indicating its row and column.



