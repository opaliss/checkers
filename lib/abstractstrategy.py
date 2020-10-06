
class Strategy:
    """"
    Abstract strategy for playing a two player game.
    Abstract class from which specific strategies should be derived
    """
        
    def __init__(self, player, game, maxplies, verbose=False):
        """
        Initialize a strategy
        :param player: player represented by this strategy
        :param game: class or instance that supports the class or instance method
            game.other_player(player) which finds the name of the other player
        :param maxplies: maximum number of plies before a cutoff test is applied
        :param verbose: print additional (debug) information if True
        """

        # Useful for initializing any constant values or structures
        # used to evaluate the utility of a board
        self.maxplayer = player
        self.minplayer = game.other_player(player)
        self.maxplies = maxplies
        self.verbose = verbose

    def verbose(self, enabled=True):
        """
        verbose - enable/disable verbose mode
        :param enabled: True --> enabled
        :return:
        """
        self.verbose = verbose
    
    def evaluate(self, game, turn=None):
        """
        evaluate - Provide a heuristic estimate of the utility of a given
        board configuration
        :param game: Object that contains a representation of the game state
        :param turn: Player turn, must be self.maxplayer, self.minplayer, or None
            Implementations of the abstract strategy may take into account or
            ignore the player turn but they must also work if turn is set
            to the default value of None
        :return:  estimated utility of the game state
        """
        "Return the utility of the specified game"
        raise NotImplementedError("Subclass must implement")
    
    def play(self, game):
        """
        play - Determine the best move for the maxplayer to make after
        conducting analysis (e.g. a minimax search with alpha-beta pruning.
        :param game:  An instance of the class containing the game state.
        :return:  (new_game_state, action) Tuple indicating the agent's action
           and the result of applying action to game.
        """

        raise NotImplementedError("Subclass must implement")
