# Wikipedia Game

### Overview
This project implements the Wiki Game outlined [here](https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game). The object of 
the game is to try and find a connection between two Wikipedia pages in as little time and as few clicks as possible.

### Installation
To install this project first checkout the git repository:
```
$ git clone https://github.com/BradyHammond/wikipedia_game.git
```
This project requires Python3. If needed you can download that [here](https://www.python.org/downloads/). It is 
recommended that you run this project in a virtual environment. To setup a Python virtual environment you will need to 
install virtualenv:
```
$ pip3 install virtualenv
```
Next navigate into the project repo and start a virtual environment:
```
$ cd WikipediaGame
$ virtualenv -p python3 venv
$ source venv/bin/activate
```
With a virtual environment setup you can now download the project dependencies:
```
$ pip3 install -r requirements.txt
```
The program can now be run using Python in the command line. Alternatively, for a more robust CLI you can install the
project using pip3:
```
$ pip3 install .
```
If you plan on modifying the project, consider using the editable flag when pip installing.

### Usage
If running without a pip installation use the following format:
```
$ python3 wikipedia_game.py "PAGE1" "PAGE2"
```
where PAGE1 and PAGE2 are two different wikipedia pages. If using the pip installed version, you can use the command:
```
$ wiki "PAGE1" "PAGE2"
```
where again PAGE1 and PAGE2 are two different wikipedia pages. Further options for the robust CLI can be found below:
```
Options:
  --version                       Show the version and exit.
  --verbose                       Increase verbosity of messages.
  --single-ended / --double-ended
                                  Run breadth first search from start page
                                  only or run breadth first search from start
                                  and end pages simultaneously.

  -t, --timeout INTEGER           Override default timeout duration. Use -1
                                  for no timeout.

  --help                          Show this message and exit.
```
### Teardown
When you are finished with the project don't forget to deactivate your virtual environment. You can do so by running the 
following command:
```
$ deactivate
```

### Notes
I did try a couple additional implementations. First, I attempted to use Wikipedia's API, but that proved to be too 
slow. Then, I also tried using processes from the multiprocessing library to speed up gathering links. Unfortunately, I 
ran into the issue of figuring out how to share the queue. It was easy to use a manager to create a shared list, but I 
kept running having problems when trying to translate the shared list back into my queue. For any questions about my 
thought process or final implementation feel free to reach out to me directly.