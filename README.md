# Adversarial Search

In this assignment you will bring to practice the algorithms that were introduced to you during the lectures about adversarial search.  
You will implement the well known game *Tic-Tac-Toe* and apply adversarial search techniques in order to make the computer play it.

To make your life easier, there are some classes and interfaces already defined for you. Namely, a `Game` class, a `GameState` tuple as well as some minor helpers. We will go over them in detail now.

## Task 1.1



```python
#!pip install ipycanvas

from canvas import Canvas_TicTacToe
```


```python
from games import GameState, Game, Player, infinity
```

## The `GameState` Namedtuple

`GameState` is a [namedtuple](https://docs.python.org/3.5/library/collections.html#collections.namedtuple) which represents the current state of a game. Let it be Tic-Tac-Toe or any other game.

## The `Game` Class

Let's have a look at the class `Game` in our module. We see that it has functions, namely `actions`, `result`, `utility`, `terminal_test`, `to_move` and `display`.

We see that these functions have not actually been implemented. This class is actually just a template class; we are supposed to create the class for our game, `TicTacToe` by inheriting this `Game` class and implement all the methods mentioned in `Game`. Do not close the popup so that you can follow along the description of code below.


```python
%psource Game
```

Now let's get into details of all the methods in our `Game` class. You have to implement these methods when you create new classes that would represent your game.

* `actions(self, state)` : Given a game state, this method generates all the legal actions possible from this state, as a list or a generator. Returning a generator rather than a list has the advantage that it saves space and you can still operate on it as a list.


* `result(self, state, move)` : Given a game state and a move, this method returns the game state that you get by making that move on this game state.


* `utility(self, state, player)` : Given a terminal game state and a player, this method returns the utility for that player in the given terminal game state. While implementing this method assume that the game state is a terminal game state. The logic in this module is such that this method will be called only on terminal game states.


* `terminal_test(self, state)` : Given a game state, this method should return `True` if this game state is a terminal state, and `False` otherwise.


* `to_move(self, state)` : Given a game state, this method returns the player who is to play next. This information is typically stored in the game state, so all this method does is extract this information and return it.


* `display(self, state)` : This method prints/displays the current state of the game.

* `play_game` : This function is the one that will actually be used to play the game. You pass an instance of the game you want to play and the instances of the players you want in this game. Use it to play AI vs AI, AI vs human, or even human vs human matches!

## `TicTacToe` Class 

Now that you know about how to use the `Game` class, the first task is to implement the class `TicTacToe`, which has been inherited from the class `Game`.

Additional methods in TicTacToe:

* `__init__(self, h=3, v=3, k=3)` :  When you create a class inherited from the `Game` class (class `TicTacToe` in our case), you'll have to create an object of this inherited class to initialize the game. This initialization might require some additional information which would be passed to `__init__` as variables. For the case of our `TicTacToe` game, this additional information would be the number of rows `h`, number of columns `v` and how many consecutive X's or O's are needed in a row, column or diagonal for a win `k`. Also, the initial game state has to be defined here in `__init__`.


* `compute_utility(self, board, move, player)` : A method to calculate the utility of TicTacToe game. If 'X' wins with this move, this method returns 1; if 'O' wins return -1; else return 0.


* `k_in_row(self, board, move, player, delta_x_y)` : This method returns `True` if there is a line formed on the TicTacToe board with the latest move else `False.`

### GameState in TicTacToe game

Now, before we start implementing our `TicTacToe` game, we need to decide how we will be representing our game state. Typically, a game state will give you all the current information about the game at any point in time. When you are given a game state, you should be able to tell whose turn it is next, how the game will look like on a real-life board (if it has one) etc. A game state need not include the history of the game. If you can play the game further given a game state, you game state representation is acceptable. While we might like to include all kinds of information in our game state, we wouldn't want to put too much information into it. Modifying this game state to generate a new one would be a real pain then.

Now, as for our `TicTacToe` game state, would storing only the positions of all the X's and O's be sufficient to represent all the game information at that point in time? Well, does it tell us whose turn it is next? Looking at the 'X's and O's on the board and counting them should tell us that. But that would mean extra computing. To avoid this, we will also store whose move it is next in the game state.

Think about what we've done here. We have reduced extra computation by storing additional information in a game state. Now, this information might not be absolutely essential to tell us about the state of the game, but it does save us additional computation time. We'll do more of this later on.

The `TicTacToe` game defines its game state as:

`GameState = namedtuple('GameState', 'to_move, utility, board, moves')`

The game state is called, quite appropriately, `GameState`, and it has 4 variables, namely, `to_move`, `utility`, `board` and `moves`.

Below, you can find a more detailed description of each of those variables:

* `to_move` : It represents whose turn it is to move next. This will be a string of a single character, either 'X' or 'O'.


* `utility` : It stores the utility of the game state. Storing this utility is a good idea, because, when you do a Minimax Search or an Alphabeta Search, you generate many recursive calls, which travel all the way down to the terminal states. When these recursive calls go back up to the original callee, we have calculated utilities for many game states. We store these utilities in their respective `GameState`s to avoid calculating them all over again.


* `board` : A dict that stores all the positions of X's and O's on the board.


* `moves` : It stores the list of legal moves possible from the current position. Note here, that storing the moves as a list, as it is done here, increases the space complexity of Minimax Search from `O(m)` to `O(bm)`. Refer to Sec. 5.2.1 of the book.

### Representing a move in TicTacToe game

Now that we have decided how our game state will be represented, it's time to decide how our move will be represented. A move should have a representation, that makes it easy to use this move to modify a current game state in order to generate a new one.

For our `TicTacToe` game, we'll just represent a move by a `tuple`, where the first and the second elements of the tuple will represent the row and column, respectively, where the next move is to be made. Whether to make an `'X'` or an `'O'` will be decided by the `to_move` in the `GameState` namedtuple.


```python
from typing import List, Tuple, Dict

class TicTacToe(Game):
    """Play TicTacToe on an h x v board, with <first player> playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h: int = 3, v: int = 3, k: int = 3):
        """
        Args:
            h -- horizontal dimension of the board
            v -- vertical dimension of the board
            k -- how many consecutive tiles of same kind are needed for a win
        """
        # YOUR CODE HERE
        self.h = h
        self.v = v
        self.k = k
        
        self.initial = GameState(to_move='X', utility=0, board={},
                                    moves=[(x, y) for x in range(h) for y in range(v)]
                                )

    def actions(self, state: GameState) -> List[Tuple[int, int]]:
        """Legal moves are any square not yet taken.
        
        Args:
            state -- The current state of the game
        Returns:
            All leagal moves possible in the current game state.
        """
        return state.moves

    

    def result(self, state: GameState, move: Tuple[int, int]) -> GameState:
        # YOUR CODE HERE

        board = state.board.copy()
        board[move] = state.to_move
        moves = list(state.moves)
        moves.remove(move)
        next_player = 'O' if state.to_move == 'X' else 'X'
        utility = self.compute_utility(board, move, state.to_move)
        return GameState(to_move=next_player, utility=utility, board=board, moves=moves)
    

    def utility(self, state: GameState, player: str) -> int:
        """Return the utility of the current state for the respective player.
        
        Args:
            state  -- The current game state
            player -- The player whose turn it is
        Returns:
            1 for win, -1 for loss, 0 otherwise."""
        # YOUR CODE HERE
        return state.utility if player == 'X' else -state.utility

    def terminal_test(self, state: GameState) -> bool:
        """A state is terminal if it is won or there are no empty squares.
        Args:
            state: The current game state
        Returns:
            True if the current state is terminal; False otherwise.
        """
        # YOUR CODE HERE
        terminal = False
        if not state.moves:
            terminal = True
        if state.utility != 0:
            terminal = True
            
        return terminal

    def display(self, state: GameState) -> None:
        """Visualize the current game state by printing to console.
        Args:
            state: The current game state
        """
        # YOUR CODE HERE
        for x in range(self.h):
            for y in range(self.v):
                print(state.board.get((x, y), "-"), end="  ")
            print("\n")
        

    def compute_utility(self, board: Dict[Tuple[int, int], str], move: Tuple[int, int], player: str) -> int:
        """Compute the utility of a given move in a given game state.
        Args:
            board  -- The board state
            move   -- The move played
            player -- The player whose turn it is
        Returns:
            If player 'X' wins return 1; elif 'O' wins return -1; else (draw) return 0
        """
        # YOUR CODE HERE
        
        # horizontal (0, 1)
        # vertical (1, 0)
        # diagonals (1, 1), (1, -1)
        if self.k_in_row(board, move, player, (0, 1)) or \
           self.k_in_row(board, move, player, (1, 0)) or \
           self.k_in_row(board, move, player, (1, 1)) or \
           self.k_in_row(board, move, player, (1, -1)):
            return 1 if player == 'X' else -1
        return 0

    def k_in_row(self, board: Dict[Tuple[int, int], str], move: Tuple[int, int], player: str,
                 delta_x_y: Tuple[int, int]) -> bool:
        """Check whether there is a line of length k through tiles of kind player.
        Args:
            board  -- The boards state
            move   -- The move played
            player -- Player whose tiles should be checked for in_row condition
        Returns:
            If there is a line vertically, horizontally or diagonally using only tiles of the respective
            player, return True; False otherwise.
        """
        # YOUR CODE HERE
        (delta_x, delta_y) = delta_x_y
        x, y = move

        def count_step(x, y, dx, dy):
            count = 0
            while board.get((x, y)) == player:
                count += 1
                x, y = x + dx, y + dy
            return count
        
        total_in_a_row = count_step(x, y, delta_x, delta_y) + count_step(x, y, -delta_x, -delta_y)
        
        total_in_a_row -= 1
        return  total_in_a_row>= self.k
```


```python

```



## Players to play games

So, we have finished the implementation of the `TicTacToe` class. What this class does is that, it just defines the rules of the game. Now we need to create the AI that actually plays the game.

There are four players that we will define: human player, random player, minimax player and alphabeta player. Of those four players, two are already implemented for you. Namely, the `query_player` implements the human player, and the `human_player` implements a player that draws some legal move uniformly from the set of possible moves.

### Human Player
The `human_player` function allows you, a human opponent, to play the game. This function requires a `display` method to be implemented in your game class, so that successive game states can be displayed on the terminal, making it easier for you to visualize the game and play accordingly.

### Random Player
The `random_player` is a function that plays random moves in the game. That's it. There isn't much more to this guy. 

### MiniMax Player
The `MiniMax` player uses the classical Minimax algorithm to determine the best possible move in the current game state.

### AlphaBeta Player
The `AlphaBeta` player utilizes alpha-beta search on minimax to play the best move in the current game state (assuming no cutoff).


```python
from typing import Tuple
import random

def human_player(game: Game, state: GameState) -> Tuple[int, int]:
    """Make a move by querying standard input.
    Args:
        game  -- the game that is played
        state -- the current game state
    Returns:
        The move played
    """
    print("current state:")
    game.display(state)
    print("available moves: {}".format(game.actions(state)))
    print("")
    move_string = input('Your move? ')
    try:
        move = eval(move_string)
    except NameError:
        move = move_string
    return move


def random_player(game: Game, state: GameState):
    """A player that chooses a legal move at random.
    Args:
        game  -- the game that is played
        state -- the current state of the game
    Returns:
        A random move drawn uniformly from the set of legal moves.
    """
    return random.choice(game.actions(state))
```

### Implementing the MiniMax Player 

Lets start by implementing the `MiniMax` player. Below you will find a class template that defines three methods: `max_value`, `min_value` and `search`. Additionally a `__call__` function is implemented, which is used as an entry point when a player instance is passed to the `Game.play_game()` function in order to play the game.
> You do **not** have to change the `__call__` function!

Please implement the **plain** minimax algorithm using the provided template!


```python
from typing import List, Tuple, Dict, Union, Optional

class MiniMax(Player):
    
    def __init__(self, game: Optional[Game] = None):
        """
        Args:
            game -- game that is being played (can be None if the instance of the class is used with
            Game.play_game).
        """
        self.game = game
    
    def max_value(self, state: GameState, player: str) -> int:
        """The maximin value is the highest value that the player can be sure to get without knowing the actions
        of the other players; equivalently, it is the lowest value the other players can force the player to
        receive when they know the player's action.
        Args:
            state  -- The current game state
            player -- The player to consider
        Returns:
            The highest utility value a player can be sure to get independent of the actions of the other
            player.
        """
        # YOUR CODE HERE
        if self.game.terminal_test(state):
            return None, self.game.utility(state, player)
        
        
        best_move = None
        best_score = float('-inf')
        
        for move in self.game.actions(state):
            temp_move, value = self.min_value(self.game.result(state, move), player)
            
            if value > best_score:
                best_score = value
                best_move = move
        
        return best_move, best_score


    def min_value(self, state: GameState, player: str) -> int:
        """The minimax value of a player is the smallest value that the other players can force the player to
        receive, without knowing the player's actions; equivalently, it is the largest value the player can be
        sure to get when they know the actions of the other players.
        Args:
            state  -- The current game state
            player -- The player to consider
        Returns:
            The lowest utility value that the other player can force the player to receive independent of the
            actions of the other player.
        """
        # YOUR CODE HERE
        if self.game.terminal_test(state):
            return None, self.game.utility(state, player)
        
        
        best_move = None
        best_score = float('inf')
        
        for move in self.game.actions(state):
            temp_move, value = self.max_value(self.game.result(state, move), player)
            
            if value < best_score:
                best_score = value
                best_move = move
        
        return best_move, best_score


    def search(self, state: GameState) -> Tuple[int, int]:
        """Given a state in a game, calculate the best move by searching forward all the way to the terminal
        states.
        Args:
            state -- The current game state
        Returns:
            The best move.
        """
        # YOUR CODE HERE
        player = state.to_move
        best_move, best_value = self.max_value(state, player)
 
        return best_move
    
    def __call__(self, game: Game, state: GameState) -> Tuple[int, int]:
        """
            This function enables you to call a MiniMax instance like a function and is used in the play_game
            method.
        """
        self.game = game
        return self.search(state)
```


```python

```


### Implementing the AlphaBeta Player 

With the plain version of minimax implemented, now implement the enhanced version of the algorithm by using **alpha-beta-search**.

A similar template is provided to you. Please use it to implement the algorithm!

> Be aware, that since `cutoff_test` and `eval_fn` are defined as `Optional` you **need** to define a default function that takes their place if they are not given!


```python
from typing import List, Tuple, Dict, Callable, Optional

class AlphaBeta(Player):
    
    def __init__(self, d: int = 4, game: Optional[Game] = None,
                 cutoff_test: Optional[Callable] = None, eval_fn: Optional[Callable] = None):
        """
        Args:
            d    -- maximum depth to search
            game -- game that is being played (can be None if the instance of the class is used with
            Game.play_game).
            cutoff_test -- function to test whether a cutoff is reached
            eval_fn     -- function to evaluate the current state with regards to its utility
        """
        self.game = game
        self.d = d
        # YOUR CODE HERE
        self.cutoff_test = cutoff_test or self.default_cutoff
        self.eval_fn = eval_fn or self.default_eval
    
    def default_cutoff(self, state, depth):
        return depth > self.d or self.game.terminal_test(state)
    
    def default_eval(self, state):
        return  None, self.game.utility(state, state.to_move)
    
    def max_value(self, state: GameState, player: str, alpha: int, beta: int, depth: int) -> int:
        """Compute the maximin of a player. This is the highest value that the player can be sure to get
        without knowing the actions of the other players; equivalently, it is the lowest value the other
        players can force the player to receive when they know the player's action.
        Args:
            state  -- the current game state
            player -- the player whose move it is
            alpha -- minimum score that the maximizing player is assured of
            beta  -- maximum score that the minimizing player is assured of
            depth  -- current depth in the search tree
        Returns:
            The highest utility value a player can be sure to get independent of the actions of the other
            player.
        """
        # YOUR CODE HERE
        if self.cutoff_test(state, depth):
            return self.eval_fn(state)
        
        
        best_move = None
        best_score = float('-inf')
        
        for move in self.game.actions(state):
            temp_move, value = self.min_value(self.game.result(state, move), player, alpha, beta, depth + 1)
            
            if value > best_score:
                best_score = value
                best_move = move
            
            if alpha < best_score:
                alpha = best_score
            if beta <= best_score:
                return best_move, best_score            
        
        return best_move, best_score


    def min_value(self, state: GameState, player: str, alpha: int, beta: int, depth: int) -> int:
        """Compute the minimax value of a player. This is the smallest value that the other players can force
        the player to receive, without knowing the player's actions; equivalently, it is the largest value the
        player can be sure to get when they know the actions of the other players.
        Args:
            state  -- the current game state
            player -- the player whose move it is
            alpha  -- minimum score that the maximizing player is assured of
            beta   -- maximum score that the minimizing player is assured of
            depth  -- current depth in the search tree
        Returns:
            The lowest utility value that the other player can force the player to receive independent of the
            actions of the other player.
        """
        # YOUR CODE HERE
        if self.cutoff_test(state, depth):
            return self.eval_fn(state)
        
        
        best_move = None
        best_score = float('inf')
        
        for move in self.game.actions(state):
            temp_move, value = self.max_value(self.game.result(state, move), player, alpha, beta, depth + 1)
            
            if value < best_score:
                best_score = value
                best_move = move

            if beta > best_score:
                beta = best_score
            if best_score <= alpha:
                return best_move, best_score                
                
        return best_move, best_score


    def search(self, state: GameState) -> Tuple[int, int]:
        """ Implementation of alpha-beta pruning on minimax using cutoff.
        Args:
            state -- the current game state
        Returns:
            The best possible move.
        """
        # YOUR CODE HERE
        player = state.to_move
        alpha = float('-inf')
        beta = float('inf')
        best_move, best_value = self.max_value(state, player, alpha, beta, 1)
 
        return best_move
    
    def __call__(self, game: Game, state: GameState) -> Tuple[int, int]:
        """
            This function enables you to call a AlphaBeta instance like a function and is used in the play_game
            method.
        """
        self.game = game
        return self.search(state)
```


```python

```


## Playing a Game 

With all the players in place we can now play some games. Either by letting different algorithmic players play against each other, or by playing ourself.

Please implement two games:
1. `random_player` vs. `AlphaBeta`
1. `MiniMax` vs. `AlphaBeta`

Since the players given to `Game.play_game()` are always ordered, meaning that the player given as a first argument always starts, please perform each game **twice**, such that each player had the starting position once!

> **DO NOT** leave the `human_player` in the code for submission! Since the autograding will get stuck!


```python
player1 = "Random Player"
player2 = "MiniMax Player"
player3 = "AlphaBeta Player"

# YOUR CODE HERE

def print_winner(result, player_1, player_2):
    if result == 0:
        print("Result: Draw!\n ------------------------------------ \n")
    else:
        print("Result:", player_1 if result > 0 else player_2, " won!\n ------------------------------------ \n")

tictactoe = TicTacToe(3,3,3)
minimax_player = MiniMax()
alphabeta_player = AlphaBeta()


print("Random Player vs MiniMax Player")
print("X: Random Player")
print("O: AlphaBeta Player\n")
result_game_1 = tictactoe.play_game(random_player, alphabeta_player, verbose=True)
print_winner(result_game_1, player1, player3)


print("MiniMax Player vs Random Player")
print("X: MiniMax Player")
print("O: AlphaBeta Player\n")
result_game_2 = tictactoe.play_game(minimax_player, alphabeta_player, verbose=True)
print_winner(result_game_2, player2, player3)
```

    Random Player vs MiniMax Player
    X: Random Player
    O: AlphaBeta Player
    
    O  X  X  
    
    X  O  O  
    
    O  X  X  
    
    Result: Draw!
     ------------------------------------ 
    
    MiniMax Player vs Random Player
    X: MiniMax Player
    O: AlphaBeta Player
    
    X  O  O  
    
    X  X  O  
    
    X  -  -  
    
    Result: MiniMax Player  won!
     ------------------------------------ 
    
    


## Evaluating MiniMax and AlphaBeta A) 

Now lets compare the two optimal agents against one another. For this please let each agent play against another instance of itself $10$ times and record both the terminal states and the time taken for the entire game in `terminal_states` and `time_taken` respectively.

> If you want, you can also **override** the `play_game` method of your `TicTacToe` class in order to optionally return additional metrics for a more fine grained evaluation!


```python
import time

ttt = TicTacToe()
terminal_states = []
time_taken = []

# YOUR CODE HERE

# MiniMax vs MiniMax
minimax_player = MiniMax()
for _ in range(10):
    start_time = time.time()
    result = ttt.play_game(minimax_player, minimax_player, verbose=False)
    end_time = time.time()
    terminal_states.append(result)
    time_taken.append(end_time - start_time)

print("MiniMax vs MiniMax\n")    
print("Terminal States:", terminal_states)
print("Time Taken:", time_taken)


terminal_states = []
time_taken = []
# AlphaBeta vs AlphaBeta
alphabeta_player = AlphaBeta()
for _ in range(10):
    start_time = time.time()
    result = ttt.play_game(alphabeta_player, alphabeta_player, verbose=False)
    end_time = time.time()
    terminal_states.append(result)
    time_taken.append(end_time - start_time)
    
print("AlphaBeta vs AlphaBeta\n")
print("Terminal States:", terminal_states)
print("Time Taken:", time_taken)
```

    MiniMax vs MiniMax
    
    Terminal States: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Time Taken: [2.7886507511138916, 2.8396589756011963, 2.824657440185547, 2.845665454864502, 2.783790349960327, 2.8086533546447754, 2.8540143966674805, 2.882016897201538, 2.8026490211486816, 2.830656051635742]
    AlphaBeta vs AlphaBeta
    
    Terminal States: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    Time Taken: [0.004000663757324219, 0.004001140594482422, 0.004000663757324219, 0.004001140594482422, 0.0050013065338134766, 0.004000186920166016, 0.004001140594482422, 0.004001140594482422, 0.00400090217590332, 0.0040013790130615234]
    


```python

```


## Evaluating MiniMax and AlphaBeta B) 

Try to explain the above results. What are the takeways? Was this results to be expected? Why?

What does this tell us about the nature of the game that we have implemented?

YOUR ANSWER HERE
