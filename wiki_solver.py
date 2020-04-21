# ================================================== #
#                     WIKI SOLVER                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 04/20/2020                                #
# Last Edited: N/A                                   #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

import wikipedia
from timeout import timeout
import logging
import time
from collections import deque

# ================================================== #
#                      CLASSES                       #
# ================================================== #


class WikiSolver:
    def __init__(self, start, stop, verbose=False, single=False, timeout_limit=120):
        self.start = PageNode(start)
        self.stop = PageNode(stop)
        self.verbosity = verbose
        self.single = single
        self.timeout_limit = timeout_limit
        self.start_time = None
        self.queue1 = deque()
        self.queue2 = deque()
        self.seen = set()

    def verify_ends(self):
        logging.info("Verifying that source page exists")
        try:
            for link in wikipedia.page(title=self.start.name).links:
                self.queue1.append(PageNode(link, parent=self.start))
        except (wikipedia.PageError, wikipedia.DisambiguationError):
            raise ValueError(f"{self.start.name} is not a valid wikipedia page")

        logging.info("Verifying that target page exists")
        try:
            for link in wikipedia.page(title=self.start.name).links:
                self.queue2.append(PageNode(link, parent=self.stop))
        except (wikipedia.PageError, wikipedia.DisambiguationError):
            raise ValueError(f"{self.stop.name} is not a valid wikipedia page")

    def start_search(self):
        logging.info("Starting search")
        self.start_time = time.time()

        with timeout(seconds=self.timeout_limit):
            self.verify_ends()
            if self.single:
                self.single_ended_search()
            else:
                self.double_ended_search()

    def single_ended_search(self):
        while self.queue1:
            for i in range(len(self.queue1)):
                node = self.queue1.popleft()
                logging.info(f"Searching node {node.name}")
                self.seen.add(node.name)
                for link in wikipedia.page(title=node.name).links:
                    if link == self.stop.name:
                        self.get_output(link, node)
                        return
                    elif link not in self.seen:
                        self.queue1.append(PageNode(link, parent=node))

    def double_ended_search(self):
        pass

    def get_output(self, link, node):
        logging.info(f"Formatting Output")
        result = deque([link])
        while node.parent is not None:
            result.appendleft(node.name)
            node = node.parent
        print(" -> ".join(result))
        print("Time Elapsed: " + str(time.time() - self.start_time))

# ================================================== #


class PageNode:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent


# ================================================== #
#                        EOF                         #
# ================================================== #
