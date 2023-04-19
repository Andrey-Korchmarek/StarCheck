from ursina import *
from __init__ import *
from GameBoard import GameBoard
from Player import Player

class Game(object):
    def __init__(self, boardSize):
        self.level: int = self.get_board_level(boardSize)
        self.preparation()

    def get_board_level(self, size) -> int:
        if size < 1:
            return 0
        elif size < 7:
            return int(size)
        else:
            return 7

    def preparation(self):
        self.board = GameBoard(self.level, self.play, self.end_of_game)
        self.P1 = Player(WHITE)
        self.P2 = Player(BLACK)
        self.board.add_units(self.P1.generate_units(self.level))
        self.board.add_units(self.P2.generate_units(self.level))
        self.gameover = False
        self.active = self.P1
        self.waiting = self.P2
        self.waiting.set_collider(False)
        self.board.catch = self.active.add_capture
        self.board.set_units_action(self.active.side, self.waiting.side)

    def play(self):
        print_on_screen('NEW TURN', position=(0, 0), origin=(0, 0), scale=8, duration=3)
        self.active.set_collider(False)
        self.active, self.waiting = self.waiting, self.active
        self.board.set_units_action(self.active.side, self.waiting.side)
        self.active.set_collider(True)
        self.board.catch = self.active.add_capture

    def end_of_game(self):
        endgame = WindowPanel(
            title='player WINN',
            content=(
                Button(text='Restart', color=color.green),
                Button(text='Exit', color=color.red, on_click=application.quit),
            ),
        )
        endgame.content[0].on_click=Sequence(endgame.disable, scene.clear, self.preparation)

if __name__ == '__main__':
    app = Ursina()
    window.fullscreen = True
    window.exit_button.visible = False
    EditorCamera()
    #Sky(texture="textures/sky")
    game = Game(3)
    def input(key):
        if 'escape' == key:
            application.quit()
        if 'tab' == key:
            game.board.switch_cell_visibility()
    app.run()
