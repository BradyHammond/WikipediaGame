# ================================================== #
#                       TIMEOUT                      #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 04/20/2020                                #
# Last Edited: N/A                                   #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

import signal

# ================================================== #
#                      CLASSES                       #
# ================================================== #


class timeout:
    """Class for timing out functions"""
    def __init__(self, seconds=10, error_message='search exceeded timeout limit'):
        """
        Initializes timeout object
        :param seconds: number of seconds before timeout
        :param error_message: custom error message
        """
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        """
        Raises TimeoutError on timeout
        :param signum: signal triggering event
        :param frame: stack/exception frame
        """
        raise TimeoutError(self.error_message)

    def __enter__(self):
        """
        Starts timeout clock and enables use of with statement
        """
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, type, value, traceback):
        """
        Exits timeout block and enables use of with statement
        :param type: exception type
        :param value: exception value
        :param traceback: traceback
        """
        signal.alarm(0)

# ================================================== #
#                        EOF                         #
# ================================================== #
