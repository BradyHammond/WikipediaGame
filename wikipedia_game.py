# ================================================== #
#                  WIKIPEDIA GAME                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 04/20/2020                                #
# Last Edited: N/A                                   #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from wiki_solver import WikiSolver
import sys

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #


def mainClick(verbose, single, pages):
    start = pages[0]
    stop = pages[1]
    solver = WikiSolver(start, stop, verbose, single)

# ================================================== #


def main(argv):
    if len(argv) != 2:
        args = len(argv)
        raise TypeError(f"input expected 2 arguments, got {args}")

# ================================================== #
#                       MAIN                         #
# ================================================== #


if __name__ == "__main__":
    main(sys.argv[1:])

# ================================================== #
#                        EOF                         #
# ================================================== #
