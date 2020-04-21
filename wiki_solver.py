# ================================================== #
#                     WIKI SOLVER                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 04/20/2020                                #
# Last Edited: N/A                                   #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from timeout import timeout
import logging
import time
from collections import deque
import requests
from bs4 import BeautifulSoup
import re

# ================================================== #
#                      CLASSES                       #
# ================================================== #


class WikiSolver:
    """ Class for finding path between two wikipedia pages"""
    def __init__(self, start, stop, verbose=False, single=False, timeout_limit=-1):
        """
        Initializes WikiSolver object
        :param start: start page
        :param stop: stop page
        :param verbose: verbose logging flag
        :param single: single ended BFS or double ended BFS flag
        :param timeout_limit: timeout time in seconds
        """
        self.start = PageNode(start)
        self.stop = PageNode(stop)
        self.verbosity = verbose
        self.single = single
        self.timeout_limit = timeout_limit
        self.start_time = None
        self.queue1 = deque()
        self.queue2 = deque()
        self.seen1 = set()
        self.seen2 = set()
        self.url_base = "https://en.wikipedia.org"
        self.url_back = "https://en.wikipedia.org/w/index.php?title=Special%3AWhatLinksHere&target="
        self.url_back_namespace = "&namespace=0"

    def verify_ends(self):
        """
        Verifies that the start page and stop page are valid wikipedia pages
        """
        logging.info("Verifying that source page exists")
        # Attempts to access start page and scrape all links
        try:
            self.seen1.add(self.start.url)
            links = self.get_links(self.start)
            self.process_links(links, self.seen1, self.queue1, self.start)
        except Exception:
            raise ValueError(f"{self.start.url} is not a valid wikipedia page")

        logging.info("Verifying that target page exists")
        # Attempts to access stop page (scrapes links if double ended BFS flag is set)
        try:
            if not self.single:
                self.seen1.add(self.stop.url)
                links = self.get_links(self.stop, backwards=True)
                self.process_links(links, self.seen2, self.queue2, self.stop)
            else:
                request = requests.get(self.stop.url)
                if request.status_code != 200:
                    raise ValueError(f"{self.start.url} is not a valid wikipedia page")
        except Exception:
            raise ValueError(f"{self.start.url} is not a valid wikipedia page")

    def start_search(self):
        """
        Starts searching for path between pages
        """
        self.start_time = time.time()

        with timeout(seconds=self.timeout_limit):
            self.verify_ends()
            if self.single:
                logging.info("Starting unidirectional BFS")
                self.single_ended_search()
            else:
                logging.info("Starting bidirectional BFS")
                self.double_ended_search()

    def single_ended_search(self):
        """
        Performs unidirectional BFS
        """
        while self.queue1:
            logging.info(f"Nodes to search: {len(self.queue1)}")
            # Cycle through links at current depth
            for i in range(len(self.queue1)):
                node = self.queue1.popleft()
                logging.info(f"Searching node {node.url}")
                # Look for stop page
                if node.url == self.stop.url:
                    self.get_output(node)
                    return
                # Add new links to next level
                links = self.get_links(node)
                self.process_links(links, self.seen1, self.queue1, node)
        print("NO CONNECTION FOUND")

    def double_ended_search(self):
        """
        Performs bidirectional BFS
        """
        while self.queue1 and self.queue2:
            logging.info(f"Nodes to search: {len(self.queue1)}")
            # Cycle through links at current depth from start
            for i in range(len(self.queue1)):
                node = self.queue1.popleft()
                logging.info(f"Searching node {node.url}")
                # Look for stop page (ensures page isn't missed if directly connected)
                if node.url == self.stop.url:
                    self.get_output(node)
                    return
                # Look for connection between other end of search
                if node.url in self.seen2:
                    self.connect_path(node, self.queue2)
                    return
                # Add new links to next level
                links = self.get_links(node)
                self.process_links(links, self.seen1, self.queue1, node)

            logging.info(f"Nodes to search: {len(self.queue2)}")
            # Cycle through links at current depth from stop
            for i in range(len(self.queue2)):
                node = self.queue2.popleft()
                logging.info(f"Searching node {node.url}")
                # Look for connection between other end of search
                if node.url in self.seen1:
                    self.connect_path(node, self.queue1, backwards=True)
                    return
                # Add new links to next level
                links = self.get_links(node, backwards=True)
                self.process_links(links, self.seen2, self.queue2, node)
        print("NO CONNECTION FOUND")

    def get_links(self, node, backwards=False):
        """
        Collects all links from webpage
        :param node: page node
        :param backwards: work backwards flag
        """
        url = node.url
        if backwards:
            # References "What links here" page for given article
            page_name = node.url.split("/")[-1]
            url = "".join([self.url_back, page_name, self.url_back_namespace])
        # Attempts to scrape links from webpage
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            content = soup.find(id='content')
            links = content.find_all('a', attrs={'href': re.compile("^/wiki/")})
            return [link.get('href') for link in links]
        except (ConnectionRefusedError, AttributeError):
            return []

    def process_links(self, links, seen, queue, node):
        """
        Saves new links to specified queue and updates seen list
        :param links: links to be processed
        :param seen: list of previously seen links
        :param queue: queue of links on next search level
        :param node: page node
        :return:
        """
        for link in links:
            # Removes special wikipedia links (i.e. "Category:")
            if ":" not in link:
                url = "".join([self.url_base, link])
                if url not in self.seen1:
                    seen.add(url)
                    queue.append(PageNode(url, parent=node))

    def connect_path(self, node, queue, backwards=False):
        """
        Connects paths of bidirectional BFS
        :param node: page node
        :param queue: queue to search through
        :param backwards: output backwards flag
        """
        # Look through queue to find connecting node object
        same = None
        for i in queue:
            if i.url == node.url:
                same = i
                break

        # Link nodes back to other end
        connection = same.parent
        while connection:
            old_parent = connection.parent
            connection.parent = node
            node = connection
            connection = old_parent
        self.get_output(node, backwards=backwards)

    def get_output(self, node, backwards=False):
        """
        Prints output of search
        :param node: page node
        :param backwards: output backwards flag
        """
        logging.info(f"Formatting Output")
        result = deque()
        while node is not None:
            if backwards:
                result.append(node.url.split("/")[-1])
            else:
                result.appendleft(node.url.split("/")[-1])
            node = node.parent
        print(" -> ".join(result))
        print("Elapsed Search Time: " + str(round(time.time() - self.start_time, 2)) + "s")

# ================================================== #


class PageNode:
    """Class for page nodes (turn links into graph structure)"""
    def __init__(self, url, parent=None):
        """
        Initializes PageNode object
        :param url: url of page
        :param parent: previous page node
        """
        self.url = url
        self.parent = parent


# ================================================== #
#                        EOF                         #
# ================================================== #
