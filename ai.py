from lib import abstractstrategy, boardlibrary
import math


class AlphaBetaSearch:

    def __init__(self, strategy, maxplayer, minplayer, maxplies=3,
                 verbose=False):
        """"alphabeta_search - Initialize a class capable of alphabeta search
        problem - problem representation
        maxplayer - name of player that will maximize the utility function
        minplayer - name of player that will minimize the uitlity function
        maxplies- Maximum ply depth to search
        verbose - Output debugging information
        """
        # strategy
        self.strategy = strategy
        # the player we should find the best action.
        self.maxplayer = maxplayer
        # the opponent.
        self.minplayer = minplayer
        # the maximum number of depth. until we terminate search.
        self.maxplies = maxplies
        # if set to verbose is True -> print results.
        self.verbose = verbose

    def alphabeta(self, state):
        """
        Conduct an alpha beta pruning search from state
        :param state: Instance of the game representation
        :return: best action for maxplayer


        pseudopod:
        alpha-beta search(state)
        v = maxvalue(state, α=-∞, β=∞)
        return action in actions(state) with value v
        """
        v, best_action = self.maxvalue(state=state, alpha=-math.inf, beta=math.inf, ply=0)
        if best_action is None:
            if len(state.get_actions(player=self.maxplayer)) != 0:
                self.maxplies += -1
                v, best_action = self.maxvalue(state=state, alpha=-math.inf, beta=math.inf, ply=0)
            else:
                print("game is over, winner = ", self.minplayer)

        return best_action

    def cutoff(self, state, ply):
        """
        cutoff_test - Should the search stop?
        :param state: current game state
        :param ply: current ply (depth) in search tree
        :return: True if search is to be stopped (terminal state or cutoff
           condition reached)

        # check if the game is over or if we went above max_depth
        """
        # check if game is over, aka player moves list is zero or it has zero players.
        # TODO: check if state is an object of checkerboard class.
        terminal, winner = state.is_terminal()

        if terminal:
            print(" ***** game over ******, winner = ", winner)

        if ply <= self.maxplies and terminal is False and len(state.get_actions(player=self.maxplayer)) != 0:
            return False

        else:
            return True

    def maxvalue(self, state, alpha, beta, ply):
        """
        maxvalue - - alpha/beta search from a maximum node
        Find the best possible move knowing that the next move will try to
        minimize utility.
        :param state: current state
        :param alpha: lower bound of best move max player can make
        :param beta: upper bound of best move max player can make
        :param ply: current search depth
        :return: (value, maxaction)
        """
        max_action = None
        if self.cutoff(state=state, ply=ply) is True:
            v = self.strategy.evaluate(state=state)
        else:
            v = -math.inf
            for a in state.get_actions(player=self.maxplayer):
                if self.minvalue(state=state.move(move=a), alpha=alpha, beta=beta, ply=ply + 1)[0] > v:
                    v = self.minvalue(state=state.move(move=a), alpha=alpha, beta=beta, ply=ply + 1)[0]
                    max_action = a
                if v >= beta:
                    break
                else:
                    alpha = max(alpha, v)
        return v, max_action

    def minvalue(self, state, alpha, beta, ply):
        """
        minvalue - alpha/beta search from a minimum node
        :param state: current state
        :param alpha:  lower bound on best move for min player
        :param beta:  upper bound on best move for max player
        :param ply: current depth
        :return: (v, minaction)  Value of min action and the action that
           produced it.
        """
        min_action = None
        if self.cutoff(state=state, ply=ply):
            v = self.strategy.evaluate(state=state)
        else:
            v = math.inf
            for a in state.get_actions(player=self.minplayer):
                if self.maxvalue(state=state.move(move=a), alpha=alpha, beta=beta, ply=ply + 1)[0] < v:
                    v = self.maxvalue(state=state.move(move=a), alpha=alpha, beta=beta, ply=ply + 1)[0]
                    min_action = a
                if v <= alpha:
                    break
                else:
                    beta = min(beta, v)
        return v, min_action


class Strategy(abstractstrategy.Strategy):
    """Your strategy, maybe you can beat Tamara Tansykkuzhina, 
       2019 World Women's Champion
    """

    def __init__(self, *args):
        """
        Strategy - Concrete implementation of abstractstrategy.Strategy
        See abstractstrategy.Strategy for parameters
       """

        super(Strategy, self).__init__(*args)

        self.search = AlphaBetaSearch(self, self.maxplayer, self.minplayer, maxplies=self.maxplies, verbose=False)

    def play(self, board):
        """
        play(board) - Find best move on current board for the maxplayer
        Returns (newboard, action)
        """

        best_action = self.search.alphabeta(state=board)
        if best_action is None:
            return board, None
        else:
            return board.move(move=best_action), best_action

    def evaluate(self, state, turn=None):
        """
        evaluate - Determine utility of terminal state or estimated
        utility of a non-terminal state
        :param state: Game state
        :param turn: Optional turn (None to omit)
        :return:  utility or utility estimate based on strengh of board
                  (bigger numbers for max player, smaller numbers for
                   min player)
        """

        # get the number of current black and red kings on the board.
        r_king, b_king = state.get_kingsN()

        # get the number of current black and red spawn on the board.
        r_spawn, b_spawn = state.get_pawnsN()

        # how many actions available for player rn?
        if self.maxplayer == "r":
            r_len_actions = len(state.get_actions(player=self.maxplayer))
            b_len_actions = len(state.get_actions(player=self.minplayer))

        elif self.maxplayer == "b":
            r_len_actions = len(state.get_actions(player=self.minplayer))
            b_len_actions = len(state.get_actions(player=self.maxplayer))

        else:
            b_len_actions, r_len_actions = 0, 0

        # number of players at the first row, aka the guardians.
        black_gaurds = state.board[0].count('b')
        red_gaurds = state.board[-1].count('r')

        # count the number of pawns close to become king.
        black_pot_king = state.board[5].count('b') + state.board[6].count('b')
        red_pot_king = state.board[1].count('r') + state.board[2].count('r')

        # weight initializer:
        c1 = 10  # diff of kings
        c2 = 10  # diff of spawns
        c3 = 2  # number of legal actions. Is one of the players trapped?
        c4 = 2  # diff in number of guards.
        c5 = 2  # diff in potential soon to become kings.

        val = c1 * (b_king - r_king) + c2 * (b_spawn - r_spawn) + c3 * (b_len_actions - r_len_actions) + \
              c4 * (black_gaurds - red_gaurds) + c5 * (black_pot_king - red_pot_king)

        if self.maxplayer == "r":
            return -val
        elif self.maxplayer == "b":
            return val
        else:
            return False


# Run test cases if invoked as main module
if __name__ == "__main__":
    b = boardlibrary.boards["StrategyTest1"]
    redstrat = Strategy('r', b, 6)
    blackstrat = Strategy('b', b, 6)

    print(b)
    (nb, action) = redstrat.play(b)
    print("Red would select ", action)
    print(nb)

    (nb, action) = blackstrat.play(b)
    print("Black would select ", action)
    print(nb)
