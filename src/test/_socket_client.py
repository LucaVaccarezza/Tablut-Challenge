from tablut.common.enums.player import ROLE
from tablut.network.socket_client import SocketClient


def start_game(client):
    while True:
        state = client.receive_state()
        print(state)


if __name__ == "__main__":
    client = SocketClient(ROLE.WHITE)
    client.connect()
    start_game(client)
