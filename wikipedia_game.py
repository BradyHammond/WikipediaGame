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


def mainClick(verbose, single, timeout, pages):
    if verbose:
        logging.basicConfig(format='%(asctime)s:%(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)
    logging.info("Checking if source page is formatted as URL")
    start = pages[0]
    if "http" in start:
        if "en.wikipedia.org/wiki/" not in start:
            raise ValueError(f"{start} is not a valid wikipedia page")
    else:
        logging.info("Reformatting source page")
        start = "/".join(["https://en.wikipedia.org/wiki", start.replace(" ", "_")])

    logging.info("Checking if target page is formatted as URL")
    stop = pages[1]
    if "http" in stop:
        if "en.wikipedia.org/wiki/" not in stop:
            raise ValueError(f"{stop} is not a valid wikipedia page")
    else:
        logging.info("Reformatting target page")
        stop = "/".join(["https://en.wikipedia.org/wiki", stop.replace(" ", "_")])

    logging.info("Initializing search object")
    solver = WikiSolver(start, stop, verbose, single, timeout)
    solver.start_search()


# ================================================== #


def main(argv):
    if len(argv) != 2:
        args = len(argv)
        raise TypeError(f"input expected 2 arguments, got {args}")

    start = argv[0]
    if "http" in start:
        if "wikipedia.org/wiki/" not in start:
            raise ValueError(f"{start} is not a wikipedia page")

    stop = argv[1]
    if "http" in stop:
        if "wikipedia.org/wiki/" not in stop:
            raise ValueError(f"{stop} is not a wikipedia page")

    solver = WikiSolver(start, stop, verbose=False, single=False)

# ================================================== #
#                       MAIN                         #
# ================================================== #


if __name__ == "__main__":
    main(sys.argv[1:])

# ================================================== #
#                        EOF                         #
# ================================================== #
