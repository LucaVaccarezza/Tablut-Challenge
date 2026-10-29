from pydantic import BaseModel as Model

from tablut.common.enums.chess import CHESS
from tablut.common.enums.turn import TURN


class ReceiveStateType(Model):
    board: list[list[CHESS]]
    turn: TURN
