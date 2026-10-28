from tablut.common.enums.player import ROLE


class ChessGameInterface:
    def __init__(self) -> None:
        self.chess_board = None
        self.player: ROLE = ROLE.BLACK

    def __update_chessboard(self):
        pass

    def __get_movement(self):
        pass


    def start_game(self):
        pass
