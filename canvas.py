from ipycanvas import Canvas

class Canvas_TicTacToe:
    """Play a 3x3 TicTacToe game on HTML canvas
    """
    def __init__(self, ttt, player_1='human', player_2='random', id=None,
                 width=300, height=300):
        valid_players = ('human', 'random', 'alphabeta')
        if player_1 not in valid_players or player_2 not in valid_players:
            raise TypeError("Players must be one of {}".format(valid_players))
        self.width = width
        self.height = height
        self.canvas = Canvas(width=width, height=height)
        self.ttt = ttt
        self.state = self.ttt.initial
        self.turn = 0
        self.canvas.line_width = 5
        self.players = (player_1, player_2)
        self.draw_board()
        self.canvas.font = "Ariel 30px"
        self.canvas.on_mouse_down(self.mouse_click)

    def mouse_click(self, x, y):
        self.canvas.stroke_arc((1/3 + 1/6)*self.width, (1/3 + 1/6)*self.height, 1/9*self.width, 0*self.height, 360)
        player = self.players[self.turn]
        if self.ttt.terminal_test(self.state):
            return

        if player == 'human':
            x, y = int(3*x/self.width) + 1, int(3*y/self.height) + 1
            if (x, y) not in self.ttt.actions(self.state):
                # Invalid move
                return
            move = (x, y)
        elif player == 'alphabeta':
            move = alphabeta_player(self.ttt, self.state)
        else:
            move = random_player(self.ttt, self.state)
        self.state = self.ttt.result(self.state, move)
        self.turn ^= 1
        self.draw_board()

    def draw_board(self):
        self.canvas.clear()
        self.canvas.stroke_style("black")
        offset = 1/20
        self.canvas.stroke_line((0 + offset)*self.width, 1/3*self.height, (1 - offset)*self.width, 1/3*self.height)
        self.canvas.stroke_line((0 + offset)*self.width, 2/3*self.height, (1 - offset)*self.width, 2/3*self.height)
        self.canvas.stroke_line(1/3*self.width, (0 + offset)*self.height, 1/3*self.width, (1 - offset)*self.height)
        self.canvas.stroke_line(2/3*self.width, (0 + offset)*self.height, 2/3*self.width, (1 - offset)*self.height)
        board = self.state.board
        for mark in board:
            if board[mark] == 'X':
                self.draw_x(mark)
            elif board[mark] == 'O':
                self.draw_o(mark)
        if self.ttt.terminal_test(self.state):
            # End game message
            utility = self.ttt.utility(self.state, self.ttt.to_move(self.ttt.initial))
            if utility == 0:
                self.canvas.stroke_text('Game Draw!', 0.1, 0.1)
            else:
                self.canvas.stroke_text('Player {} wins!'.format(1 if utility > 0 else 2), 2, 10)
        else:  # Print which player's turn it is
            self.canvas.fill_text("Player {}'s move({})".format(self.turn+1, self.players[self.turn]),
                        2, 10)


    def draw_x(self, position):
        self.canvas.stroke_style("green")
        x, y = [i-1 for i in position]
        offset = 1/15
        self.canvas.stroke_line((x/3 + offset)*self.width, (y/3 + offset)*self.height, (x/3 + 1/3 - offset)*self.width,
                                (y/3 + 1/3 - offset)*self.height)
        self.canvas.stroke_line((x/3 + 1/3 - offset)*self.width, (y/3 + offset)*self.height, (x/3 + offset)*self.width,
                                (y/3 + 1/3 - offset)*self.height)

    def draw_o(self, position):
        self.canvas.stroke_style("red")
        self.canvas.stroke()
        x, y = [i-1 for i in position]
        self.canvas.stroke_arc((x/3 + 1/6)*self.width, (y/3 + 1/6)*self.height, 1/9*self.width, 0*self.height, 360)