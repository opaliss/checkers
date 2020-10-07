'''
@author: mroch
'''

# Game representation and mechanics

# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.
import statistics

# Python can load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
# if True:
#     import imp
#     import sys
#
#     major = sys.version_info[0]
#     minor = sys.version_info[1]
#     modpath = "lib/__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
#     tonto = imp.load_compiled("tonto", modpath)

# human - human player, prompts for input
from lib import human, checkerboard  # , tonto
import ai

from lib.timer import Timer


def Game(red=human.Strategy, black=ai.Strategy,
         maxplies=6, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 

    Returns winning player 'r' or 'b'
    """
    # first create an initial board.
    if init is not None:
        board = init
    else:
        board = checkerboard.CheckerBoard()

    if verbose:
        print("initial board\n", board)

    # create instances of strategy.
    red_player = red('r', checkerboard.CheckerBoard, maxplies)
    black_player = black('b', checkerboard.CheckerBoard, maxplies)

    action=[0, 0]

    ii = 0
    while board.is_terminal()[0] is False and action is not None:  # the game is not over.
        if firstmove == 0:
            if ii % 2 == 0:
                board, action = red_player.play(board)
                if verbose is True:
                    print("Red player action = ", action)
                    print(board)
            else:
                board, action = black_player.play(board)
                if verbose:
                    print("Black player action = ", action)
                    print(board)

        else:
            if ii % 2 == 0:
                board, action = black_player.play(board)
                if verbose:
                    print("Black player action = ", action)
                    print(board)
            else:
                board, action = red_player.play(board)
                if verbose:
                    print("Red player action = ", action)
                    print(board)

        ii += 1

    if verbose:
        print("The winner is = ", board.is_terminal()[1])
    return board.is_terminal()[1]


if __name__ == "__main__":
    # Examples
    # Starting from specific board with default strategy
    # Game(init=boardlibrary.boards["multihop"])
    # Game(init=boardlibrary.boards["StrategyTest1"])
    # Game(init=boardlibrary.boards["EndGame1"], firstmove = 1)

    # Tonto vs Tonto
    # Game(red=tonto.Strategy, black=tonto.Strategy)

    # example using human.
    Game(red=ai.Strategy, black=ai.Strategy, maxplies=2, verbose=True)
