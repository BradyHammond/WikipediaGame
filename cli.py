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

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #


@click.command()
@click.version_option(version=version.__version__)
@click.option('--verbose', is_flag=True, help="Increase verbosity of messages.")
@click.option('--single-ended/--double-ended', default=True, help="Run breadth first search from start page only or run"
                                                                  " breadth first search from start and end pages "
                                                                  "simultaneously.")
@click.argument('pages', type=str, nargs=2)
def main(verbose, single_ended, pages):
    """Command line interface for Wiki Game as defined here: https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game."""
    print(pages[0])
    print(pages[1])

# ================================================== #
#                        EOF                         #
# ================================================== #
