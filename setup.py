# ================================================== #
#                       SETUP                        #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 04/20/2020                                #
# Last Edited: N/A                                   #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from setuptools import setup

# ================================================== #
#                       SETUP                        #
# ================================================== #

exec(open('version.py').read())
setup(
    name='WikipediaGame',
    version=__version__,
    license='GPLv3',
    description='Implementation of Wiki Game as outlined here: https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game',
    author='Brady Hammond',
    author_email='bradymh23@gmail.com',
    url='https://github.com/BradyHammond/wikipedia_game',
    py_modules=['wikipedia_game'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Topic :: Games/Entertainment',
    ],
    install_requires=['beautifulsoup4>=4.9.0', 'certifi>=2020.4.5.1', 'chardet>=3.0.4', 'click>=7.1.1', 'idna>=2.9',
                      'requests>=2.23.0', 'soupsieve>=2.0', 'urllib3>=1.25.9', 'wikipedia>=1.4.0'],
    entry_points={
        'console_scripts': ['wiki = cli:main'],
    }
)