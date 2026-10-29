import json
import socket
import struct
from typing import Any

from tablut.common.enums.player import ROLE
from tablut.common.types.receive_state import ReceiveStateType
from tablut.network.errors import ConnectionClosedError, ProtocolError
from tablut.utils.logger import Logger

_LENGTH_PREFIX_SIZE = 4
_MAX_MESSAGE_SIZE = 1024 * 1024
_CONNECT_TIMEOUT = 10.0


class SocketClient:
    def __init__(
        self,
        role: ROLE,
        name: str = "SocketClient",
        host: str = "localhost",
    ) -> None:
        self.logger = Logger(name)
        self.host = host
        self.port = 5800 if role == ROLE.WHITE else 5801
        self.sock: socket.socket | None = None

    def connect(self) -> None:
        try:
            self.sock = socket.create_connection(
                (self.host, self.port), timeout=_CONNECT_TIMEOUT
            )
        except OSError as e:
            self.logger.error(f"Failed to connect to {self.host}:{self.port} - {e}")
            self.sock = None
            raise
        # Waiting for the opponent can take a whole move timeout: block forever.
        self.sock.settimeout(None)
        self.logger.info(f"Connected to {self.host}:{self.port}")

    def disconnect(self) -> None:
        if self.sock:
            try:
                self.sock.close()
                self.logger.info(f"Disconnected from {self.host}:{self.port}")
            except OSError as e:
                self.logger.error(
                    f"Failed to disconnect from {self.host}:{self.port} - {e}"
                )
            finally:
                self.sock = None

    def send_name(self, player_name: str) -> None:
        """Declare the player name: the first message the referee expects."""
        self._send_message(player_name)
        self.logger.info(f"Declared name: {player_name}")

    def receive_state(self) -> ReceiveStateType:
        """Block until one full state message arrives and return it as a dict."""
        self.logger.debug("Waiting to receive state...")
        header = self._recv_exact(_LENGTH_PREFIX_SIZE)
        (length,) = struct.unpack(">i", header)
        if not 0 <= length <= _MAX_MESSAGE_SIZE:
            raise ProtocolError(f"Invalid message length: {length}")
        payload = self._recv_exact(length)
        try:
            state = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as e:
            raise ProtocolError(f"Invalid state payload: {e}") from e
        self.logger.debug(f"Received state: {state}")

        # FIXME: transform the data
        return ReceiveStateType.model_validate(state)

    def _send_message(self, obj: Any) -> None:
        payload = json.dumps(obj).encode("utf-8")
        header = struct.pack(">i", len(payload))
        self._require_socket().sendall(header + payload)

    def _require_socket(self) -> socket.socket:
        if self.sock is None:
            raise ConnectionError("Not connected: call connect() first")
        return self.sock

    def _recv_exact(self, n: int) -> bytes:
        sock = self._require_socket()
        buf = bytearray()
        while len(buf) < n:
            self.logger.debug(f"Receiving {n - len(buf)} more bytes...")
            chunk = sock.recv(n - len(buf))
            if not chunk:
                raise ConnectionClosedError(
                    f"Connection closed by {self.host}:{self.port}"
                )
            buf.extend(chunk)
        return bytes(buf)
