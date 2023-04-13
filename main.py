from ursina import *
from __init__ import *
from GameBoard import GameBoard
from Player import Player

class Game(Ursina):
    def __init__(self, boardSize):
        self.level: int = self.get_board_level(boardSize)
        super().__init__(
            fullscreen=True,
        )
        window.exit_button.visible = False
        EditorCamera()
        self.board = GameBoard(self.level)
        self.P1 = Player(WHITE)
        self.P2 = Player(BLACK)
        self.board.add_units(self.P1.generate_units(self.level))
        self.board.add_units(self.P2.generate_units(self.level))

    def get_board_level(self, size) -> int:
        if size < 1:
            return 0
        elif size < 7:
            return int(size)
        else:
            return 7

    def play(self):
        gameOver = False
        currentPlayer = self.P1
        opponent = self.P2
        while False == gameOver:
            opponent.set_collider(False)
            currentPlayer.set_collider(True)


            gameOver = True
        WindowPanel(
            title='player WINN',
            content=(
                Button(text='Restart', color=color.green),
                Button(text='Exit', color=color.red, on_click=application.quit),
            ),
        )
    def input(self, key, is_raw=False):
        super().input(key)
        print(key)
        if 'escape' == key:
            application.quit()
        if 'tab' == key:
            self.board.switch_cell_visibility()
        if 'space' == key:
            self.play()

if __name__ == '__main__':
    app = Game(3)
    app.run()
