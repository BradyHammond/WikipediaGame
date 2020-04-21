# ================================================== #
#              COMMAND LINE INTERFACE                #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 04/20/2020                                #
# Last Edited: N/A                                   #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

import click
import version
from wikipedia_game import main_click

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #


@click.command()
@click.version_option(version=version.__version__)
@click.option('--verbose', is_flag=True, help="Increase verbosity of messages.")
@click.option('--single-ended/--double-ended', default=True, help="Run breadth first search from start page only or run"
                                                                  " breadth first search from start and end pages "
                                                                  "simultaneously.")
@click.option('--timeout', '-t', default=60, type=int, help="Override default timeout duration. Use -1 for no timeout")
@click.argument('pages', type=str, nargs=2)
def main(verbose, single_ended, timeout, pages):
    """
    Command line interface for Wiki Game as defined here: https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game.
    :param verbose: verbose logging flag
    :param single_ended: single ended BFS or double ended BFS flag
    :param timeout: timeout time in seconds
    :param pages: start and stop pages'
    """
    main_click(verbose, single_ended, timeout, pages)

# ================================================== #
#                        EOF                         #
# ================================================== #
