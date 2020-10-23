"""
@author: mroch


Single Programmer Affidavit
I the undersigned promise that the attached assignment is my own work. While I was free to discuss ideas with others,
the work contained is my own. I recognize that should this not be the case, I will be subject to penalties as outlined
in the course syllabus.

Programmer: Opal Issan: Oct, 2020.

Should we implement if the players do not eat for 40 turns the game is terminated.
"""

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
if True:
    import imp
    import sys

    major = sys.version_info[0]
    minor = sys.version_info[1]
    modpath = "lib/__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
    tonto = imp.load_compiled("tonto", modpath)

# human - human player, prompts for input
from lib import human, checkerboard  # , tonto

from lib.timer import Timer


def Game(red=human.Strategy, black=tonto.Strategy,
         maxplies=10, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 

    Returns winning player 'r' or 'b'
    """
    # First create an initial board.
    if init is not None:
        board = init
    else:
        board = checkerboard.CheckerBoard()

    if verbose:
        print("Initial board\n", board)

    # Create instances of strategy.
    red_player = red('r', checkerboard.CheckerBoard, maxplies)
    black_player = black('b', checkerboard.CheckerBoard, maxplies)

    # Initialize the winner - returned 'r' or 'b' or None.
    winner = None

    ii = 0  # keep track of the number of turns.

    while board.is_terminal()[0] is False:  # the game is not over.
        # red player is the first to start.
        if firstmove == 0:
            if ii % 2 == 0:
                board, action = red_player.play(board)
                if action is None:
                    winner = 'b'
                    break
                if verbose is True:
                    print("Red player action = ", action)

            else:
                board, action = black_player.play(board)
                if action is None:
                    winner = 'a'
                    break
                if verbose:
                    print("Black player action = ", action)

        # black player is the first to start.
        else:
            if ii % 2 == 0:
                board, action = black_player.play(board)
                if action is None:
                    winner = 'r'
                    break
                if verbose:
                    print("Black player action = ", action)

            else:
                board, action = red_player.play(board)
                if action is None:
                    winner = 'b'
                    break
                if verbose:
                    print("Red player action = ", action)

        if verbose:
            print(board)

        ii += 1

    # If the winner did not win from cornering the other player,
    # check if the other player has no players left on the board.
    if winner is None:
        terminal, winner = board.is_terminal()

    # print the game.
    if verbose:
        if winner is not None:
            print("Game is over, winner is = ", winner)
        else:
            print("Game is over, resulting in a draw.")

    return winner


if __name__ == "__main__":
    # Examples
    from lib import abstractstrategy, boardlibrary
    import ai
    # Starting from specific board with default strategy
    # Game(init=boardlibrary.boards["multihop"])
    # Game(init=boardlibrary.boards["StrategyTest1"])
    # Game(init=boardlibrary.boards["EndGame1"], firstmove=0)

    # Tonto vs Tonto
    # Game(red=tonto.Strategy, black=tonto.Strategy)

    # Example using AI agent vs AI agent.
    Game(red=ai.Strategy, black=tonto.Strategy, maxplies=6, verbose=True)

