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
from multiprocessing import Process, Manager

# ================================================== #
#                      CLASSES                       #
# ================================================== #


class WikiSolver:
    def __init__(self, start, stop, verbose=False, single=False, timeout_limit=-1):
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

    def verify_ends(self, double=True):
        logging.info("Verifying that source page exists")
        try:
            self.seen1.add(self.start.url)
            links = self.get_links(self.start)
            self.process_links(links, self.seen1, self.queue1, self.start)
        except Exception:
            raise ValueError(f"{self.start.url} is not a valid wikipedia page")

        logging.info("Verifying that target page exists")
        try:
            if double:
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
        self.start_time = time.time()

        with timeout(seconds=self.timeout_limit):
            if self.single:
                logging.info("Starting uniderictional BFS search")
                self.verify_ends(double=False)
                self.single_ended_search()
            else:
                logging.info("Starting bidirectional BFS search")
                self.verify_ends()
                self.double_ended_search()

    def single_ended_search(self):
        while self.queue1:
            logging.info(f"Nodes to search: {len(self.queue1)}")
            for i in range(len(self.queue1)):
                node = self.queue1.popleft()
                logging.info(f"Searching node {node.url}")
                if node.url == self.stop.url:
                    self.get_output(node)
                    return
                links = self.get_links(node)
                self.process_links(links, self.seen1, self.queue1, node)
        print("NO CONNECTION FOUND")

    def double_ended_search(self):
        while self.queue1 and self.queue2:
            logging.info(f"Nodes to search: {len(self.queue1)}")
            for i in range(len(self.queue1)):
                node = self.queue1.popleft()
                logging.info(f"Searching node {node.url}")
                if node.url == self.stop.url:
                    self.get_output(node)
                    return
                if node.url in self.seen2:
                    self.connect_path(node, self.queue2)
                    return
                links = self.get_links(node)
                self.process_links(links, self.seen1, self.queue1, node)

            logging.info(f"Nodes to search: {len(self.queue2)}")
            for i in range(len(self.queue2)):
                node = self.queue2.popleft()
                logging.info(f"Searching node {node.url}")
                if node.url in self.seen1:
                    self.connect_path(node, self.queue1, backwards=True)
                    return
                links = self.get_links(node, backwards=True)
                self.process_links(links, self.seen2, self.queue2, node)
        print("NO CONNECTION FOUND")

    def get_links(self, node, backwards=False):
        url = node.url
        if backwards:
            page_name = node.url.split("/")[-1]
            url = "".join([self.url_back, page_name, self.url_back_namespace])
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            content = soup.find(id='content')
            links = content.find_all('a', attrs={'href': re.compile("^/wiki/")})
            return [link.get('href') for link in links]
        except (ConnectionRefusedError, AttributeError):
            return []

    def process_links(self, links, seen, queue, node):
        for link in links:
            if ":" not in link:
                url = "".join([self.url_base, link])
                if url not in self.seen1:
                    seen.add(url)
                    queue.append(PageNode(url, parent=node))

    def connect_path(self, node, queue, backwards=False):
        same = None
        for i in queue:
            if i.url == node.url:
                same = i
                break

        connection = same.parent
        while connection:
            old_parent = connection.parent
            connection.parent = node
            node = connection
            connection = old_parent
        self.get_output(node, backwards=backwards)

    def get_output(self, node, backwards=False):
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
    def __init__(self, url, parent=None):
        self.url = url
        self.parent = parent


# ================================================== #
#                        EOF                         #
# ================================================== #
