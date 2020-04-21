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
import logging

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #


def main_click(verbose, single, timeout, pages):
    """
    Entry point for click cli program
    :param verbose: verbose logging flag
    :param single: single ended BFS or double ended BFS flag
    :param timeout: timeout time in seconds
    :param pages: start and stop pages'
    """
    main(verbose, single, timeout, pages[0], pages[1])

# ================================================== #


def main_py(argv):
    """
    Entry point for python program
    :param argv: system arguments
    """
    if len(argv) != 2:
        args = len(argv)
        raise TypeError(f"input expected 2 arguments, got {args}")
    main(False, False, -1, argv[0], argv[1])

# ================================================== #


def main(verbose, single, timeout, start, stop):
    """
    Unified main function
    :param verbose: verbose logging flag
    :param single: single ended BFS or double ended BFS flag
    :param timeout: timeout time in seconds
    :param start: start page
    :param stop: stop page
    """
    if verbose:
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

    logging.info("Checking if source page is formatted as URL")
    # Validates/formats start link
    if "http" in start:
        if "en.wikipedia.org/wiki/" not in start:
            raise ValueError(f"{start} is not a valid wikipedia page")
    else:
        logging.info("Reformatting source page")
        start = "/".join(["https://en.wikipedia.org/wiki", start.replace(" ", "_")])

    logging.info("Checking if target page is formatted as URL")
    # Validates/formats stop link
    if "http" in stop:
        if "en.wikipedia.org/wiki/" not in stop:
            raise ValueError(f"{stop} is not a valid wikipedia page")
    else:
        logging.info("Reformatting target page")
        stop = "/".join(["https://en.wikipedia.org/wiki", stop.replace(" ", "_")])

    logging.info("Initializing search object")
    # Runs path search
    solver = WikiSolver(start, stop, verbose, single, timeout)
    solver.start_search()

# ================================================== #
#                       MAIN                         #
# ================================================== #


if __name__ == "__main__":
    main_py(sys.argv[1:])

# ================================================== #
#                        EOF                         #
# ================================================== #
