class ConnectionClosedError(ConnectionError):
    """The peer closed the connection."""


class ProtocolError(Exception):
    """The peer sent data that violates the wire protocol."""
