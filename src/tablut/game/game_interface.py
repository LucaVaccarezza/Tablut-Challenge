from tablut.common.enums.chess import CHESS
from tablut.common.enums.game_status import GAME_STATUS
from tablut.common.enums.player import ROLE
from tablut.common.enums.turn import TURN
from tablut.common.types.receive_state import ReceiveStateType
from tablut.network.socket_client import SocketClient
from tablut.utils.logger import Logger


class ChessGameInterface:
    def __init__(
        self,
        role: ROLE,
        time_out: float,
        host: str,
        player_name: str = "Cooked",
    ) -> None:
        # Game Status
        self.__chess_board: list[list[CHESS]] = [
            [CHESS.EMPTY for _ in range(9)] for _ in range(9)
        ]
        self.__game_status: GAME_STATUS = GAME_STATUS.INITIAL

        # Assets
        self.__role: ROLE = role
        self.__player_name = player_name
        self.__time_out = time_out
        self.__server = SocketClient(role=self.__role, host=host)
        self.logger = Logger(f"ChessGame_{player_name}")

    def __next_move(self) -> None:
        pass

    def __update_chessboard(self, chess_board: list[list[CHESS]]) -> None:
        self.logger.info("Updating the chess board")
        self.__chess_board = chess_board

    def __get_movement(self) -> None:  # FIXME: Add the return type
        pass

    def __initialize(self) -> None:
        try:
            # Initialize the chess board or any other necessary setup
            self.logger.info("Initializing the chess board")
            self.__server.connect()
            self.__server.send_name(self.__player_name)

            # TODO: CHECK HOW TO UPDATE THE STATUS OF THE GAME
            self.__game_status = GAME_STATUS.WAIT

        except Exception as e:
            self.logger.error(f"Initialization failed: {e}")

    def start_game(self) -> None:
        if self.__game_status == GAME_STATUS.INITIAL:
            self.__initialize()

        while (
            self.__game_status != GAME_STATUS.INITIAL
            and self.__game_status != GAME_STATUS.FINISHED
        ):

            self.logger.info(f"Current game status: {self.__game_status}")

            
            if self.__game_status == GAME_STATUS.PLAY:
                self.__next_move()

            server_response = ReceiveStateType.model_validate(
                self.__server.receive_state()
            )

            if server_response.turn in [TURN.DRAW, TURN.WHITEWIN, TURN.BLACKWIN]:
                self.logger.info(f"Game ended with turn: {server_response.turn}")
                self.__game_status = GAME_STATUS.FINISHED
                continue

            # TURN and ROLE are different enums: compare their values.
            self.__game_status = (
                GAME_STATUS.PLAY
                if server_response.turn.value == self.__role.value
                else GAME_STATUS.WAIT
            )
